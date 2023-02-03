# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
from frappe.model.document import Document
from requests import get
from io import BytesIO
from PIL import Image


class CompoundProduction(Document):
    def validate(self):
        """self.title = format_item_name(self);
        self.primary_item_name = get_item_name(self.primary_item_code)"""

@frappe.whitelist()
def get_item_name(code):
    item = frappe.get_doc("Item", code)
    """return " ".join(filter(None, [item.item_name]))"""
    data = {
        "name": item.item_name,
        "group": item.item_group,
        "weight_per_unit" : item.weight_per_unit,
        "uoms": item.uoms,
        "attributes" : item.attributes
    }
    return data

@frappe.whitelist()
def get_customer(customer):
    customer_info = frappe.get_doc("Customer", customer)
    data = {
        "customer_code": customer_info.customer_code,
        "customer_abbreviation" : customer_info.customer_abbreviation
    }
    return data

@frappe.whitelist()
def get_all_attachments(document, method=None):
    document = json.loads(document)
    document["doctype"] = "Compound Production"
    attachments = frappe.db.sql("""select file_url from `tabFile` where attached_to_doctype = %(doctype)s and attached_to_name = %(docname)s ORDER BY file_name ASC""", {'doctype': document["doctype"],'docname': document["name"]}, as_dict=True)
    
    for attc in attachments:
        location = attc.file_url
        image_raw = get("http://172.16.0.121"+location)
        image = Image.open(BytesIO(image_raw.content))
        width, height = image.size
        attc.width = width
        attc.height = height
    return attachments