# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "duraprints"
app_title = "Duraprints"
app_publisher = "Betalogics"
app_description = "App to automate complex order booking and production cycle"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "avaiskhatri@betalogics.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/duraprints/css/duraprints.css"
# app_include_js = "/assets/duraprints/js/duraprints.js"

# include js, css files in header of web template
# web_include_css = "/assets/duraprints/css/duraprints.css"
# web_include_js = "/assets/duraprints/js/duraprints.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {
  "Work Order" : [
    "duraprints/duraprints/templates/pages/work_order_list.js"
  ]
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "duraprints.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "duraprints.install.before_install"
# after_install = "duraprints.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "duraprints.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"duraprints.tasks.all"
# 	],
# 	"daily": [
# 		"duraprints.tasks.daily"
# 	],
# 	"hourly": [
# 		"duraprints.tasks.hourly"
# 	],
# 	"weekly": [
# 		"duraprints.tasks.weekly"
# 	]
# 	"monthly": [
# 		"duraprints.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "duraprints.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "duraprints.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "duraprints.task.get_dashboard_data"
# }


fixtures = [
       {
         "dt": "Custom Field", 
         "filters":[["name", "in", [
             'Item-design_properties','Item-design_height','Item-design_width',
             'Item-design_column_1',
             'Item-design_gap','Item-design_uom',
             'Item-design_column_2',
             'Item-design_notes','Item-design_name',
             'Item-fabric_properties',
             'Item-fabric_wastage',
             'Item-fabric_properties_column_2',
             'Item-fabric_gsm','Item-fabric_width','Item-fabric_material',
             'Item-fabric_properties_column_1',
             'Item-fabric_source','Item-fabric_type','Item-fabric_construction',
             'Item-fabric_name',
             'Item-compound_production_id',
             'Customer-customer_code','Customer-customer_abbreviation',
             'Customer-cnic','Customer-ntn','Customer-strn','Supplier-cnic','Supplier-ntn','Supplier-strn',
             'Sales Order-reference',
             'Sales Order-customer_code',
             'Sales Order-default_wastage','Sales Order-default_wastage_type'
             'Sales Order-wastage_column_1','Sales Order-master_rate',
             'Sales Order-wastage_section_break',
             'Sales Order-default_uom',
             'Sales Order Item-fabric_quantity','Sales Order Item-wastage_type',
             'Sales Order Item-fabric_width','Sales Order Item-fabric_gsm','Sales Order Item-fabric_material',
             'Sales Order Item-fabric_source','Sales Order Item-fabric_type',
             'Sales Order Item-fabric_properties_column_1',
             'Sales Order Item-fabric_properties_column_2',
             'Sales Order Item-fabric_wastage',
             'Sales Order Item-fabric_name',
             'Sales Order Item-design_height','Sales Order Item-design_width',
             'Sales Order Item-design_uom','Sales Order Item-design_notes',
             'Sales Order Item-design_gap','Sales Order Item-design_name',
             'Sales Order Item-default_wastage_type',
             'Delivery Note-customer_code',
             'Delivery Note Item-design_name',
             'Delivery Note Item-fabric_gsm','Delivery Note Item-fabric_column_2',
             'Delivery Note Item-fabric_construction','Delivery Note Item-fabric_width',
             'Delivery Note Item-fabric_type',
             'Delivery Note Item-fabric_name',
             'Delivery Note Item-fabric_material',
             'Delivery Note Item-fabric_column_1',
             'Delivery Note Item-package_no',
             'Delivery Note Item-design_height','Delivery Note Item-design_gap',
             'Delivery Note Item-unprinted_fabric','Delivery Note Item-is_raw_fabric',
             'Delivery Note Item-package_quantity',
             'Sales Invoice-cnic','Sales Invoice-ntn','Sales Invoice-strn',
             'Sales Invoice-customer_code',
             'Work Order-is_sample'
             ]]]
      },
      {
        "dt": "Custom Script", 
        "filters": [["name", "in", [
                "Item-Client",
                "Sales Order-Client"
                ]]]
      },
      {
        "dt": "Print Format", 
        "filters": [["name", "in", [
                "duraprints Sale Order",
                "duraprints Sale Order - Itemwise Tax"
                
                "Internal Production Order - duraprints",
                "Internal Production Order v1- duraprints",
                
                "Print for work order","Standard for Work Order",
                
                "duraprints Delivery Challan",
                "duraprints Sample Delivery Challan",
                
                ]]]
      },
      {
        "dt": "Report",
        "filters": [["name", "in", [
          "Item Stock And Purchase",
          "SFL Fabric Stock And Purchase",
          "Customer Fabric Ledger",
          "Sales Summary by Customers"
          "Delivery Summary",
          "Pending Delivery",
          "Production Summary by Customers"
        ]]]
      }
]
