import frappe 
from gst_india.cleartax_integration.API.gst import create_gst_invoice 
import secrets
import string

def purchase_invoice_submit(doc, method=None):
    if frappe.db.get_single_value('Cleartax Settings','automate'):
        r = create_gst_invoice(**{'invoice':doc.name,'type': "PURCHASE"})
        if r.get('msg') == "success":
            doc.gst_invoice = 1
            

def purchase_invoice_cancel(doc, method=None):
    if frappe.db.get_single_value('Cleartax Settings','automate'):
        create_gst_invoice(**{'invoice':doc.name,'type': "PURCHASE",'cancel':1})

def purchase_invoice_save(doc,method=None):
    if not doc.shipping_address:
        doc.shipping_address = doc.billing_address
    if doc.import_supplier ==1:
        if doc.gst_import_supplier_gst_details:
            for item in doc.gst_import_supplier_gst_details:
                # if item.item_rate and not item.item_amount:
                #     item.item_amount=float(item.qty)*float(item.item_rate)
                if item.item_rate and item.item_amount and item.qty:
                    item.item_rate=float(item.item_amount)/float(item.qty)
    if doc.gst_category == "Unregistered":
        if doc.taxes_and_charges_added <= 0:
            doc.custom_non_gst = 1

def generate_random_id(length=12):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(secrets.choice(characters) for _ in range(length))
    return random_id

def group_id(doc,method=None):
    # pan_no=frappe.db.get_value("Customer",doc.customer,'pan')

    random_id = generate_random_id()
    # exist=frappe.db.exists("Generate Group ID", {"pan": doc.supplier_pan,"party_type":"Supplier"})
    # if exist:
    #     doc.custom_group_id=frappe.db.get_value("Generate Group ID",exist,"random_id")
    # else:
    new_doc=frappe.new_doc("Generate Group ID")
    new_doc.pan=doc.supplier_pan
    new_doc.pan_no=doc.supplier_pan
    new_doc.random_id = random_id
    new_doc.document_no=doc.name
    new_doc.party_type="Supplier"
    new_doc.dacument_type='Purchase Invoice'
    new_doc.save()
    doc.custom_group_id = random_id


def sales_group_id(doc,method=None):
    # pan_no=frappe.db.get_value("Customer",doc.customer,'pan')

    random_id = generate_random_id()
    # exist=frappe.db.exists("Generate Group ID", {"pan": doc.supplier_pan,"party_type":"Supplier"})
    # if exist:
    #     doc.custom_group_id=frappe.db.get_value("Generate Group ID",exist,"random_id")
    # else:
    new_doc=frappe.new_doc("Generate Group ID")
    new_doc.pan=frappe.get_doc("Customer",doc.customer,"pan")
    new_doc.pan_no=frappe.get_doc("Customer",doc.customer,"pan")
    new_doc.random_id = random_id
    new_doc.document_no=doc.name
    new_doc.party_type="Customer"
    new_doc.dacument_type='Sales Invoice'
    new_doc.save()
    doc.custom_group_id = random_id




    