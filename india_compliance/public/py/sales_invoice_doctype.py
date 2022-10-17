from cleartax_integration.cleartax_integration.API.irn import generate_irn, e_invoicing_enabled
from cleartax_integration.cleartax_integration.API.gst import create_gst_invoice
import frappe 

def sales_invoice_submit(doc, method=None):
    if frappe.get_value('Cleartax Settings', 'Cleartax Settings','automate'):
        if e_invoicing_enabled(company=doc.company):
            generate_irn(**{'invoice':doc.name})
        else:
            create_gst_invoice(**{'invoice':doc.name,'type':"SALE"})

def sales_invoice_cancel(doc, method=None):
    if frappe.get_value('Cleartax Settings', 'Cleartax Settings','automate'):
        if not e_invoicing_enabled(company=doc.company):
            create_gst_invoice(**{'invoice':doc.name,'type': "SALE",'cancel':1})



