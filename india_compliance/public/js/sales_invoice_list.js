const erpnext_onload = frappe.listview_settings["Sales Invoice"].onload;
frappe.listview_settings["Sales Invoice"].onload = function (list_view) {
    if (erpnext_onload) {
        erpnext_onload(list_view);
    }
    list_view.page.add_action_item(__("Generate IRN"), function (event) {
        let selected = [];

        for (let check of event.view.cur_list.$checks) {
            selected.push(check.dataset.name);
        }
        frappe.call({
            method: "india_compliance.cleartax_integration.API.irn.bulk_irn",
            args: {
                data: selected
            },
            type: "POST",
            callback: function(r) {
                frappe.msgprint("IRN is being Generated!")
                list_view.refresh();
                }
            })

    });
    list_view.page.add_action_item(__("Generate EWB"), function (event) {
        let selected = [];

        for (let check of event.view.cur_list.$checks) {
            selected.push(check.dataset.name);
        }
        frappe.call({
            method: "india_compliance.cleartax_integration.API.ewb.bulk_ewb",
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

};
