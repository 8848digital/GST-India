# Copyright (c) 2022, Resilient Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from india_compliance.cleartax_integration.API.gst import bulk_purchase_gst


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


@frappe.whitelist()
def push_to_cleartax(**kwargs):
    if kwargs.get('sales_invoice'):
        sales_invoices = """
                            SELECT 
                                inv.name as name
                            FROM
                                `tabSales Invoice` as inv
                            WHERE name NOT IN
                                (SELECT log.document_name as name
                                FROM
                                    `tabCleartax Api Log` as log)
                            AND
                                inv.irn IS NOT NULL
                            AND inv.creation >= '%s'
                            """ %(kwargs.get('sales_invoice'))
        sales_invoices = frappe.db.sql(sales_invoices,as_dict=1)
        frappe.logger('cleartax').exception(kwargs)
        frappe.logger('cleartax').exception(sales_invoices)
        for i in sales_invoices:
            frappe.enqueue("india_compliance.cleartax_integration.API.irn.generate_irn",**{'invoice':i.name})
    if kwargs.get('purchase_invoice'):
        purchase_invoices = frappe.get_all("Purchase Invoice",filters=[['gst_invoice','=',0],['creation','>=',kwargs.get('purchase_invoice')]])
        frappe.logger('cleartax').exception(purchase_invoices)
        for i in purchase_invoices:
            frappe.enqueue("india_compliance.cleartax_integration.gst.create_gst_invoice",**{'invoice':i.name,'type':'PURCHASE'})
