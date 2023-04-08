from gst_india.API.ewb import ewb_without_irn
import frappe 
from gst_india.utils import automate


def delivery_note_submit(doc, method=None):
    if automate():
        ewb_without_irn(**{'delivery_note':doc.name})

def delivery_note_save(doc,method=None):
    if not doc.shipping_address_name:
        doc.shipping_address_name = doc.customer_address
    if not doc.dispatch_address_name:
        doc.dispatch_address_name = doc.company_address

def delivery_note_cancel(doc, method=None):
    if doc.ewaybill and not doc.eway_bill_cancelled:
        frappe.throw("Please Cancel EWB!")