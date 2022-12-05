frappe.listview_settings['Delivery Note'] = {
    onload: function(listview) {
        listview.page.add_action_item(__("Generate EWB"), function (event) {
			let selected = [];

            for (let check of event.view.cur_list.$checks) {
                selected.push(check.dataset.name);
            }
            frappe.call({
                method: "india_compliance.cleartax_integration.API.ewb.bulk_ewb_dn",
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
