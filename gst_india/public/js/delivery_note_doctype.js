frappe.ui.form.on('Delivery Note', {
	refresh(frm) {
		if (frm.selected_doc.docstatus == 1 || frm.selected_doc.is_return == 1){
		// Eway - Bill generation
		var enabled = 0
		if (frm.selected_doc.ewaybill == undefined || frm.selected_doc.ewaybill == '') {
			if (frm.selected_doc.eway_bill_cancelled == 0) {
				enabled = 1
			}
		}
		else if (frm.selected_doc.is_return == 1) {
			enabled = 1
		}
		if (enabled == 1) {
			cur_frm.add_custom_button(__("E-Way Bill"), function () {
				frappe.call({
					method: "gst_india.cleartax_integration.API.ewb.ewb_without_irn",
					args: {
						delivery_note: frm.selected_doc.name
					},
					callback: function (r) {
						if (r.message.msg == 'success') {
							frappe.msgprint("Eway Bill Created Successfully!")
							location.reload();
						}
						else {
							frappe.msgprint(r.message.error)
						}
					}
				});
			}, __('Create'));
			cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
		else if (frm.selected_doc.eway_bill_cancelled == false && frm.selected_doc.ewaybill) {
			cur_frm.add_custom_button(__("Extend EWB"), function () {
				let d1 = new frappe.ui.Dialog({
					title: "Extend Ewaybill",
					fields: [
						{
							label: 'Reason',
							fieldname: 'reason',
							fieldtype: "Select",
							options: ["NATURAL_CALAMITY", "TRANSSHIPMENT", "OTHERS", "ACCIDENT", "LAW_ORDER_SITUATION"]
						},
						{
							label: 'Consignment Status',
							fieldname: 'status',
							fieldtype: "Select",
							options: ["MOVEMENT","TRANSIT"]
						},
						{
							label: 'Transit Type',
							fieldname: 'type',
							fieldtype: "Select",
							depends_on: "eval:doc.status=='TRANSIT'",
							options: ["ROAD",
							"WAREHOUSE",
							"OTHERS",
							"NONE"]
						},
						{
							label: 'Remarks',
							fieldname: 'remarks',
							fieldtype: "Data"
						}
					],
					primary_action_label: 'Extend',
					primary_action(values) {

						frappe.call({
							method: "gst_india.cleartax_integration.API.ewb.extend_ewb",
							args: {
								data: values,
								delivery_note: frm.selected_doc.name
							},
							type: "POST",
							callback: function (r) {
								if (r.message.msg == 'Success') {
									frappe.msgprint("Eway Bill Extended Successfully!")
									location.reload();
								}
								else {
									frappe.msgprint(r.message.error)
								}
							}
						})
						d1.hide();
					}
				})
				d1.show();
			});
			if (frm.selected_doc.update_partb == 0) {
				cur_frm.add_custom_button(__("Update PARTB"), function () {
					let d1 = new frappe.ui.Dialog({
						title: "Update Part B",
						fields: [
							{
								label: 'Reason',
								fieldname: 'reason',
								fieldtype: "Select",
								options: ["BREAKDOWN", "TRANSSHIPMENT", "FIRST_TIME", "OTHERS"]
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
								method: "gst_india.cleartax_integration.API.ewb.update_ewb_partb",
								args: {
									data: values,
									delivery_note: frm.selected_doc.name
								},
								type: "POST",
								callback: function (r) {
									if (r.message.msg == 'success') {
										frappe.msgprint("Eway Bill Updated Successfully!")
										location.reload();
									}
									else {
										frappe.msgprint(r.message.error)
									}
								}
							})
							d.hide();
						}
					})
					d1.show();
				});

			}
			cur_frm.add_custom_button(__("Cancel E-Way Bill"), function () {
				let d = new frappe.ui.Dialog({
					title: "Cancel E-Way Bill",
					fields: [
						{
							label: 'Reason',
							fieldname: 'reason',
							fieldtype: "Select",
							options: ["DATA_ENTRY_MISTAKE", "ORDER_CANCELLED", "DUPLICATE", "OTHERS"]
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
							method: "gst_india.cleartax_integration.API.ewb.cancel_ewb_dn",
							args: {
								data: values,
								delivery_note: frm.selected_doc.name
							},
							type: "POST",
							callback: function (r) {
								if (r.message.msg == 'success') {
									frappe.msgprint("Eway Bill Cancelled Successfully!")
									location.reload();
								}
								else {
									frappe.msgprint(r.message.error)
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
	}
})