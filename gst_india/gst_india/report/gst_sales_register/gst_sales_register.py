# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from erpnext.accounts.report.sales_register.sales_register import _execute


def execute(filters=None):
    return _execute(
        filters,
        additional_table_columns=[
            dict(
                fieldtype="Data",
                label="Billing Address GSTIN",
                fieldname="billing_address_gstin",
                width=140,
            ),
            dict(
                fieldtype="Data",
                label="Company GSTIN",
                fieldname="company_gstin",
                width=120,
            ),
            dict(
                fieldtype="Data",
                label="Place of Supply",
                fieldname="place_of_supply",
                width=120,
            ),
            dict(
                fieldtype="Check",
                label="Is Reverse Charge",
                fieldname="is_reverse_charge",
                width=120,
            ),
            dict(
                fieldtype="Data",
                label="GST Category",
                fieldname="gst_category",
                width=120,
            ),
            dict(
                fieldtype="Check",
                label="Is Export With GST",
                fieldname="is_export_with_gst",
                width=120,
            ),
            dict(
                fieldtype="Data",
                label="E-Commerce GSTIN",
                fieldname="ecommerce_gstin",
                width=130,
            ),
        ],
        additional_query_columns=[
            "billing_address_gstin",
            "company_gstin",
            "place_of_supply",
            "is_reverse_charge",
            "gst_category",
            "is_export_with_gst",
            "ecommerce_gstin",
        ],
    )
