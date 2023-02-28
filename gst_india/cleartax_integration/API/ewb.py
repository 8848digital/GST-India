import frappe
from gst_india.cleartax_integration.utils import success_response, error_response, response_error_handling, response_logger,get_dict
from frappe import *
import json
import requests

@frappe.whitelist()
def generate_e_waybill_by_irn(**kwargs):
    try:
        transporter_details = None
        invoice = frappe.get_doc('Sales Invoice',kwargs.get('invoice'))
        item_list = []
        gst_round_off = frappe.get_value('GST Settings','round_off_gst_values')
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in invoice.items:
            item_list.append(get_dict('Item',row.item_code))
        delivery_note = get_delivery_note(invoice)
        transporter = delivery_note.transporter
        data = {
            'invoice': invoice.as_dict(),
            'customer': get_dict('Customer',invoice.customer),
            'billing_address': get_dict('Address',invoice.company_address),
            'customer_address': get_dict('Address',invoice.customer_address),
            'shipping_address': get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts,
            'gst_round_off': gst_round_off,
            'delivery_note': delivery_note,
            'transporter': get_dict('Supplier',transporter)
       }
        dispatch_address = frappe.get_doc("Address",invoice.dispatch_address_name)
        return create_ewb_request(invoice,dispatch_address.gstin,data)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def create_ewb_request(inv,gstin,data):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.generate_e_waybill_by_irn"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=data)
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_status = response['msg']
        response_logger(response['request'],response['response'],"GENERATE EWB BY IRN","Sales Invoice",inv.name,
                        response_status)
        if response_status == "Success":
            return store_ewb_details(inv.name,data,response['response'][0])
        return response_error_handling(response['response'])
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)



@frappe.whitelist()
def ewb_without_irn(**kwargs):
    try:
        delivery_note = frappe.get_doc('Delivery Note',kwargs.get('delivery_note'))
        item_list = []
        gst_round_off = frappe.get_value('GST Settings','round_off_gst_values')
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':delivery_note.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in delivery_note.items:
            item_list.append(get_dict('Item',row.item_code))
        data = {
            'delivery_note':  delivery_note.as_dict(),
            'billing_address': get_dict('Address',delivery_note.company_address),
            'customer_address': get_dict('Address',delivery_note.customer_address),
            'shipping_address': get_dict('Address',delivery_note.shipping_address_name),
            'dispatch_address': get_dict('Address',delivery_note.dispatch_address_name),
            'transporter': get_dict('Supplier',delivery_note.transporter),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts,
            'gst_round_off': gst_round_off
        }
        return ewb_without_irn_request(data,delivery_note=kwargs.get('delivery_note'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

def ewb_without_irn_request(data,delivery_note=None,subcontracting_challan=None):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.ewb_without_irn"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=data)
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_status = response['msg']
        if delivery_note:
            response_logger(response['request'],response['response'],"GENERATE EWB WITHOUT IRN","Delivery Note",delivery_note,
                            response_status)
            if response_status == 'Success':
                return store_ewb_details_dn(delivery_note,data,response['response'])
        if subcontracting_challan:
            response_logger(response['request'],response['response'],"GENERATE EWB WITHOUT IRN","Subcontracting Challan",subcontracting_challan,
                            response_status)
            if response_status == 'Success':
                return store_ewb_details_sc(subcontracting_challan,data,response['response'])
        return response_error_handling(response['response'])
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e) 

def store_ewb_details_dn(delivery_note,data,response):
    frappe.db.set_value('Delivery Note',delivery_note,'ewaybill', response.get('govt_response').get('EwbNo'))
    frappe.db.set_value('Delivery Note',delivery_note,'ewb_date', response.get('govt_response').get('EwbDt'))
    frappe.db.set_value('Delivery Note',delivery_note,'ewb_valid_till', response.get('govt_response').get('EwbValidTill'))
    frappe.db.set_value('Delivery Note',delivery_note,'ewb_trans_id', response.get('transaction_id'))
    frappe.db.commit()
    return success_response()

def store_ewb_details_sc(subcontracting_challan,data,response):
    frappe.db.set_value('Subcontracting Challan',subcontracting_challan,'ewaybill', response.get('govt_response').get('EwbNo'))
    frappe.db.set_value('Subcontracting Challan',subcontracting_challan,'ewb_date', response.get('govt_response').get('EwbDt'))
    frappe.db.set_value('Subcontracting Challan',subcontracting_challan,'ewb_valid_till', response.get('govt_response').get('EwbValidTill'))
    frappe.db.set_value('Subcontracting Challan',subcontracting_challan,'ewb_trans_id', response.get('transaction_id'))
    frappe.db.commit()
    return success_response()




@frappe.whitelist()
def update_ewb_partb(**kwargs):
    try:
        delivery_note = frappe.get_doc('Delivery Note', kwargs.get('delivery_note'))
        data = {
            'data' : json.loads(kwargs.get('data')),
            'delivery_note': delivery_note.as_dict(),
            'dispatch_address': get_dict('Address', delivery_note.dispatch_address_name),
            'shipping_address': get_dict('Address',delivery_note.shipping_address_name)
        }
        return partb_request(data,dn=kwargs.get('delivery_note'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


@frappe.whitelist()
def update_ewb_partb_sc(**kwargs):
    try:
        sc = frappe.get_doc('Subcontracting Challan', kwargs.get('doc'))
        data = {
            'data' : json.loads(kwargs.get('data')),
            'delivery_note': sc.as_dict(),
            'dispatch_address': get_dict('Address', sc.billing_address),
            'shipping_address': get_dict('Address',sc.shipping_address)
        }
        return partb_request(data,sc=kwargs.get('doc'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def partb_request(data,dn=None,sc=None):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.update_ewb_partb"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        data = json.dumps(data, indent=4, sort_keys=False, default=str)    
        response = requests.request(
            "POST", url, headers=headers, data=data)
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_status = response['status']
        if dn:
            response_logger(response['request'],response['response'],"UPDATE PART B","Delivery Note",dn,response_status)
        elif sc:
            response_logger(response['request'],response['response'],"UPDATE PART B","Subcontracting Challan",sc,response_status)
        if response_status == 'Success':
            if dn:
                frappe.db.set_value('Delivery Note',dn,'update_partb',1)
            elif sc:
                frappe.db.set_value('Subcontracting Challan',sc,'update_partb',1)
            return success_response(response['response'])
        else:
            return response_error_handling(response['response'])
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

    



@frappe.whitelist()
def cancel_ewb(**kwargs):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.cancel_ewb"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        invoice = frappe.get_doc('Sales Invoice', kwargs.get('invoice'))
        gstin = frappe.get_value('Address', invoice.company_address,'gstin')
        data = json.loads(kwargs.get('data'))
        data = {
                    "ewbNo": invoice.ewaybill,
                    "cancelRsnCode": data.get('reason'),
                    "cancelRmrk" : data.get('remarks'),
                    'gstin': gstin,
                    'invoice': invoice.name
                }
        return cancel_ewb_request(headers,url,data,invoice.name)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

@frappe.whitelist()
def cancel_ewb_dn(**kwargs):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.cancel_ewb"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        deliver_note = frappe.get_doc('Delivery Note', kwargs.get('delivery_note'))
        gstin = frappe.get_value('Address', deliver_note.dispatch_address_name,'gstin')
        data = json.loads(kwargs.get('data'))
        data = {
                    "ewbNo": deliver_note.ewaybill,
                    "cancelRsnCode":data.get('reason'),
                    "cancelRmrk" : data.get('remarks'),
                    "gstin":gstin
                }
        return cancel_ewb_request(headers,url,data,delivery_note=kwargs.get('delivery_note'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)
        

@frappe.whitelist()
def cancel_ewb_sc(**kwargs):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.ewb.cancel_ewb"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['token'] = settings.get_password('sandbox_auth_token')
            else:
                headers['token'] = settings.get_password('production_auth_token')
        sc = frappe.get_doc('Subcontracting Challan', kwargs.get('doc'))
        gstin = frappe.get_value('Address', sc.billing_address,'gstin')
        data = json.loads(kwargs.get('data'))
        data = {
                    "ewbNo": sc.ewaybill,
                    "cancelRsnCode":data.get('reason'),
                    "cancelRmrk" : data.get('remarks'),
                    "gstin":gstin
                }
        return cancel_ewb_request(headers,url,data,sc=kwargs.get('doc'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def store_ewb_details(inv,data,response):
    try:
        response = response.get('govt_response')
        if response.get('Status') == "GENERATED" or response.get('Status')== 'PARTA_GENERATED':
            frappe.db.set_value('Sales Invoice',inv,'ewaybill', response.get('EwbNo'))
            frappe.db.set_value('Sales Invoice',inv,'ewb_date', response.get('EwbDt'))
            frappe.db.set_value('Sales Invoice',inv,'eway_bill_validity', response.get('EwbValidTill'))
            frappe.db.commit()
            return success_response(response)
        return response_error_handling(response)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)




def cancel_ewb_request(headers,url,data,invoice=None,delivery_note=None,sc=None):
    data = json.dumps(data, indent=4, sort_keys=False, default=str)
    response = requests.request(
            "POST", url, headers=headers, data=data)
    response = response.json()['message']
    doctype = "Sales Invoice" if invoice else "Delivery Note"
    docname = invoice if invoice else delivery_note
    response_status = "Failed"
    if response.get('error'):
        return error_response(response.get('error'))
    if response['response'].get('ewbStatus') == 'CANCELLED':
        response_status = "Success"
        response_logger(response['request'],response['response'],"CANCEL EWB",doctype,docname,response_status)
        if invoice:
            frappe.db.set_value('Sales Invoice',invoice,'eway_bill_cancelled',1)
        elif delivery_note:
            frappe.db.set_value('Delivery Note',delivery_note,'eway_bill_cancelled',1)
        elif sc:
            frappe.db.set_value('Subcontracting Challan',sc,'eway_bill_cancelld',1)
        return success_response(data="EWB Cancelled Successfully!")
    return response_error_handling(response) 



def get_delivery_note(doc):
        delivery_note = frappe.get_value('Delivery Note Item',{"against_sales_invoice":doc.name},"parent")
        if delivery_note:
            return frappe.get_doc('Delivery Note',delivery_note).as_dict()
        delivery_note = frappe.get_value('Sales Invoice Item',{"parent":doc.name},"delivery_note")
        if delivery_note:
            return frappe.get_doc('Delivery Note',delivery_note).as_dict()
        if frappe.db.exists('Transporter Details', {'sales_invoice':doc.name}):
            td = frappe.get_value('Transporter Details', {'sales_invoice':doc.name},'name')
            return frappe.get_doc('Transporter Details',td).as_dict()
        return {}



@frappe.whitelist()
def bulk_ewb(**kwargs):
    try:
        data = json.loads(kwargs.get('data'))
        for i in data:
            frappe.enqueue("gst_india.cleartax_integration.API.ewb.generate_e_waybill_by_irn",**{'invoice':i})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)

@frappe.whitelist()
def bulk_ewb_dn(**kwargs):
    try:
        data = json.loads(kwargs.get('data'))
        for i in data:
            frappe.enqueue("gst_india.cleartax_integration.API.ewb.ewb_without_irn",**{'delivery_note':i})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)


@frappe.whitelist()
def sub_con_ewb(**kwargs):
    try:
        sc = frappe.get_doc('Subcontracting Challan',kwargs.get('subcontracting_challan'))
        item_list = []
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':sc.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in sc.items:
            item_list.append(get_dict('Item',row.item_code))
        data = {
            'delivery_note':  sc.as_dict(),
            'billing_address': get_dict('Address',sc.billing_address),
            'customer_address': get_dict('Address',sc.shipping_address),
            'shipping_address': get_dict('Address',sc.shipping_address),
            'dispatch_address': get_dict('Address',sc.billing_address),
            'transporter': get_dict('Supplier',sc.transporter),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts
        }
        return ewb_without_irn_request(data,subcontracting_challan=kwargs.get('subcontracting_challan'))
    except Exception as e:
        frappe.logger('cleartax').exception(e)
