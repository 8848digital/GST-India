// Copyright (c) 2022, Resilient Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cleartax Settings', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__("PUSH TO CLEARTAX"), function () {
			frappe.call({
				method: "gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_to_cleartax",
				args: {
					purchase_invoice: frm.selected_doc.purchase_invoices_from,
					sales_invoice: frm.selected_doc.sales_invoices_from
				},
				callback: function (r) {
						frappe.msgprint("Documents Scheduled to be processed!")
					}
			});
		});
		// cur_frm.add_custom_button(__("SYNC SINV GST"), function () {
		// 	frappe.call({
		// 		method: "gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_to_gst",
		// 		callback: function (r) {
		// 				frappe.msgprint("Documents Scheduled to be processed!")
		// 			}
		// 	});
		// }, __('GST'));
		// cur_frm.add_custom_button(__("Retry Failed PINV"), function () {
		// 	frappe.call({
		// 		method: "gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.retry_failed_pi",
		// 		callback: function (r) {
		// 				frappe.msgprint("Documents Scheduled to be processed!")
		// 			}
		// 	});
		// }, __('GST'));
		// cur_frm.add_custom_button(__("Retry Failed SINV"), function () {
		// 	frappe.call({
		// 		method: "gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.retry_faield_si",
		// 		callback: function (r) {
		// 				frappe.msgprint("Documents Scheduled to be processed!")
		// 			}
		// 	});
		// }, __('GST'));
		// cur_frm.add_custom_button(__("Sync PINV ID"), function () {
		// 	frappe.call({
		// 		method: "gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_pi_gst",
		// 		callback: function (r) {
		// 				frappe.msgprint("Documents Scheduled to be processed!")
		// 			}
		// 	});
		// }, __('GST'));

	}
});
