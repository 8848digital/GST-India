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
						frappe.msgprint("Documents Scheduled to be processed!")
					}
			});
		});
		cur_frm.add_custom_button(__("PUSH GST"), function () {
			frappe.call({
				method: "india_compliance.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_to_gst",
				args: {
					purchase_invoice: frm.selected_doc.purchase_invoices_from,
					sales_invoice: frm.selected_doc.sales_invoices_from
				},
				callback: function (r) {
						frappe.msgprint("Documents Scheduled to be processed!")
					}
			});
		});

	}
});
