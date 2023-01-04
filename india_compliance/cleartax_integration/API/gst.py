import frappe
import requests
import json
from frappe import *
from india_compliance.cleartax_integration.utils import success_response, error_response, response_error_handling, response_logger, get_dict


@frappe.whitelist()
def create_gst_invoice(**kwargs):
    try:
        invoice = kwargs.get('invoice')
        type = kwargs.get('type')
        if  type == "SALE":
            doctype = "Sales Invoice"
        else:
            doctype = "Purchase Invoice"
        invoice = frappe.get_doc(doctype,kwargs.get('invoice'))
        item_list = []
        gst_round_off = frappe.get_value('GST Settings','round_off_gst_values')
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in invoice.items:
            item_list.append(get_dict('Item',row.item_code))
        data = {
            'invoice': invoice.as_dict(),
            'type': type,
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts,
            'gst_round_off': gst_round_off
        }
        if type == 'SALE':
            data['company_address'] = get_dict('Address',invoice.company_address)
            data['customer'] = get_dict('Customer',invoice.customer)
            data['customer_address'] = get_dict('Address',invoice.customer_address)
            data['shipping_address'] = get_dict('Address',invoice.shipping_address_name)
        else:
            data['company_address'] = get_dict('Address',invoice.supplier_address)
            data['customer_address'] = get_dict('Address',invoice.billing_address)
            data['shipping_address'] = get_dict('Address',invoice.shipping_address)
        if invoice.is_return:
            data['original_invoice'] = get_dict(doctype,invoice.return_against)
            return gst_cdn_request(data,kwargs.get('invoice'),type)
        # if invoice.is_debit_note:
        #     data['original_invoice'] = get_dict('Sales Invoice',invoice.return_against)
        #     return gst_cdn_request(data,kwargs.get('invoice'),type)
        return gst_invoice_request(data,kwargs.get('invoice'),type)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def gst_invoice_request(data,id,type):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.gst.create_gst_invoice"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if type == 'SALE':
            gstin = data.get('company_address').get('gstin')
        else:
            gstin = data.get('customer_address').get('gstin')
        if settings.enterprise:
            headers['token'] = settings.get_password('gst_auth_token')
            #headers['taxid'] = settings.tax_id(gstin)
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data) 
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        api = "GENERATE GST SINV" if type == 'SALE' else "GENERATE GST PINV"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response_status = response['msg']
        response_logger(response['request'],response['response'],api,doctype,id,response_status)
        if response_status == "Success":
            if type == 'SALE':
                frappe.db.set_value('Sales Invoice',id,'gst_invoice',1)
            else:
                frappe.db.set_value('Purchase Invoice',id,'gst_invoice',1)
            frappe.db.commit()
            return success_response(response['response'])
        return response_error_handling(response['response'])
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def gst_cdn_request(data,id,type):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_url
        url+= "/api/method/cleartax.cleartax.API.gst.create_gst_invoice"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if type == 'SALE':
            gstin = data.get('company_address').get('gstin')
        else:
            gstin = data.get('customer_address').get('gstin')
        if settings.enterprise:
            headers['token'] = settings.get_password('gst_auth_token')
            #headers['taxid'] = settings.tax_id(gstin)
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data)
        response = response.json()['message']
        if response.get('error'):
            return error_response(response.get('error'))
        response_status = response['msg']
        api = "GENERATE GST CDN"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response_logger(response['request'],response['response'],api,doctype,id,response_status)
        if response_status == 'Success':
            if type == 'SALE':
                frappe.db.set_value('Sales Invoice',id,'cdn',1)
            else:
                frappe.db.set_value('Purchase Invoice',id,'cdn',1)
            frappe.db.commit()
            return success_response(response['response'])
        return response_error_handling(error)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

@frappe.whitelist()
def bulk_purchase_gst(**kwargs):
    try:
        data = json.loads(kwargs.get('data'))
        for i in data:
            frappe.enqueue("india_compliance.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i,'type':'PURCHASE'})
    except Exception as e:
        frappe.logger('sfa_online').exception(e)