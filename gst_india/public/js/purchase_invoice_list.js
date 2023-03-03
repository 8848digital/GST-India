const erp_onl = frappe.listview_settings["Purchase Invoice"].onload;
frappe.listview_settings["Purchase Invoice"].onload = function (list_view) {
    if (erp_onl) {
        erp_onl(list_view);
    }
    list_view.page.add_action_item(__("GST Invoice"), function (event) {
        let selected = [];

        for (let check of event.view.cur_list.$checks) {
            selected.push(check.dataset.name);
        }
        frappe.call({
            method: "gst_india.API.gst.bulk_purchase_gst",
            args: {
                data: selected
            },
            type: "POST",
            callback: function(r) {
                frappe.msgprint("GST Invoices are scheduled to be genereated!")
                list_view.refresh();
                }
            })

    });

}