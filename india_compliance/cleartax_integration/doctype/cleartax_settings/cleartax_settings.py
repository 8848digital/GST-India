# Copyright (c) 2022, Resilient Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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