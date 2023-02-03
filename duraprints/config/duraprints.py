from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Duraprints"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Compound Production",
                    "label": _("Compound Production"),
					"description": _("Complex & Compound Production"),
                    "onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Work Order",
                    "label": _("Work Order"),
					"description": _("Work Orders in Production"),
                    "onboard": 1,
				}
			]
		},
		{
			"label": _("Stock"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Item",
                    "label": _("Items"),
					"description": _("Items"),
                    "onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
                    "label": _("Stock Entry"),
					"description": _("Stock Entry"),
                    "onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Delivery Note",
                    "label": _("Delivery Challan"),
					"description": _("Delivery Challan"),
                    "onboard": 1,
				},
			]
		},
		{
			"label": _("Selling"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Customer",
                    "label": _("Customers"),
					"description": _("Customers"),
                    "onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Sales Order",
                    "label": _("Sales Order"),
					"description": _("All sales order"),
                    "onboard": 1,
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "report",
					"name": "Sales Summary by Customers",
                    "is_query_report": 	True,
					"doctype": "Sales Order"	
				},
				{
					"type": "report",
					"name": "Pending Delivery",
                    "is_query_report": 	True,
					"doctype": "Sales Order"	
				},
				{
					"type": "report",
					"name": "Delivery Summary",
                    "is_query_report": 	True,
					"doctype": "Delivery Note"	
				},
				{
					"type": "report",
					"name": "Production Summary by Customers",
                    "is_query_report": 	True,
					"doctype": "Delivery Note"	
				},
				{
					"type": "report",
					"name": "Item Stock And Purchase",
                    "is_query_report": 	True,
					"doctype":	"Stock Ledger Entry"	
				},
				{
					"type": "report",
					"name": "Customer Fabric Ledger",
                    "is_query_report": 	True,
					"doctype":	"Stock Ledger Entry"	
				},
				{
					"type": "report",
					"name": "SFL Fabric Stock And Purchase",
                    "is_query_report": 	True,
					"doctype":	"Stock Ledger Entry"	
				}
			]
		}
	]
