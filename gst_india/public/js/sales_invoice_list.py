frappe.listview_settings['Sales Invoice'] = {
    onload: function(listview) {
		listview.page.add_action_item(__("Generate IRN"), function (event) {
			let selected = [];

            for (let check of event.view.cur_list.$checks) {
                selected.push(check.dataset.name);
            }
            frappe.call({
                method: "gst_india.cleartax_integration.API.irn.bulk_irn",
                args: {
                    data: selected
                },
                type: "POST",
                callback: function(r) {
                    frappe.msgprint("IRN is being Generated!")
                    listview.refresh();
                    }
                })

		});
        listview.page.add_action_item(__("Generate EWB"), function (event) {
			let selected = [];

            for (let check of event.view.cur_list.$checks) {
                selected.push(check.dataset.name);
            }
            frappe.call({
                method: "gst_india.cleartax_integration.API.ewb.bulk_ewb",
                args: {
                    data: selected
                },
                type: "POST",
                callback: function(r) {
                    frappe.msgprint("EWB is being Generated!")
                    listview.refresh();
                    }
                })

		});
    }
}