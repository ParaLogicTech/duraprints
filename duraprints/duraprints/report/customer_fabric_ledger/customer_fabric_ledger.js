// Copyright (c) 2016, Betalogics and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Fabric Ledger"] = {
	"filters": [
		{
			"fieldname":"item",
			"label": __("Customer Fabric"),
			"fieldtype": "Link",
			"options": 'Item',
			"reqd" : 1,
			"get_query": function(){ return {'filters': [['item_group','in', 'Polyester fabrics,Cotton fabrics,Silk fabrics,Viscose fabrics' ]]}}
		}
	]	
};
