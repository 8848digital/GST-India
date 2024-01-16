# Copyright (c) 2022, Resilient Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from gst_india.cleartax_integration.API.gst import bulk_purchase_gst, create_gst_invoice


class CleartaxSettings(Document):
	def tax_id(self,gstin):
		return frappe.get_value('Tax Entities',{'gstin':gstin,'parent':self.name},'entity_id')


@frappe.whitelist()
def irn_failed():
    sql  = """
                    SELECT 
                        COUNT(*) as count
                    FROM `tabSales Invoice` as si
                    LEFT JOIN `tabCleartax Api Log` as al ON si.name = al.document_name
                    AND al.api = 'GENERATE IRN'
					AND al.status = 'Failed'
                """ 
    return frappe.db.sql(sql,as_dict=1)[0]['count']


@frappe.whitelist()
def ewb_irn_failed():
    sql  = """
                    SELECT 
                        COUNT(*) as count
                    FROM `tabSales Invoice` as si
                    LEFT JOIN `tabCleartax Api Log` as al ON si.name = al.document_name
                    AND al.api = 'GENERATE EWB BY IRN'
					AND al.status = 'Failed'
                """ 
    return frappe.db.sql(sql,as_dict=1)[0]['count']

@frappe.whitelist()
def ewb_failed():
    sql  = """
                    SELECT 
                        COUNT(*) as count
                    FROM `tabDelivery Note` as si
                    LEFT JOIN `tabCleartax Api Log` as al ON si.name = al.document_name
                    AND al.api = 'GENERATE EWB WITHOUT IRN'
					AND al.status = 'Failed'
                """ 
    return frappe.db.sql(sql,as_dict=1)[0]['count']


def sales_gst_job(data):
    for i in data:
        frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'SALE'})
        # create_gst_invoice(**{'invoice':i.name,'type':'SALE'})

def purchase_gst_job(data):
    for i in data:
        frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'PURCHASE'})
        # create_gst_invoice(**{'invoice':i.name,'type':'PURCHASE'})


@frappe.whitelist()
def push_to_cleartax():
    doc = frappe.get_doc('Cleartax Settings')
    if doc.sales_invoices_from:
        sales_invoices = """
                            SELECT
                                log.document_name as name
                            FROM
                                `tabCleartax Api Log` as log
                            WHERE
                                log.status = 'Failed'
                            AND
                                log.api LIKE '%GENERATE GST SINV%'
                            LIMIT 100            
                            """
        sales_invoices = frappe.db.sql(sales_invoices,as_dict=1)
        frappe.log_error("sales_invoices",sales_invoices)
        frappe.logger('cleartax').exception(doc.sales_invoices_from)
        sales_gst_job(sales_invoices)
    if doc.purchase_invoices_from:
        purchase_invoices = """
                            SELECT
                                log.document_name as name
                            FROM
                                `tabCleartax Api Log` as log
                            WHERE
                                log.status = 'Failed'
                            AND
                                log.api LIKE '%GENERATE GST PINV%'

                            LIMIT 100            
                            """
        purchase_invoices = frappe.db.sql(purchase_invoices,as_dict=1)
        frappe.logger('cleartax').exception(doc.purchase_invoices_from)
        purchase_gst_job(purchase_invoices)


        
@frappe.whitelist()
def push_to_gst(**kwargs):
    if kwargs.get('sales_invoice'):
        sales_invoices = frappe.get_all('Sales Invoice',filters= [["posting_date","<=",kwargs.get('sales_invoice')],["gst_invoice",'=',0]])
        for i in sales_invoices:
            frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'SALE'})
    if kwargs.get('purchase_invoice'):
        purchase_invoices = frappe.get_all('Purchase Invoice',filters= [["posting_date","<=",kwargs.get('purchase_invoice')],["gst_invoice",'=',0]])
        for i in purchase_invoices:
            frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'PURCHASE'})

@frappe.whitelist()
def push_to_cleartax_scheduler():
    doc = frappe.get_doc('Cleartax Settings')
    if not doc.enable_scheduler:
        return
    si_list=[]
    if doc.sales_invoice:
        si_list=frappe.db.get_all("Sales Invoice",filters={"gst_invoice":1},fields=["name"])
    pi_list=[]
    if doc.purchase_invoice:
        pi_list=frappe.db.get_all("Purchase Invoice",filters={"gst_invoice":1},fields=["name"])
    if si_list:
        for i in si_list:
            frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'SALE'})
            # create_gst_invoice(**{'invoice':i.name,'type':'SALE'})
    if pi_list:
        for i in pi_list:
            frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'PURCHASE'})
            # create_gst_invoice(**{'invoice':i.name,'type':'PURCHASE'})



# @frappe.whitelist()
# def retry_failed_pi():
#     pi_list = frappe.get_all('Cleartax APi Log',filters=[['api','in',['GENERATE GST PINV','GENERATE GST CDN']],['status','Failed']],fields=['document_name'])
#     for i in pi_list:
#             frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.document_name,'type':'PURCHASE'})


# @frappe.whitelist()
# def retry_faield_si():
#     si_list = frappe.get_all('Cleartax APi Log',filters=[['api','in',['GENERATE GST SINV','GENERATE GST CDN']],['status','Failed']],fields=['document_name'])
#     for i in si_list:
#             frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.document_name,'type':'SALE'})



# @frappe.whitelist()
# def push_pi_gst():
#     purchase_invoices = frappe.get_all('Purchase Invoice',{'gst_invoice':1})
#     for i in purchase_invoices:
#             frappe.enqueue("gst_india.cleartax_integration.API.gst.create_gst_invoice",**{'invoice':i.name,'type':'PURCHASE'})