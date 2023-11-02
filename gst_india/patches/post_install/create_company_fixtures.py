import frappe

from gst_india.gst_india.overrides.company import make_default_tax_templates
from gst_india.income_tax_india.overrides.company import create_company_fixtures

"""
This patch is used to create company fixtures for Indian Companies created before installing India Compliance.
"""


def execute():
    company_list = frappe.get_all("Company", filters={"country": "India"}, pluck="name")
    for company in company_list:
        # Income Tax fixtures
        if not frappe.db.exists(
            "Account", {"company": company, "account_name": "TDS Payable"}
        ):
            create_company_fixtures(company)

        # GST fixtures
        if not frappe.db.exists("GST Account", {"company": company}):
            pass
            # make_default_tax_templates(company)
