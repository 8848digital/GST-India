frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		if (frm.selected_doc.docstatus == 1) {
		frappe.call({
			method: "india_compliance.cleartax_integration.API.irn.e_invoicing_enabled",
			args: {
				company: frm.selected_doc.company
			},
			callback: function (r) {
				console.log(r.message)
				if (r.message == true) {
					if (frm.selected_doc.irn_cancelled == false && frm.selected_doc.irn == undefined) {
						cur_frm.add_custom_button(__("IRN"), function () {
							frappe.call({
								method: "india_compliance.cleartax_integration.API.irn.generate_irn",
								args: {
									invoice: frm.selected_doc.name
								},
								callback: function (r) {
								//console.log(r.message)
									if (r.message.msg == 'success') {
										frappe.msgprint("IRN Created Successfully!")
										location.reload();
									}
									else {
										// frappe.msgprint(r.message.error, raise_exception=True)
										frappe.msgprint(r.message.error, raise_exception=True)
									}
								}
							});
						}, __('Create'));
						cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
					}
					else if (frm.selected_doc.irn_cancelled == false) {
						cur_frm.add_custom_button(__("Cancel IRN"), function () {
							let d = new frappe.ui.Dialog({
								title: "Cancel IRN",
								fields: [
									{
										label: 'Reason',
										fieldname: 'reason',
										fieldtype: "Select",
										options: ["Duplicate", "Data entry mistake", "Order Cancelled", "Others"]
									},
									{
										label: 'Remarks',
										fieldname: 'remarks',
										fieldtype: "Data"
									}
								],
								primary_action_label: 'Submit',
								primary_action(values) {

									frappe.call({
										method: "india_compliance.cleartax_integration.API.irn.cancel_irn",
										args: {
											data: values,
											invoice: frm.selected_doc.name
										},
										type: "POST",
										callback: function (r) {
											if (r.message.msg == 'success') {
												frappe.msgprint("IRN Cancelled Successfully!")
												location.reload();
											}
											else {
												// frappe.msgprint(r.message.error, raise_exception=True)
												frappe.msgprint(r.message.error, raise_exception=True)
											}
										}
									})
									d.hide();
								}
							})
							d.show();
						});
					}
					if(frm.selected_doc.irn){
					cur_frm.add_custom_button(__("Create E-way Bill by IRN"), function () {
						frappe.call({
							method: "india_compliance.cleartax_integration.API.ewb.generate_e_waybill_by_irn",
							args: {
								invoice: frm.selected_doc.name
							},
							callback: function (r) {
								if (r.message.msg == 'success') {
									frappe.msgprint("Eway Bill Created Successfully!")
									location.reload();
								}
								else {
									// frappe.msgprint(r.message.error, raise_exception=True)
									frappe.msgprint(r.message.error, raise_exception=True)
								}
							}
						});
					}, __('Create'));
					cur_frm.page.set_inner_btn_group_as_primary(__('Create'));}


					if (frm.selected_doc.eway_bill_cancelled == false && frm.selected_doc.ewaybill) {
						cur_frm.add_custom_button(__("Cancel E-way Bill"), function () {
							let d = new frappe.ui.Dialog({
								title: "Cancel Eway Bill",
								fields: [
									{
										label: 'Reason',
										fieldname: 'reason',
										fieldtype: "Select",
										options: ["DUPLICATE", "DATA_ENTRY_MISTAKE", "ORDER_CANCELLED", "OTHERS"]
									},
									{
										label: 'Remarks',
										fieldname: 'remarks',
										fieldtype: "Data"
									}
								],
								primary_action_label: 'Submit',
								primary_action(values) {

									frappe.call({
										method: "india_compliance.cleartax_integration.API.ewb.cancel_ewb",
										args: {
											data: values,
											invoice: frm.selected_doc.name
										},
										type: "POST",
										callback: function (r) {
											if (r.message.msg == 'success') {
												frappe.msgprint("Eway Bill Cancelled Successfully!")
												location.reload();
											}
											else {
												// frappe.msgprint(r.message.error, raise_exception=True)
												frappe.msgprint(r.message.error, raise_exception=True)
											}
										}
									})
									d.hide();
								}
							})
							d.show();
						});
					}
				}
				else {
					let button_name = ""
					if (frm.selected_doc.gst_invoice == false) {
						button_name = "GST Invoice"
					}
					else if((frm.selected_doc.is_return || frm.selected_doc.is_debit_note) && frm.selected_doc.cdn == 0){
						button_name = "Credit/Debit Note"
					}
						// GST Invoice Custom Button
						if(button_name != ""){
						cur_frm.add_custom_button(__(button_name), function () {
							frappe.call({
								method: "india_compliance.cleartax_integration.API.gst.create_gst_invoice",
								args: {
									invoice: frm.selected_doc.name,
									type: 'SALE'
								},
								callback: function (r) {
									if (r.message.msg == 'success') {
										frappe.msgprint("GST Invoice Created Successfully!")
										location.reload();
									}
									else {
										frappe.msgprint(r.message.error, raise_exception=True)
									}
								}
							});
						}, __('Create'));
						cur_frm.page.set_inner_btn_group_as_primary(__('Create'));}
					
				}
			}
		});



	}

	}
})