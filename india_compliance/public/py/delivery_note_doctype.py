from cleartax_integration.cleartax_integration.API.ewb import ewb_without_irn
import frappe 

def delivery_note_submit(doc, method=None):
    if frappe.get_value('Cleartax Settings', 'Cleartax Settings','automate'):
        ewb_without_irn(**{'delivery_note':doc.name})

