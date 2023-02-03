# Copyright (c) 2013, Betalogics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.utils import getdate
from datetime import date, timedelta
from frappe import msgprint, _
from frappe.utils import flt
# import frappe

def execute(filters=None):
    data = []
    total = [0,0]
    columns = get_columns(filters)
    data = get_delivery_details(filters, data, total)

    if filters.get("design_count") and int(filters.get("design_count")) > 0:
        data = get_top_designs(filters, data)
    return columns, data

def get_delivery_details(filters, data, total):

    customers = frappe.db.sql("""SELECT
        so.customer, so.contact_display, so.contact_mobile, COUNT(*) as order_count, SUM(so.total_qty)as order_qty 
        FROM `tabSales Order` so
        WHERE 
        so.docstatus = 1 {conditions}
        GROUP BY so.customer
        ORDER BY order_qty DESC """\
        .format(conditions=get_conditions(filters)), as_list=1)
    for ti in customers:
        customer = ti[0]
        customer_name = ti[1]
        customer_contact = ti[2]
        order_count = ti[3]
        order_qty = ti[4]
        
        total[0] += order_count
        total[1] += order_qty
        data.append([
            customer, customer_name, customer_contact, '{:0,.0f}'.format(order_count), '{:2,.2f}'.format(order_qty)
        ])
    data.append([
            'TOTAL', '', '', '{:0,.0f}'.format(total[0]), '{:2,.2f}'.format(total[1])
        ])
    return data

def get_top_designs(filters, data):

    designs = frappe.db.sql("""
        SELECT
            soi.item_code,
            sum(soi.qty) as total_qty,
            i.image
        FROM
        `tabSales Order Item` soi 
        LEFT OUTER JOIN `tabItem` i ON soi.item_code = i.item_code	
        WHERE soi.parent IN (
                SELECT name FROM `tabSales Order` so WHERE so.docstatus = 1 {conditions}
        )
        GROUP BY soi.item_code
        ORDER BY total_qty DESC 
        limit 0, {design_limit}"""\
        .format(conditions=get_conditions(filters), design_limit=filters.get("design_count")), as_list=1)
    for ti in designs:
        design_code = ti[0]
        top_qty = ti[1]
        image = ti[2]
        data.append([
            "TOP DESIGN", design_code, '', image, top_qty
        ])
    return data


def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")
        conditions.append("so.transaction_date BETWEEN '{0}' AND '{1}'". format(from_date, to_date))

    return "AND {}".format(" AND ".join(conditions)) if conditions else ""


def get_columns(filters):
    """return columns based on filters"""

    columns = [
        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Contact Person"),
            "fieldname": "contact_person",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Mobile Number"),
            "fieldname": "contact_mobile",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Orders"),
            "fieldname": "order_count",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Qty in Meters"),
            "fieldname": "qty_in_meters",
            "fieldtype": "Data",
            "width": 200
        }
    ]
    return columns