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
            'invoice': frappe._dict(invoice),
            'billing_address': get_dict('Address',invoice.company_address),
            'customer_address': get_dict('Address',invoice.customer_address),
            'shipping_address': get_dict('Address',invoice.shipping_address_name),
            'dispatch_address': get_dict('Address',invoice.dispatch_address_name),
            'item_list': item_list,
            'gst_accounts':gst_settings_accounts
        }
        if invoice.is_return:
            return gst_cdn_request(data,kwargs.get('invoice'),type)
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
            'sandbox': settings.sandbox,
            'username': settings.username,
            'api_key': settings.get_password('api_key'),
            'Content-Type': 'application/json'
        }
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data)
        error = response.text
        response = response.json()
        api = "GENERATE GST SINV" if type == 'SALE' else "GENERATE GST PINV"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response_status = "Failed"
        if response.get('invoice_status') == 'CREATED':
            response_status = "Success"
            response_logger(data,response,api,doctype,id,response_status)
            if type == 'SALE':
                frappe.db.set_value('Sales Invoice',id,'gst_invoice',1)
            else:
                frappe.db.set_value('Purchase Invoice',id,'gst_invoice',1)
            return success_response(response)
        return response_error_handling(error)
    except Exception as e:
        frappe.logger('cleartax').exception(e)
        return error_response(e)


def gst_cdn_request(data,id,type):
    try:
        settings = frappe.get_doc('Cleartax Settings')
        url = settings.host_site
        url+= "/api/method/cleartax.cleartax.API.gst.generate_cdn"
        headers = {
            'sandbox': settings.sandbox,
            'username': settings.username,
            'api_key': settings.get_password('api_key'),
            'Content-Type': 'application/json'
        }
        data = json.dumps(data, indent=4, sort_keys=False, default=str)
        response = requests.request("PUT", url, headers=headers, data= data)
        error = response.text
        response = response.json()
        api = "GENERATE GST CDN"
        doctype = "Sales Invoice" if type == 'SALE' else "Purchase Invoice"
        response_status = " Failed"
        if response.get('cdn_status') == 'CREATED':
            response_status = "Success"
            response_logger(data,response,api,doctype,id,response_status)
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

