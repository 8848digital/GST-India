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
            invoice = frappe.get_doc('Sales Invoice',kwargs.get('invoice'))
        else:
            invoice = frappe.get_doc('Purchase Invoice',kwargs.get('invoice'))
        item_list = []
        gst_settings_accounts = frappe.get_all("GST Account",
                filters={'company':invoice.company},
                fields=["cgst_account", "sgst_account", "igst_account", "cess_account"])
        for row in invoice.items:
            item_list.append(get_dict('Item',row.item_code))
        data = {
            'invoice': invoice.as_dict(),
            'type': type,
            'customer': get_dict('Customer',invoice.customer),
            'billing_address': get_dict('Address',invoice.company_address),
            'customer_address': get_dict('Address',invoice.customer_address),
            'shipping_address': get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts
        }
        if invoice.is_return:
            data['original_invoice'] = get_dict('Sales Invoice',invoice.return_against)
            return gst_cdn_request(data,kwargs.get('invoice'),type)
        if invoice.is_debit_note:
            data['original_invoice'] = get_dict('Sales Invoice',invoice.return_against)
        return gst_invoice_request(data,kwargs.get('invoice'),type)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def gst_invoice_request(data,id,type):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_site
        url+= "/api/method/cleartax.cleartax.API.gst.generate_gst"
        headers = {
            'Content-Type': 'application/json'
        }
        if type == 'SALE':
            gstin = data.get('seller').get('gstin')
        if settings.enterprise:
            headers['auth_token'] = settings.production_auth_token
            headers['tax_id'] = settings.tax_id(gstin)
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data)
        response = response.json()['message']
        api = "GENERATE GST SINV" if type == 'SALE' else "GENERATE GST PINV"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response = response['msg']
        response_status = response['msg']['response_status']
        response_logger(data,response,api,doctype,id,response_status)
        if response_status == "Success":
            if type == 'SALE':
                frappe.db.set_value('Sales Invoice',id,'gst_invoice',1)
            else:
                frappe.db.set_value('Purchase Invoice',id,'gst_invoice',1)
            return success_response(response)
        return response_error_handling(response['response'])
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def gst_cdn_request(data,id,type):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_site
        url+= "/api/method/cleartax.cleartax.API.gst.generate_cdn"
        headers = {
            'sandbox': str(settings.sandbox),
            'Content-Type': 'application/json'
        }
        if settings.enterprise:
            if settings.sandbox:
                headers['auth_token'] = settings.sandbox_auth_token
            else:
                headers['auth_token'] = settings.production_auth_token
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data)
        response = response['msg']
        response_status = response['msg']['response_status']
        api = "GENERATE GST CDN"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response_logger(data,response,api,doctype,id,response_status)
        if response_status == 'Success':
            if type == 'SALE':
                doc = frappe.get_doc('Sales Invoice',id)
                if doc.is_return or doc.is_debit_note:
                    doc.cdn=1
            else:
                doc = frappe.get_doc('Purchase Invoice',id)
                if doc.is_return or doc.is_debit_note:
                    doc.cdn=1
            doc.save(ignore_permissions=True)
            return success_response(response)
        return response_error_handling(error)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)

