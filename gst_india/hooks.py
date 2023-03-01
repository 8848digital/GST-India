from . import __version__ as app_version

app_name = "gst_india"
app_title = "GST India"
app_publisher = "8848 Digital LLP"
app_description = "ERPNext app to simplify compliance with Indian Rules and Regulations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "contact@8848digital.com"
app_license = "MIT"
required_apps = ["erpnext"]

after_install = "gst_india.install.after_install"
before_tests = "gst_india.tests.before_tests"
boot_session = "gst_india.boot.set_bootinfo"

app_include_js = "gst_india.bundle.js"

doctype_js = {
    "Address": "gst_india/client_scripts/address.js",
    "Company": "gst_india/client_scripts/company.js",
    "Customer": "gst_india/client_scripts/customer.js",
    "Delivery Note": [
         "public/js/delivery_note_doctype.js",
#        "public/js/delivery_note_doctype.js",
        "gst_india/client_scripts/e_waybill_actions.js",
#        "gst_india/client_scripts/delivery_note.js",
    ],
    "Item": "gst_india/client_scripts/item.js",
    "Journal Entry": "gst_india/client_scripts/journal_entry.js",
    "Payment Entry": "gst_india/client_scripts/payment_entry.js",
    "Sales Invoice": [
         "public/js/sales_invoice_doctype.js",
#        "public/js/sales_invoice_doctype.js",
        "gst_india/client_scripts/e_waybill_actions.js",
#        "gst_india/client_scripts/e_invoice_actions.js",
#        "gst_india/client_scripts/sales_invoice.js",
    ],
    "Supplier": "gst_india/client_scripts/supplier.js",
    "Purchase Invoice" : "public/js/purchase_invoice_doctype.js"
}
doctype_list_js = {
    "Sales Invoice": [
        "public/js/sales_invoice_list.js",
        "gst_india/client_scripts/e_waybill_actions.js",
        "gst_india/client_scripts/sales_invoice_list.js",
    ],
    "Purchase Invoice": "public/js/purchase_invoice_list.js",
    "Delivery Note": "public/js/delivery_note_list.js"
}

doc_events = {
    "Address": {
        "validate": [
            "gst_india.gst_india.overrides.address.validate",
            "gst_india.gst_india.overrides.party.set_docs_with_previous_gstin",
        ],
    },
    "Company": {
        "on_trash": "gst_india.gst_india.overrides.company.delete_gst_settings_for_company",
        "on_update": [
            "gst_india.income_tax_india.overrides.company.make_company_fixtures",
            "gst_india.gst_india.overrides.company.create_default_tax_templates",
        ],
        "validate": "gst_india.gst_india.overrides.party.validate_party",
    },
    "Customer": {
        "validate": "gst_india.gst_india.overrides.party.validate_party",
        "after_insert": (
            "gst_india.gst_india.overrides.party.create_primary_address"
        ),
    },
    "Delivery Note": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
        "before_submit": "gst_india.public.py.delivery_note_doctype.delivery_note_submit",
        "before_save": "gst_india.public.py.delivery_note_doctype.delivery_note_save",
        "before_cancel": "gst_india.public.py.delivery_note_doctype.delivery_note_cancel"
    },
    "Item": {"validate": "gst_india.gst_india.overrides.item.validate_hsn_code"},
    "Payment Entry": {
        "validate": (
            "gst_india.gst_india.overrides.payment_entry.update_place_of_supply"
        )
    },
    "Purchase Invoice": {
        "validate": "gst_india.gst_india.overrides.purchase_invoice.validate",
        "before_submit": "gst_india.public.py.purchase_invoice_doctype.purchase_invoice_submit",
        "before_cancel": "gst_india.public.py.purchase_invoice_doctype.purchase_invoice_cancel",
        "before_save": "gst_india.public.py.purchase_invoice_doctype.purchase_invoice_save"
    },
    "Purchase Order": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
    },
    "Purchase Receipt": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
    },
    "Sales Invoice": {
        "onload": "gst_india.gst_india.overrides.sales_invoice.onload",
        "validate": "gst_india.gst_india.overrides.sales_invoice.validate",
        "on_submit": "gst_india.gst_india.overrides.sales_invoice.on_submit", 
        "before_submit":"gst_india.public.py.sales_invoice_doctype.sales_invoice_submit",
        "before_cancel": "gst_india.public.py.sales_invoice_doctype.sales_invoice_cancel",
        "before_save": "gst_india.public.py.sales_invoice_doctype.sales_invoice_save"
    },
    "Sales Order": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
    },
    "Supplier": {
        "validate": [
            "gst_india.gst_india.overrides.supplier.update_transporter_gstin",
            "gst_india.gst_india.overrides.party.validate_party",
        ],
        "after_insert": (
            "gst_india.gst_india.overrides.party.create_primary_address"
        ),
    },
    "Tax Category": {
        "validate": "gst_india.gst_india.overrides.tax_category.validate"
    },
    "POS Invoice": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
    },
    "Quotation": {
        "validate": (
            "gst_india.gst_india.overrides.transaction.validate_transaction"
        ),
    },
}


regional_overrides = {
    "India": {
        "erpnext.controllers.taxes_and_totals.get_itemised_tax_breakup_header": "gst_india.gst_india.overrides.transaction.get_itemised_tax_breakup_header",
        "erpnext.controllers.taxes_and_totals.get_itemised_tax_breakup_data": (
            "gst_india.gst_india.utils.get_itemised_tax_breakup_data"
        ),
        "erpnext.controllers.taxes_and_totals.get_regional_round_off_accounts": "gst_india.gst_india.overrides.transaction.get_regional_round_off_accounts",
        "erpnext.accounts.party.get_regional_address_details": (
            "gst_india.gst_india.overrides.transaction.update_party_details"
        ),
        "erpnext.stock.doctype.item.item.set_item_tax_from_hsn_code": "gst_india.gst_india.overrides.transaction.set_item_tax_from_hsn_code",
        "erpnext.assets.doctype.asset.asset.get_depreciation_amount": (
            "gst_india.income_tax_india.overrides.asset.get_depreciation_amount"
        ),
    }
}

jinja = {
    "methods": [
        "gst_india.gst_india.utils.get_state",
        "gst_india.gst_india.utils.jinja.add_spacing",
        "gst_india.gst_india.utils.jinja.get_supply_type",
        "gst_india.gst_india.utils.jinja.get_sub_supply_type",
        "gst_india.gst_india.utils.jinja.get_e_waybill_qr_code",
        "gst_india.gst_india.utils.jinja.get_qr_code",
        "gst_india.gst_india.utils.jinja.get_transport_type",
        "gst_india.gst_india.utils.jinja.get_transport_mode",
        "gst_india.gst_india.utils.jinja.get_ewaybill_barcode",
        "gst_india.gst_india.utils.jinja.get_non_zero_fields",
    ],
}

override_doctype_dashboards = {
    "Sales Invoice": (
        "gst_india.gst_india.overrides.sales_invoice.get_dashboard_data"
    ),
    "Delivery Note": (
        "gst_india.gst_india.overrides.delivery_note.get_dashboard_data"
    ),
}
fixtures = [
        {
                "dt":"Custom Field",
                "filters":[["name","in",["Sales Invoice","Sales Invoice Item","Packed Item","Purchase Invoice","Purchase Invoice Item","Delivery Note","Delivery Note Item"]
                                                                        ]]
        }
]
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gst_india/css/gst_india.css"

# include js, css files in header of web template
# web_include_css = "/assets/gst_india/css/gst_india.css"
# web_include_js = "/assets/gst_india/js/gst_india.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gst_india/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gst_india.utils.jinja_methods",
# 	"filters": "gst_india.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gst_india.install.before_install"

# Uninstallation
# ------------

# before_uninstall = "gst_india.uninstall.before_uninstall"
# after_uninstall = "gst_india.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gst_india.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"hourly_long":["gst_india.cleartax_integration.doctype.cleartax_settings.cleartax_settings.push_to_cleartax"]
}

# Testing
# -------

# before_tests = "gst_india.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gst_india.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gst_india.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gst_india.auth.validate"
# ]
