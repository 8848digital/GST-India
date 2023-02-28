const erp_onl = frappe.listview_settings["Delivery Note"].onload;
frappe.listview_settings["Delivery Note"].onload = function (list_view) {
    if (erp_onl) {
        erp_onl(list_view);
    }
        list_view.page.add_action_item(__("Generate EWB"), function (event) {
			let selected = [];

            for (let check of event.view.cur_list.$checks) {
                selected.push(check.dataset.name);
            }
            frappe.call({
                method: "gst_india.cleartax_integration.API.ewb.bulk_ewb_dn",
                args: {
                    data: selected
                },
                type: "POST",
                callback: function(r) {
                    frappe.msgprint("EWB is being Generated!")
                    list_view.refresh();
                    }
                })

		});
    }

