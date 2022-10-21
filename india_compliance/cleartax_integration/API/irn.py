import frappe
from frappe import *
from india_compliance.cleartax_integration.utils import success_response, error_response, response_error_handling, response_logger, get_dict
import requests
import json 

@frappe.whitelist(allow_guest=True)
def generate_irn(**kwargs):
    try:
        invoice = frappe.get_doc('Sales Invoice',kwargs.get('invoice'))
        item_list = []
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in invoice.items:
            if row.batch_no:
                row['batch'] = get_dict('Batch',row.batch_no)
            item_list.append(get_dict('Item',row.item_code))
        
        data = {
            'invoice': invoice.as_dict(),
            'customer': get_dict('Customer',invoice.customer),
            'billing_address': get_dict('Address',invoice.company_address),
            'customer_address': get_dict('Address',invoice.customer_address),
            'shipping_address': get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts
        }
        return create_irn_request(data,invoice.name)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)



def create_irn_request(data,inv):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.irn.generate_irn"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['auth_token'] = settings.sandbox_auth_token
            else:
                headers['auth_token'] = settings.production_auth_token

        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=payload) 
        response = response.json()['message']
        frappe.logger('cleartax').exception(response)
        if response['msg'] == 'Success':
            store_irn_details(**{inv,json.loads(json.dumps(response['response']))})
            return success_response()
        return response_error_handling(json.loads(json.dumps(response['response'])))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


@frappe.whitelist()
def store_irn_details(**kwargs):
    try:
        response = kwargs.get('response')
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'acknowledgement_number', response.get('govt_response').get("AckNo"))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'acknowledgement_date', response.get('govt_response').get('AckDt'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'signed_invoice', response.get('govt_response').get('SignedInvoice'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'signed_qr_code', response.get('govt_response').get('SignedQRCode'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'irn', response.get('govt_response').get('Irn'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'irn_status', response.get('govt_response').get('Status'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'ewb_number', response.get('EwbNo'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'ewb_date', response.get('EwbDt'))
        frappe.db.set_value("Sales Invoice",kwargs.get('inv'),'ewb_valid_till', response.get('EwbValidTill'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)



@frappe.whitelist()
def cancel_irn(**kwargs):
    try:
        inv= kwargs.get('invoice')
        data = json.loads(kwargs.get('data'))
        reason = data.get('reason')
        if reason == 'Duplicate':
            reason =1
        elif reason == 'Data entry mistake':
            reason=2
        elif reason == 'Order Cancelled':
            reason=3 
        elif reason == 'Others':
            reason=4
        data = {
            'irn': frappe.get_value('Sales Invoice', inv, 'irn'),
            "CnlRsn": reason,
            "CnlRem": data.get('remarks')
        }
        company_address = frappe.db.get_value('Dynamic Link',{
                'link_doctype': "Company", 
                'link_name': frappe.get_value('Sales Invoice',inv,'company'), 
                'parenttype': 'Address'
                }, ['parent'])
        addr = frappe.get_doc("Address",company_address)
        return cancel_irn_request(inv,data,addr.gstin) 
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def cancel_irn_request(inv,data,gstin):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.irn.cancel_irn"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['auth_token'] = settings.sandbox_auth_token
            else:
                headers['auth_token'] = settings.production_auth_token
        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        frappe.log_error(payload,"cancel irn")
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        response_status = "Failed"
        if response.json().get("Success") == "Y":
            response_status = "Success"
            frappe.db.set_value('Sales Invoice',inv,'irn_cancelled',1)
            return success_response()
        response_logger(payload,response.json(),"CANCEL IRN","Sales Invoice",inv,response_status)
        return response_error_handling(response.json())
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

@frappe.whitelist()
def e_invoicing_enabled(company):
    if frappe.db.exists('E Invoicing Eligible',{'company':company}):
        return True
    
    return False

@frappe.whitelist()
def bulk_irn(**kwargs):
    try:
        data = json.loads(kwargs.get('data'))
        for i in data:
            frappe.enqueue("cleartax.cleartax.API.irn.generate_irn",**{'invoice':i})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)