frappe.listview_settings['Purchase Invoice'] = {
    onload: function(listview) {
		listview.page.add_action_item(__("GST Invoice"), function (event) {
			let selected = [];

            for (let check of event.view.cur_list.$checks) {
                selected.push(check.dataset.name);
            }
            frappe.call({
                method: "india_compliance.cleartax_integration.API.gst.bulk_purchase_gst",
                args: {
                    data: selected
                },
                type: "POST",
                callback: function(r) {
                    frappe.msgprint("GST Invoices are scheduled to be genereated!")
                    listview.refresh();
                    }
                })

		});
    }}