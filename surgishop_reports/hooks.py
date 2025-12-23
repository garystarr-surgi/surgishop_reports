from . import __version__ as app_version

app_name = "surgishop_reports"
app_title = "Surgishop Reports"
app_publisher = "Surgishop"
app_description = "Custom ERPNext reports for sales tracking and performance management"
app_email = "support@surgishop.com"
app_license = "MIT"

# Fixtures - Export these reports
fixtures = [
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                [
                    "Customer Item Purchase History",
                    "Daily EOD Sales Detail",
                    "Delivery Note Status",
                    "Item Tracking Report",
                    "Items on Hold",
                    "Outbound Shipping Status Report",
                    "Products by Specialty",
                    "Regional Dashboard",
                    "Sent Sales Invoices",
                    "Shipped Batch Expiry Report",
                    "Stock Status",
                    "Surgi General Ledger",
                    "Surgi Stock Balance",
                    "Temp Report",
                    "Warehouse Stock Status",
                ]
            ]
        ]
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/surgishop_reports/css/surgishop_reports.css"
# app_include_js = "/assets/surgishop_reports/js/surgishop_reports.js"

# include js, css files in header of web template
# web_include_css = "/assets/surgishop_reports/css/surgishop_reports.css"
# web_include_js = "/assets/surgishop_reports/js/surgishop_reports.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "surgishop_reports/public/scss/website"

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
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "surgishop_reports.utils.jinja_methods",
#	"filters": "surgishop_reports.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "surgishop_reports.install.before_install"
# after_install = "surgishop_reports.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "surgishop_reports.uninstall.before_uninstall"
# after_uninstall = "surgishop_reports.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "surgishop_reports.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"surgishop_reports.tasks.all"
#	],
#	"daily": [
#		"surgishop_reports.tasks.daily"
#	],
#	"hourly": [
#		"surgishop_reports.tasks.hourly"
#	],
#	"weekly": [
#		"surgishop_reports.tasks.weekly"
#	],
#	"monthly": [
#		"surgishop_reports.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "surgishop_reports.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "surgishop_reports.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "surgishop_reports.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["surgishop_reports.utils.before_request"]
# after_request = ["surgishop_reports.utils.after_request"]

# Job Events
# ----------
# before_job = ["surgishop_reports.utils.before_job"]
# after_job = ["surgishop_reports.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"partial": 1,
#	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"surgishop_reports.auth.validate"
# ]
