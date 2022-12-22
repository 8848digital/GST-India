import frappe
from frappe import *
from india_compliance.cleartax_integration.utils import success_response, error_response, response_error_handling, response_logger, get_dict
import requests
import json 

@frappe.whitelist(allow_guest=True)
def generate_irn(**kwargs):
    try:
        invoice = frappe.get_doc(get_doc('Sales Invoice',kwargs.get('invoice')))
        item_list = []
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        gst_round_off = frappe.get_value('GST Settings','round_off_gst_values')
        #add batch
        for row in invoice.items:
            item_list.append(get_dict('Item',row.item_code))
        #     if row.batch_no:
        #         item_list[-1]['batch_no'] = get_dict('Batch',row.batch_no)
            
        
        data = {
            'invoice': invoice.as_dict(),
            'customer': get_dict('Customer',invoice.customer),
            'billing_address': get_dict('Address',invoice.company_address),
            'customer_address': get_dict('Address',invoice.customer_address),
            'shipping_address': get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts,
            'gst_round_off': gst_round_off
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
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')

        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=payload) 
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_logger(response['request'],response['response'],"GENERATE IRN","Sales Invoice",inv,response['msg'])
        if response['msg'] == 'Success':
            store_irn_details(inv,response['response'][0])
            return success_response()
        return response_error_handling(json.loads(json.dumps(response['response'][0])))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


@frappe.whitelist()
def store_irn_details(inv,response):
    try:
        frappe.db.set_value("Sales Invoice",inv,'acknowledgement_number', response.get('govt_response').get("AckNo"))
        frappe.db.set_value("Sales Invoice",inv,'acknowledgement_date', response.get('govt_response').get('AckDt'))
        frappe.db.set_value("Sales Invoice",inv,'signed_invoice', response.get('govt_response').get('SignedInvoice'))
        frappe.db.set_value("Sales Invoice",inv,'signed_qr_code', response.get('govt_response').get('SignedQRCode'))
        frappe.db.set_value("Sales Invoice",inv,'irn', response.get('govt_response').get('Irn'))
        frappe.db.set_value("Sales Invoice",inv,'irn_status', response.get('govt_response').get('Status'))
        frappe.db.commit()
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
        invoice = frappe.get_doc('Sales Invoice',inv)
        gstin = frappe.get_value('Address',invoice.dispatch_address_name,'gstin')
        if not gstin:
            company_address = frappe.db.get_value('Dynamic Link',{
                    'link_doctype': "Company", 
                    'link_name': frappe.get_value('Sales Invoice',inv,'company'), 
                    'parenttype': 'Address'
                    }, ['parent'])
            gstin = frappe.get_value("Address",company_address,'gstin')
        data['gstin'] = gstin
        return cancel_irn_request(inv,data) 
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def cancel_irn_request(inv,data):
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
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_status = response['msg']
        if response_status == 'Success':
            frappe.db.set_value('Sales Invoice',inv,'irn_cancelled',1)
            return success_response()
        response_logger(response['request'],response['response'],"CANCEL IRN","Sales Invoice",inv,response_status)
        return response_error_handling(response)
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
            frappe.enqueue("india_compliance.cleartax_integration.API.irn.generate_irn",**{'invoice':i})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)