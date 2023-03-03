frappe.ui.form.on('Purchase Invoice', {
	refresh(frm) {
		if (frm.selected_doc.docstatus == 1) {
					let button_name = ""
					if (frm.selected_doc.gst_invoice == false) {
						button_name = "GST Invoice"
					}
					else if((frm.selected_doc.is_return) && frm.selected_doc.cdn == 0){
						button_name = "Credit/Debit Note"
					}
						// GST Invoice Custom Button
						if(button_name != ""){
						cur_frm.add_custom_button(__(button_name), function () {
							frappe.call({
								method: "gst_india.API.gst.create_gst_invoice",
								args: {
									invoice: frm.selected_doc.name,
									type: 'PURCHASE'
								},
								callback: function (r) {
									if (r.message.msg == 'success') {
										frappe.msgprint("GST Invoice Created Successfully!")
										location.reload();
									}
									else {
										frappe.msgprint(r.message.error)
									}
								}
							});
						}, __('Create'));
						cur_frm.page.set_inner_btn_group_as_primary(__('Create'));}

					}


	}
})