# Copyright (c) 2022, 8848 Digital LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DeliveryNotePartB(Document):
	def on_submit(self):
		try:
			dn = frappe.get_doc('Delivery Note',self.delivery_note)
			dn.lr_no = self.lr_no
			dn.lr_date = self.lr_date
			dn.vehicle_no = self.vehicle_no
			dn.distance = self.distance
			dn.mode_of_transport = self.mode_of_transport
		except Exception as e:
			frappe.logger('cleartax').exception(e)
