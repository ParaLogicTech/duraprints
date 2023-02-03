# -*- coding: utf-8 -*-
# Copyright (c) 2021, Betalogics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json, copy
from frappe import msgprint, _
from six import string_types, iteritems

from frappe.model.document import Document
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and, now_datetime, ceil

class CompoundPacking(Document):
    
    @frappe.whitelist()
    def get_open_sales_orders(self):
        """ Pull sales orders  which are pending to deliver based on criteria selected"""
        open_so = get_sales_orders(self)
        
        """return open_so"""
    
        if open_so:
            self.add_so_in_table(open_so)
        else:
            frappe.msgprint(_("Sales orders are not available for packing."))

    def add_so_in_table(self, open_so):
        """ Add sales orders in the table"""
        self.set('sales_order', [])
        
        for data in open_so:
            remaining_qty = 1
            if data.per_delivered != 0:
                remaining_qty = data.per_delivered/100               
                
            self.append('sales_order', {
                'sales_order': data.name,
                'sales_order_date': data.transaction_date,
                'customer': data.customer,
                'total_qty': data.total_qty,
                'remaining_qty': data.total_qty*(remaining_qty)
            })
            
    
            
    @frappe.whitelist() 
    def get_sales_order_items(self, sales_order_list):
        
        sales_order_list = json.loads(sales_order_list)       
        sales_order_list = "','".join(sales_order_list)
    
        pending_items = get_so_items(self, sales_order_list)
        """return pending_items"""
        
        if pending_items:
            self.add_item_in_table(pending_items)
        else:
            frappe.msgprint(_("Sales orders Items are not available for packing"))
    

    def add_item_in_table(self, pending_items):
        """ Add Items in the table"""
        self.set('items', [])
        
        for data in pending_items:                
            self.append('items', {
                'design_name': data.design_name,
                'design_image': data.image,
                'item_code': data.item_code,
                'item_name': data.item_name,
                'packed_qty': data.actual_qty-data.delivered_qty,
                'pending_qty': data.actual_qty-data.delivered_qty,
                'sales_order': data.parent,
                'package_no': 'RL-1'
            })
            
def get_sales_orders(self):
    so_filter = item_filter = ""
    if self.from_date:
        so_filter += " and so.transaction_date >= %(from_date)s"
    if self.to_date:
        so_filter += " and so.transaction_date <= %(to_date)s"
    if self.customer:
        so_filter += " and so.customer = %(customer)s"

    open_so = frappe.db.sql("""
        select distinct so.name, so.transaction_date, so.customer, so.total_qty, so.base_grand_total, so.per_delivered
        from `tabSales Order` so, `tabSales Order Item` so_item
        where so_item.parent = so.name
            and so.docstatus = 1 and so.status not in ("","Stopped", "Closed")
            and so_item.qty > so_item.delivered_qty {0}
        """.format(so_filter), {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "customer": self.customer			
        }, as_dict=1)
    return open_so

def get_so_items(self,sales_order_list):
    item_filter = " and so.parent IN ('%(sales_order_list)s')"

    soi = frappe.db.sql("""
        select so_item.parent, so_item.design_name, so_item.item_code, so_item.item_name, so_item.image, so_item.actual_qty, so_item.delivered_qty
        FROM `tabSales Order Item` so_item
        where so_item.parent IN ('{0}')
            and so_item.qty > so_item.delivered_qty
        """.format(sales_order_list), as_dict=1)
    return soi
    