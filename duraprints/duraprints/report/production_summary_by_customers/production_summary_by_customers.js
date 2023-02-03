// Copyright (c) 2016, Betalogics and contributors
// For license information, please see license.txt
/* eslint-disable */
var d = new Date();
frappe.query_reports["Production Summary by Customers"] = {
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
			"fieldname":"design_count",
			"label": __("Top Design Count"),
			"fieldtype": "Select",
			"options": [
				"3",
				"5",
				"10"
			],
			"default": "3"
		}
	]
};
