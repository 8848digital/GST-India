import frappe 
from cleartax_integration.cleartax_integration.API.gst import create_gst_invoice 


def purchase_invoice_submit(doc, method=None):
    if frappe.get_value('Cleartax Settings', 'Cleartax Settings','automate'):
        r = create_gst_invoice(**{'invoice':doc.name,'type': "PURCHASE"})
        if r.get('msg') == "success":
            doc.gst_invoice = 1

def purchase_invoice_cancel(doc, method=None):
    if frappe.get_value('Cleartax Settings', 'Cleartax Settings','automate'):
        create_gst_invoice(**{'invoice':doc.name,'type': "PURCHASE",'cancel':1})