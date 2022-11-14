# Copyright (c) 2022, 8848 Digital LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DeliveryNotePartB(Document):
	def on_submit(self):
		try:
			frappe.db.set_value('Delivery Note',self.delivery_note,'lr_no',self.lr_no)
			frappe.db.set_value('Delivery Note',self.delivery_note,'lr_date',self.lr_date)
			frappe.db.set_value('Delivery Note',self.delivery_note,'vehicle_no',self.vehicle_no)
			frappe.db.set_value('Delivery Note',self.delivery_note,'distance',self.distance)
			frappe.db.set_value('Delivery Note',self.delivery_note,'mode_of_transport',self.mode_of_transport)
		except Exception as e:
			frappe.logger('cleartax').exception(e)
