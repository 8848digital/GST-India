// Copyright (c) 2022, Resilient Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cleartax Settings', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__("PUSH TO CLEARTAX"), function () {
			frappe.call({
				method: "india_compliance.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_to_cleartax",
				args: {
					purchase_invoice: frm.selected_doc.purchase_invoices_from,
					sales_invoice: frm.selected_doc.sales_invoices_from
				},
				callback: function (r) {
				//console.log(r.message)
					if (r.message.msg == 'success') {
						frappe.msgprint("IRN Created Successfully!")
						location.reload();
					}
					else {
						// frappe.msgprint(r.message.error)
						frappe.msgprint(r.message.error)
					}
				}
			});
		});

	}
});
