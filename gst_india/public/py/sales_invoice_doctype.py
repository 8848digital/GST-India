from gst_india.cleartax_integration.API.irn import generate_irn, e_invoicing_enabled
from gst_india.cleartax_integration.API.gst import create_gst_invoice
import frappe 

def sales_invoice_submit(doc, method=None):
    if frappe.db.get_single_value('Cleartax Settings','automate'):
        if e_invoicing_enabled(company=doc.company):
            generate_irn(**{'invoice':doc.name})
        else:
            create_gst_invoice(**{'invoice':doc.name,'type':"SALE"})
        frappe.db.commit()
        

def sales_invoice_cancel(doc, method=None):
    if not e_invoicing_enabled(company=doc.company):
        create_gst_invoice(**{'invoice':doc.name,'type': "SALE",'cancel':1})
    else:
        if doc.ewaybill and not doc.eway_bill_cancelled:
            frappe.throw("Please Cancel EWB!")
        if doc.irn and not doc.irn_cancelled:
            frappe.throw("Please Cancel IRN!")
            

def sales_invoice_save(doc,method=None):
    if not doc.shipping_address_name:
        doc.shipping_address_name = doc.customer_address
    if not doc.dispatch_address_name:
        doc.dispatch_address_name = doc.company_address


