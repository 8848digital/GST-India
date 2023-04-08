import frappe
from frappe import *
import gst_india.utils as utils
import requests
import json 
from gst_india.API.ewb import get_delivery_note

@frappe.whitelist(allow_guest=True)
def generate_irn(**kwargs):
    try:
        invoice = frappe.get_doc('Sales Invoice',kwargs.get('invoice'))
        item_list = []
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        gst_round_off = frappe.db.get_single_value('GST Settings','round_off_gst_values')
        for row in invoice.items:
            item_list.append(utils.get_dict('Item',row.item_code))
        data = {
            'invoice': invoice.as_dict(),
            'customer': utils.get_dict('Customer',invoice.customer),
            'billing_address': utils.get_dict('Address',invoice.company_address),
            'customer_address': utils.get_dict('Address',invoice.customer_address),
            'shipping_address': utils.get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': utils.get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts,
            'gst_round_off': gst_round_off
        }
        if kwargs.get('ewb') == '1':
            delivery_note = get_delivery_note(invoice)
            data['transporter'] = utils.get_dict('Supplier',delivery_note.transporter)
            data['delivery_note'] = delivery_note
        return create_irn_request(data,invoice.name)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)



def create_irn_request(data,inv):
    try:
        url = utils.get_url()
        url+= "irn.generate_irn"
        headers = utils.set_headers()
        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=payload) 
        response = utils.process_request(response,'GENERATE IRN',"Sales Invoice",inv)
        store_irn_details(inv,response['response'])
        return utils.success_response()
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)

def store_irn_details(inv,response):
    try:
        gsp = utils.get_gsp()
        if gsp:
            store_irn_cl(inv,response[0])
        else:
            store_irn_ms(inv,response)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)

def store_irn_ms(inv,response):
    try:
        response = response.get('results').get('message')
        frappe.db.set_value("Sales Invoice", inv, {
            'acknowledgement_number': response.get('AckNo'),
            'acknowledgement_date': response.get('AckDt'),
            'signed_invoice':  response.get('SignedInvoice'),
            'signed_qr_code':  response.get('SignedQRCode'),
            'irn':  response.get('Irn'),
            'irn_status':  response.get('status')
            })
        if response.get('EwbNo'):
             frappe.db.set_value("Sales Invoice", inv, {
                'ewaybill': response.get('EwbNo'),
                'ewb_date': response.get('EwbDt'),
                'eway_bill_validity':  response.get('EwbValidTill')
                })
        frappe.db.commit()
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)

def store_irn_cl(inv,response):
    try:
        response = response.get('govt_response')
        frappe.db.set_value("Sales Invoice", inv, {
            'acknowledgement_number': response.get("AckNo"),
            'acknowledgement_date': response.get('AckDt'),
            'signed_invoice': response.get('SignedInvoice'),
            'signed_qr_code': response.get('SignedQRCode'),
            'irn': response.get('Irn'),
            'irn_status': response.get('Status')
            })
        frappe.db.commit()
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)



@frappe.whitelist()
def cancel_irn(**kwargs):
    try:
        inv= kwargs.get('invoice')
        data = json.loads(kwargs.get('data'))
        reason = data.get('reason')
        if reason == 'Duplicate':
            reason ='1'
        elif reason == 'Data entry mistake':
            reason='2'
        elif reason == 'Order Cancelled':
            reason='3' 
        elif reason == 'Others':
            reason='4'
        data = {
            'irn': frappe.get_value('Sales Invoice', inv, 'irn'),
            "CnlRsn": reason,
            "CnlRem": data.get('remarks')
        }
        invoice = frappe.get_doc('Sales Invoice',inv)
        data['gstin'] = frappe.get_value('Address',invoice.company_address,'gstin')
        return cancel_irn_request(inv,data) 
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)


def cancel_irn_request(inv,data):
    try:
        url = utils.get_url()
        url+= "irn.cancel_irn"
        headers = utils.set_headers()
        payload = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        response = utils.process_request(response,'CANCEL IRN',"Sales Invoice",inv)
        frappe.db.set_value('Sales Invoice',inv,'irn_cancelled',1)
        return utils.success_response()
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return utils.error_response(e)

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
            frappe.enqueue("gst_india.API.irn.generate_irn",**{'invoice':i})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)