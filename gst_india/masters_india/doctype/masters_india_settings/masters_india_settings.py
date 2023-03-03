# Copyright (c) 2023, 8848 Digital LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class MastersIndiaSettings(Document):

	def validate(self):
		if frappe.db.get_single_value('Cleartax Settings','enable'):
			frappe.throw("Please Disable Cleartax Integration! You can enable either Cleartax Or Masters India.")


	def authenticate(self):
		url = "https://client.mastersindia.co/oauth/access_token"
		if self.sandbox:
			payload = {
					"username":self.sandbox_username,
					"password": self.get_password('sandbox_password'),
					"client_id":self.get_password('sandbox_client_id'),
					"client_secret":self.get_password('sandbox_client_secret'),
					"grant_type":"password"
					}
		else:
			payload = {
						"username":self.production_username,
						"password": self.get_password('production_password'),
						"client_id":self.get_password('production_client_id'),
						"client_secret":self.get_password('production_client_secret'),
						"grant_type":"password"
						}
		response = requests.request("POST", url, data=payload) 
		response = response.json()
		if response.get('access_token'):
			self.auth_token = response.get('access_token')
			self.save()



@frappe.whitelist()
def update_access_token():
	doc = frappe.get_doc("Masters India Settings")
	if doc.enable:
		doc.authenticate()