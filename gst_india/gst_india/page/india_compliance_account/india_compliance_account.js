frappe.pages["india-compliance-account"].on_page_load = async function (wrapper) {
    await frappe.require([
        "gst_india_account.bundle.js",
        "gst_india_account.bundle.css",
    ]);

    new ic.pages.IndiaComplianceAccountPage(wrapper);
};
