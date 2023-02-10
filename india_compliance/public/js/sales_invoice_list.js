const erp_onl = frappe.listview_settings["Sales Invoice"].onload;
frappe.listview_settings["Sales Invoice"].onload = function (list_view) {
    if (erp_onl) {
        erp_onl(list_view);
    }
    list_view.page.add_action_item(__("Generate IRN"), function (event) {
        const docnames = list_view.get_checked_items(true);
        frappe.call({
            method: "india_compliance.cleartax_integration.API.irn.bulk_irn",
            args: {
                data: docnames
            },
            type: "POST",
            callback: function(r) {
                frappe.msgprint("IRN is being Generated!")
                list_view.refresh();
                }
            })

    });
    list_view.page.add_action_item(__("Generate EWB"), function (event) {
        const docnames = list_view.get_checked_items(true);
        frappe.call({
            method: "india_compliance.cleartax_integration.API.ewb.bulk_ewb",
            args: {
                data: docnames
            },
            type: "POST",
            callback: function(r) {
                frappe.msgprint("EWB is being Generated!")
                list_view.refresh();
                }
            })

    });

};
