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
    return DeliverySummary(filters).run()

class DeliverySummary(object):
    def __init__(self, filters=None):
        super(DeliverySummary, self).__init__()
        self.filters = frappe._dict(filters or {})

    def run(self):
        data = []
        self.columns = []
        
        data = self.get_delivery_items(data)
        self.get_columns()

        return self.columns, data
        
    def get_delivery_items(self, data):
        total = [0,0,0,0]
        delivery_items_data = frappe.db.sql("""SELECT
            dni.parent, 
            dn.customer, dn.customer_code, dn.po_no,
            dn.posting_date, dn.posting_time,
        
            dni.item_name, dni.description, dni.design_name, dni.warehouse,
            dni.fabric_gsm, dni.fabric_width, 
            dni.uom, dni.qty, dni.package_no, dni.package_quantity,
            dni.design_height, dni.design_gap,
            
            dni.fabric_material,dni.fabric_type, dni.is_raw_fabric
            
            FROM `tabDelivery Note Item` dni
            LEFT OUTER JOIN `tabDelivery Note` dn ON dn.name = dni.parent
            
            WHERE dni.docstatus = '1' AND dn.docstatus = '1' {conditions}
            ORDER BY dni.idx ASC"""\
        .format(conditions=self.get_conditions()), as_list=1)
        for dni in delivery_items_data:
            dc_no = dni[0]
            customer = dni[1]
            customer_code = dni[2]
            po_no = dni[3]
            posting_date = dni[4]
            posting_time = dni[5]
            item_name = dni[6]
            design_name = dni[8]
            warehouse = dni[9]
            gsm = dni[10]
            width = dni[11]
            uom = dni[12]
            qty = dni[13]
            pkg_no = dni[14]
            pkg_qty = dni[15]
            design_height = dni[16]
            design_gap = dni[17]
            fabric_material = dni[18]
            fabric_type = dni[19]
            is_raw_fabric = dni[20]
            panel_qty = 0
            printed_qty = 0
            unprinted_qty = 0
            
            if is_raw_fabric == 0:
                printed_qty = qty
            else:
                unprinted_qty = qty
            
            if design_name == None:
                design_name = item_name
            
            if design_gap == None:
                design_gap = 0
                
            if design_height != None:
                """panel_qty = ((qty)/((design_height + design_gap )*0.0254))"""
                panel_qty = float(printed_qty) / (float(design_height) + float(design_gap ))
                
            total[0] += printed_qty
            total[1] += unprinted_qty
            total[2] += panel_qty
            total[3] += pkg_qty
            
            
            
            data.append([
                posting_date, dc_no[3:11], warehouse, customer_code+'-'+customer, po_no, fabric_material, fabric_type, design_name, gsm, width, '{:2,.2f}'.format(printed_qty), '{:2,.2f}'.format(unprinted_qty), uom, '{:2,.0f}'.format(panel_qty), pkg_no, '{:2,.0f}'.format(pkg_qty)
            ])
        data.append([
            'TOTAL','','','','','','','','','', '{:2,.2f}'.format(total[0]), '{:2,.2f}'.format(total[1]), '', '{:2,.0f}'.format(total[2]),'', '{:2,.0f}'.format(total[3])
        ])
        return data

    def get_conditions(self):
        conditions = []
        if self.filters.get("from_date"):
            from_date = self.filters.get("from_date")
            to_date = self.filters.get("to_date")
            conditions.append("dn.posting_date BETWEEN '{0}' AND '{1}'". format(from_date, to_date))
        if self.filters.get("customer"):
            customer = self.filters.get("customer")
            conditions.append("dn.customer = '{0}'". format(customer))
        if self.filters.get("po_no"):
            po_no = self.filters.get("po_no")
            conditions.append("dn.po_no = '{0}'". format(po_no))
        if self.filters.get("sales_order"):
            sales_order = self.filters.get("sales_order")
            conditions.append("dni.against_sales_order = '{0}'". format(sales_order))
        if self.filters.get("fabric_material"):
            fabric_material = self.filters.get("fabric_material")
            conditions.append("dni.fabric_material = '{0}'". format(fabric_material))
        if self.filters.get("fabric_type"):
            fabric_type = self.filters.get("fabric_type")
            conditions.append("dni.fabric_type = '{0}'". format(fabric_type))
        return "and {}".format(" and ".join(conditions)) if conditions else ""

    def get_columns(self):

        self.columns = [
            {
                "label": _("DC Date"),
                "fieldname": "posting_date",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("DC No."),
                "fieldname": "dc_no",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Warehouse"),
                "fieldname": "warehouse",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Customer"),
                "fieldname": "party_name",
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
                "label": _("Design Name"),
                "fieldname": "design_name",
                "fieldtype": "Data",
                "width": 250
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
                "label": _("Printed Qty"),
                "fieldname": "printed_qty",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Unprinted Qty"),
                "fieldname": "unprinted_qty",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Unit"),
                "fieldname": "uom",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Panel"),
                "fieldname": "panel_qty",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Pkg No"),
                "fieldname": "pkg_no",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Pkg Qty"),
                "fieldname": "pkg_qty",
                "fieldtype": "Data",
                "width": 80
            }
        ]
        
@frappe.whitelist()
def get_item_attribute_list():
    return frappe.get_all("Item Attribute Value", filters={"parent": ["IN", ("Type") ] }, fields=["attribute_value"], order_by="attribute_value")
    