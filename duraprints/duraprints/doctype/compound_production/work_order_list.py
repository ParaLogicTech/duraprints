from __future__ import unicode_literals
import frappe
import json
from frappe import _

@frappe.whitelist()
def get_work_order(name):
    work_order = frappe.get_doc("Work Order", name)
    data = {
        "name": work_order.name,
        "qty": work_order.qty,
        "sales_order": work_order.sales_order,
        "status": work_order.status
    }
    return data

@frappe.whitelist()
def get_work_order_list_details(names):
    data = []
    
    names = json.loads(names)
    filters = {
        "name" : [ 
            'in', (names)
        ]
    }
    """return filters"""
    work_orders = frappe.get_all("Work Order", filters= filters, fields=["name","qty","sales_order","status"], order_by="name")
    for wo in work_orders:
        data.append({
            "name": wo.name,
            "qty": wo.qty,
            "sales_order": wo.sales_order,
            "status": wo.status
        })
    return data

@frappe.whitelist()
def get_sales_order(sales_order):
    sales_order = frappe.get_doc("Sales Order", sales_order)
    data = {
        "name": sales_order.name,
        "transaction_date": sales_order.transaction_date,
        "delivery_date": sales_order.delivery_date
    }
    return data