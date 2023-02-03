// Copyright (c) 2021, Betalogics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Compound Packing', {
	// refresh: function(frm) {

	// }
	get_sales_orders: function(frm) {
		frappe.call({
			method: "get_open_sales_orders",
			doc: frm.doc,
			callback: function(r) {
				//console.log(r);
				refresh_field("sales_order");

				//frm.save();
			}
		});
	},
	get_items: function(frm){
		var sales_order_list = [];
		$.each(cur_frm.doc.sales_order || [], function(i, row) {
			//console.log(row);
			if(typeof row.sales_order != 'undefined' && row.sales_order != ""){
				//console.log(row);
				sales_order_list.push(row.sales_order);
			}
		});
		//console.log(sales_order_list);
		if(sales_order_list.length > 0){
			frappe.call({
				method: "get_sales_order_items",
				args: {
					sales_order_list: JSON.stringify(sales_order_list)
				},
				doc: frm.doc,
				callback: function(r) {
					console.log(r);
					refresh_field("items");

					//frm.save();
				}
			});
		}
	}
});

