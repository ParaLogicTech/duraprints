// Copyright (c) 2016, Betalogics and contributors
// For license information, please see license.txt
/* eslint-disable */

var d = new Date();
var fabric_type = [];
frappe.call({
	method: "duraprints.duraprints.report.delivery_summary.delivery_summary.get_item_attribute_list",
	callback: function(r) {
		//console.log(r);
		for(var i=0; i<r.message.length; i++){
			fabric_type.push(r.message[i].attribute_value);
		}
	} 
});
fabric_type.unshift("");
frappe.query_reports["Delivery Summary"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": new Date(d.getFullYear(),d.getMonth(),1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "customer",
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"fieldname":"fabric_material",
			"label": __("Material"),
			"fieldtype": "Select",
			"options": [
				"",
				"Cotton",
				"Polyester",
				"Silk",
				"Viscose",
			],
		},
		{
			"fieldname": "fabric_type",
			"label": __("Fabric Type"),
			"fieldtype": "Select",
			"options": fabric_type
		},
		{
			"fieldname": "sales_order",
			"label": __("Sales Order #"),
			"fieldtype": "Link",
			"options": "Sales Order",
		},
		{
			"fieldname": "po_no",
			"label": __("PO #"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "include_return_fabric",
			"label": __("Include Return Fabric"),
			"fieldtype": "Check"
		},
	]
};