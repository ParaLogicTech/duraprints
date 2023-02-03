# Copyright (c) 2013, Betalogics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
import datetime
from frappe.utils import getdate
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from frappe import msgprint, _, scrub
from frappe.utils import getdate, nowdate, flt, cint, formatdate, cstr, now, time_diff_in_seconds


def execute(filters=None):
    return PendingDeliveryReport(filters).run()

class PendingDeliveryReport(object):
    def __init__(self, filters=None):
        super(PendingDeliveryReport, self).__init__()
        self.filters = frappe._dict(filters or {})

    def run(self):
        data = []
        self.columns = []
        
        data = self.get_sales_order_items(data)
        self.get_columns()

        return self.columns, data
        
    def get_sales_order_items(self, data):
        total = [0,0,0,0,0]
        sales_order_items_data = frappe.db.sql("""SELECT
            soi.parent, 
            so.customer, so.customer_code, so.po_no,
            so.transaction_date,
        
            soi.item_name, soi.description, soi.design_name, soi.warehouse,
            soi.fabric_gsm, soi.fabric_width, 
            soi.uom, soi.qty, soi.delivered_qty, soi.work_order_qty,
            soi.design_height, soi.design_gap,
            
            soi.fabric_material, soi.fabric_type
            
            FROM `tabSales Order Item` soi
            LEFT OUTER JOIN `tabSales Order` so ON so.name = soi.parent
            
            WHERE soi.docstatus = '1' AND so.docstatus = '1' AND so.delivery_status NOT IN ('Fully Delivered','Closed') {conditions}
            ORDER BY soi.parent DESC, soi.idx ASC"""\
        .format(conditions=self.get_conditions()), as_dict=1)
        for soi in sales_order_items_data:

            pending_production = soi.qty-soi.work_order_qty
            pending_delivery = soi.qty-soi.delivered_qty
                
            total[0] += soi.qty
            total[1] += soi.work_order_qty
            """total[2] += pending_production"""
            total[3] += soi.delivered_qty
            """total[4] += pending_delivery
            """        
            data.append([
                soi.transaction_date, soi.parent[4:13], soi.customer, soi.po_no, soi.design_name, soi.fabric_material, soi.fabric_type, soi.fabric_gsm, soi.fabric_width, soi.uom, '{:2,.2f}'.format(soi.qty), '{:2,.2f}'.format(soi.delivered_qty), '{:2,.2f}'.format(pending_delivery)
            ])
        data.append([
            'TOTAL', '', '', '', '', '', '', '', '', '', '{:2,.2f}'.format(total[0]), '{:2,.2f}'.format(total[1]), '{:2,.2f}'.format(total[3])
        ])
        return data

    def get_conditions(self):
        conditions = []
        if self.filters.get("from_date"):
            from_date = self.filters.get("from_date")
            to_date = self.filters.get("to_date")
            conditions.append("so.transaction_date BETWEEN '{0}' AND '{1}'". format(from_date, to_date))
        if self.filters.get("customer"):
            customer = self.filters.get("customer")
            conditions.append("so.customer = '{0}'". format(customer))
        if self.filters.get("po_no"):
            po_no = self.filters.get("po_no")
            conditions.append("so.po_no = '{0}'". format(po_no))
        if self.filters.get("sales_order"):
            sales_order = self.filters.get("sales_order")
            conditions.append("so.name = '{0}'". format(sales_order))
        if self.filters.get("fabric_material"):
            fabric_material = self.filters.get("fabric_material")
            conditions.append("soi.fabric_material = '{0}'". format(fabric_material))
        if self.filters.get("fabric_type"):
            fabric_type = self.filters.get("fabric_type")
            conditions.append("soi.fabric_type = '{0}'". format(fabric_type))
        return "and {}".format(" and ".join(conditions)) if conditions else ""

    def get_columns(self):

        self.columns = [
            {
                "label": _("Order Date"),
                "fieldname": "transaction_date",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("SO No."),
                "fieldname": "so_no",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Data",
                "width": 200
            },
            {
                "label": _("PO #"),
                "fieldname": "po_no",
                "fieldtype": "Data",
                "width": 100
            },
            {
                "label": _("Design Name"),
                "fieldname": "design_name",
                "fieldtype": "Data",
                "width": 250
            },
            {
                "label": _("Material"),
                "fieldname": "fabric_material",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Fabric Type"),
                "fieldname": "fabric_type",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("GSM"),
                "fieldname": "fabric_gsm",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Width"),
                "fieldname": "fabric_width",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Unit"),
                "fieldname": "uom",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Order Qty"),
                "fieldname": "order_qty",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Delivered Qty"),
                "fieldname": "delivered_qty",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Un Delivered Qty"),
                "fieldname": "undelivered_qty",
                "fieldtype": "Data",
                "width": 120
            }            
        ]
        
@frappe.whitelist()
def get_item_attribute_list():
    return frappe.get_all("Item Attribute Value", filters={"parent": ["IN", ("Type") ] }, fields=["attribute_value"], order_by="attribute_value")
    