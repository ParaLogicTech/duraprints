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
    return ItemStockPurchaseReport(filters).run()

class ItemStockPurchaseReport(object):
    def __init__(self, filters=None):
        super(ItemStockPurchaseReport, self).__init__()
        self.filters = frappe._dict(filters or {})

    def run(self):
        data = []
        self.columns = []
        
        data = self.get_item_groups(data)
        self.get_columns()

        return self.columns, data
    
    def get_item_groups(self, data):
        grand_total = [0,0,0,0,0,0,0,0]
        item_groups = frappe.get_all("Item Group", filters={"item_group_name": ["not in", ("Products","Fabrics","All Item Groups","Sub Assemblies","Process","Raw Material","Inks, chemicals and consumables","Services","Consumable") ], "parent_item_group": ["not in", ("Products", "Fabrics","Sub Assemblies","Process") ]}, fields=["item_group_name"], order_by="item_group_name")
        for tg in item_groups:
            total = [0,0,0,0,0,0,0,0]
            item_group = tg.item_group_name
            data.append([item_group,'','','','','','','','','','','',''])
            data, total = self.get_items(item_group, data, total)
            data.append(["SUB TOTAL",
                '{:0,.2f}'.format(total[0]),'{:0,.2f}'.format(total[1]),'{:0,.2f}'.format(total[2]),'{:0,.2f}'.format(total[3]),
                '{:0,.2f}'.format(total[4]),'{:0,.2f}'.format(total[5]),'{:0,.2f}'.format(total[6]),'','','','{:0,.2f}'.format(total[7]),''
            ])
            grand_total[0] += total[0]
            grand_total[1] += total[1]
            grand_total[2] += total[2]
            grand_total[3] += total[3]
            grand_total[4] += total[4]
            grand_total[5] += total[5]
            grand_total[6] += total[6]
            grand_total[7] += total[7]

        
        data.append(["GRAND TOTAL",
            '{:0,.2f}'.format(grand_total[0]),'{:0,.2f}'.format(grand_total[1]),'{:0,.2f}'.format(grand_total[2]),'{:0,.2f}'.format(grand_total[3]),
            '{:0,.2f}'.format(grand_total[4]),'{:0,.2f}'.format(grand_total[5]),'{:0,.2f}'.format(grand_total[6]),'','','','{:0,.2f}'.format(grand_total[7]),
            ''
        ])
        return data

    def get_items(self, item_group, data, total):
        query_details = ""

        bet_dates = [self.filters.get('from_date'),self.filters.get('to_date')]
        data_cols = self.get_additional_query(bet_dates,"posting_date",query_details)

        items = frappe.db.sql("""SELECT
            i.item_code, i.item_name, i.stock_uom, IFNULL(ip.price_list_rate,0) as rate,
            COALESCE(
                (
                    SELECT 
                    ir.warehouse_reorder_level 
                    FROM
                    `tabItem Reorder` ir
                    WHERE
                    ir.warehouse NOT IN ('Work In Progress')
                    AND 
                    ir.parent = i.item_code
                )
            ,0) as reorder_level
            {data_cols}
            FROM `tabItem` i
            LEFT JOIN `tabItem Price` ip ON i.item_name = ip.item_name AND ip.price_list = 'Standard Buying'
            LEFT JOIN `tabStock Ledger Entry` sl ON sl.item_code = i.item_code
            WHERE 
            i.item_group = "{item_group}" AND i.disabled = 0
            GROUP BY i.item_name
            ORDER BY i.item_name ASC"""\
            .format(item_group=item_group, data_cols=data_cols), as_dict=1)
        for ti in items:
            net_purchase = 0
            purchase_value = 0
            if ti.purchase > 0 or ti.purchase_return > 0:
                net_purchase = flt(ti.purchase) - flt(ti.purchase_return)
                purchase_value = flt(ti.rate*net_purchase)
            
            from erpnext.stock.stock_ledger import get_previous_sle
            opening_entry = get_previous_sle({
                    "item_code": ti.item_code,
                    "warehouse_condition": "warehouse NOT IN ('Work In Progress - DP')",
                    "posting_date": bet_dates[0],
                    "posting_time": "00:00:00"
            })
            opening_balance = opening_entry.get("qty_after_transaction",0)

            closing_entry = get_previous_sle({
                    "item_code": ti.item_code,
                    "warehouse_condition": "warehouse NOT IN ('Work In Progress - DP')",
                    "posting_date": bet_dates[1],
                    "posting_time": "23:59:59"
            })
            closing_balance = closing_entry.get("qty_after_transaction",0)
            use = abs(closing_balance+net_purchase-opening_balance)
            value = 0
            if ti.rate != None:
                value = ti.rate*abs(closing_balance)
            else:
                ti.rate = 0
            data.append([
                ti.item_name,
                '{:0,.2f}'.format(opening_balance),
                '{:0,.2f}'.format(ti.purchase),'{:0,.2f}'.format(ti.purchase_return),'{:0,.2f}'.format(net_purchase),
                purchase_value,
                '{:0,.2f}'.format(use),'{:0,.2f}'.format(closing_balance),ti.reorder_level,
                ti.stock_uom,'{:0,.2f}'.format(ti.rate),'{:0,.2f}'.format(value),''
            ])
            total[0] += opening_balance
            total[1] += ti.purchase
            total[2] += ti.purchase_return
            total[3] += net_purchase
            total[4] += purchase_value
            total[5] += use
            total[6] += closing_balance
            total[7] += value
                
        return data, total

    def get_additional_query(self, bet_dates, trans_date, query_details):
        
        query_details = """
                    ,
                    COALESCE(SUM(IF( (sl.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s') AND sl.voucher_type IN ('Purchase Receipt') , sl.actual_qty, 0) ),0) as purchase,
                    COALESCE(
                        (
                            SELECT 
                            SUM(pri.qty) FROM `tabPurchase Receipt Item` pri 
                            WHERE 
                            pri.qty < 0 AND
                            pri.item_code = i.item_code AND
                            pri.docstatus = 1 AND 
                            pri.parent IN 
                            (
                                SELECT name FROM `tabPurchase Receipt` pr WHERE pr.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s' AND pr.docstatus = '1'
                            )
                        ),
                    0) as purchase_return
                    """ % { "trans_date": trans_date, "sd": bet_dates[0],"ed": bet_dates[1] }
        
        return query_details
    
    def get_conditions(self):
        conditions = []
        if self.filters.get("from_date"):
            from_date = self.filters.get("from_date")
            to_date = self.filters.get("to_date")
            conditions.append("pr.posting_date BETWEEN '{0}' AND '{1}'". format(from_date, to_date))
        return "and {}".format(" and ".join(conditions)) if conditions else ""

    def get_columns(self):

        self.columns = [
            {
                "label": _("Item Name"),
                "fieldname": "item",
                "fieldtype": "Data",
                "width": 200
            },
            {
                "label": _("Opening"),
                "fieldname": "opening_balance",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Purchase"),
                "fieldname": "purchase",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("PR Return"),
                "fieldname": "purchase_return",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Net Purchase"),
                "fieldname": "net_purchase",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Purchase Value"),
                "fieldname": "purchase_value",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Use"),
                "fieldname": "use",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Closing"),
                "fieldname": "closing_balance",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Re Order"),
                "fieldname": "reorder_level",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Unit"),
                "fieldname": "unit",
                "fieldtype": "Data",
                "width": 60
            },
            {
                "label": _("Rate"),
                "fieldname": "rate",
                "fieldtype": "Data",
                "width": 70
            },
            {
                "label": _("Value"),
                "fieldname": "stock_value",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Remarks"),
                "fieldname": "remarks",
                "fieldtype": "Data",
                "width": 150
            }
        ]
        
@frappe.whitelist()
def get_item_attribute_list():
    return frappe.get_all("Item Attribute Value", filters={"parent": ["IN", ("Type") ] }, fields=["attribute_value"], order_by="attribute_value")
    