# Copyright (c) 2013, Betalogics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.utils import getdate
from datetime import date, timedelta
from frappe import msgprint, _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}
	
	data = []
	columns = get_columns(filters)
	data = get_item_groups(filters, data)

	return columns, data

def get_item_groups(filters, data):
	grand_total = [0,0,0,0,0,0,0,0]
	item_groups = frappe.get_all("Item Group", filters={"parent_item_group": ["in", ("Fabrics") ]}, fields=["item_group_name"], order_by="item_group_name")
	for tg in item_groups:
		total = [0,0,0,0,0,0,0,0]
		item_group = tg.item_group_name
		data.append([item_group,''])
		data, total = get_items(item_group, filters, data, total)
		data.append(["SUB TOTAL",
			'{:0,.2f}'.format(total[0]),'{:0,.2f}'.format(total[1]),'{:0,.2f}'.format(total[2]),'{:0,.2f}'.format(total[3]),
			'{:0,.2f}'.format(total[4]),'{:0,.2f}'.format(total[5]),'{:0,.2f}'.format(total[6]),'','','','{:0,.2f}'.format(total[7])
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
		'{:0,.2f}'.format(grand_total[4]),'{:0,.2f}'.format(grand_total[5]),'{:0,.2f}'.format(grand_total[6]),'','','','{:0,.2f}'.format(grand_total[7])
	])
	return data

def get_items(item_group, filters, data, total):
	query_details = ""

	bet_dates = [filters.get('from_date'),filters.get('to_date')]
	data_cols = get_additional_query(bet_dates,"posting_date",query_details, filters)

	items = frappe.db.sql("""SELECT
		i.item_code, i.item_name, i.stock_uom, ip.price_list_rate as rate,
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
		i.item_group = "{item_group}"
		GROUP BY i.item_name
		ORDER BY i.item_name ASC"""\
		.format(item_group=item_group, data_cols=data_cols), as_list=1)
	for ti in items:
		code = ti[0]
		name = ti[1]
		stock_uom = ti[2]
		rate = ti[3]
		re_order = ti[4]
		purchase = ti[5]
		purchase_return = abs(ti[6])
		net_purchase = 0
		purchase_value = 0
		if purchase > 0 or purchase_return > 0:
			net_purchase = purchase - purchase_return
			purchase_value = rate*net_purchase
		
		from erpnext.stock.stock_ledger import get_previous_sle
		opening_entry = get_previous_sle({
				"item_code": code,
				"warehouse_condition": "warehouse IN ('Fabric Stores - DP')",
				"posting_date": bet_dates[0],
				"posting_time": "00:00:00"
		})
		opening_balance = opening_entry.get("qty_after_transaction",0)

		closing_entry = get_previous_sle({
				"item_code": code,
				"warehouse_condition": "warehouse IN ('Fabric Stores - DP')",
				"posting_date": bet_dates[1],
				"posting_time": "23:59:59"
		})
		closing_balance = closing_entry.get("qty_after_transaction",0)
		use = abs(closing_balance+net_purchase-opening_balance)
		value = 0
		if rate != None:
			value = rate*abs(closing_balance)
		else:
			rate = 0
		if float(opening_balance) > 0:
			data.append([
				name,
				'{:0,.2f}'.format(opening_balance),
				'{:0,.2f}'.format(purchase),'{:0,.2f}'.format(purchase_return),'{:0,.2f}'.format(net_purchase),
				purchase_value,
				'{:0,.2f}'.format(use),'{:0,.2f}'.format(closing_balance),re_order,
				stock_uom,'{:0,.2f}'.format(rate),'{:0,.2f}'.format(value),''
			])
			total[0] += opening_balance
			total[1] += purchase
			total[2] += purchase_return
			total[3] += net_purchase
			total[4] += purchase_value
			total[5] += use
			total[6] += closing_balance
			total[7] += value
		
	return data, total

def get_additional_query(bet_dates, trans_date, query_details, filters):
	
	query_details = """
				,
				COALESCE(SUM(IF( (sl.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s') AND sl.voucher_type IN ('Purhcase Invoice') , sl.actual_qty, 0) ),0) as purchase,
				COALESCE(
					(
						SELECT 
						SUM(pii.qty) FROM `tabPurchase Invoice Item` pii 
						WHERE 
						pii.qty < 0 AND
						pii.item_code = i.item_code AND
						pii.docstatus = 1 AND 
						pii.parent IN 
						(
							SELECT name FROM `tabPurchase Invoice` pi WHERE pi.%(trans_date)s BETWEEN '%(sd)s' AND '%(ed)s' AND pi.docstatus = '1'
						)
					),
				0) as purchase_return
				""" % { "trans_date": trans_date, "sd": bet_dates[0],"ed": bet_dates[1] }
	
	return query_details

def get_conditions(filters):
	conditions = []
	if filters.get("from_date"):
		from_date = filters.get("from_date")
		to_date = filters.get("to_date")
		conditions.append("pi.posting_date BETWEEN '{0}' AND '{1}'". format(from_date, to_date))

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_columns(filters):
	"""return columns based on filters"""

	columns = [
		{
			"label": _("Item Name"),
			"fieldname": "item",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Opening"),
			"fieldname": "opening_balance",
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Purchase"),
			"fieldname": "purchase",
			"fieldtype": "Float",
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
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Purchase Value"),
			"fieldname": "purchase_value",
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Use"),
			"fieldname": "use",
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Closing"),
			"fieldname": "closing_balance",
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Re Order"),
			"fieldname": "re_order",
			"fieldtype": "Float",
			"width": 80,
			"precision" : 2
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
			"fieldtype": "Currency",
			"width": 80,
			"precision" : 2
		},
		{
			"label": _("Value"),
			"fieldname": "stock_value",
			"fieldtype": "Currency",
			"width": 120,
			"precision" : 2
		},
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 150
		}
	]
	return columns