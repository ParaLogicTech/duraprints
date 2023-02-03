// url /home/frappe/frappe-bench/apps/erpnext/erpnext/manufacturing/doctype/work_order
frappe.listview_settings['Work Order'] = {
	onload: function(listview) {
		setTimeout(function(){
			$('.frappe-list').find('.list-subject').each(function(e){
				$(this).css({flex : "5"});
				//console.log('check');
			});
		}, 3000);
		listview.page.add_menu_item(__("Expand Column"), function() {
			$('.frappe-list').find('.list-subject').each(function(e){
				$(this).css({flex : "5"});
				//console.log('check');
			});
		});
		listview.page.add_action_item(__("Bulk Process"), function() {
			//console.log(getIdsFromList());
			//console.log(listview.page);
			var names = [];
			$('.frappe-list').find("input:checked").each(function(){
				var name = $(this).attr('data-name');
				names.push(name);
			});
			//console.log(names);
			frappe.call({
				method: "duraprints.duraprints.doctype.compound_production.work_order_list.get_work_order_list_details",
				args: {
					"names": names
				},
				async: false,
				callback: function(r) {
					console.log(r.message);
					var work_order_list = r.message;
					for(var j=0; j<work_order_list.length; j++){
						var work_order_data = work_order_list[j];

						var sales_order_data;
						if(work_order_data.status != 'Completed'){
							if(work_order_data.sales_order != ''){
								frappe.call({
									method: "duraprints.duraprints.doctype.compound_production.work_order_list.get_sales_order",
									type: "post",
									async: false, 
									args: {
										"sales_order" : work_order_data.sales_order
									},
									callback: function(r) {
										sales_order_data = r.message;
										//location.reload();
										//console.log(sales_order_data);
									}
								});
								var updated_work_order_data = {};
								updated_work_order_data.planned_start_date = sales_order_data.transaction_date;
								updated_work_order_data.expected_delivery_date = sales_order_data.delivery_date;
								updated_work_order_data.process_execution = "Bulk Process";
							
								//frappe.call({
								//	url: "/api/resource/Work Order/"+work_order_data.name,
								//	type: "PUT",
								//	args: {
								//		data : updated_work_order_data
								//	},
								//	callback: function(e) {
								//		console.log(JSON.stringify(e));
								//		//location.reload();
								//	}
								//});
							
								//console.log(sales_order_data);
							}else{
								sales_order_data.transaction_date = "";
							}

							var purpose = ["Material Transfer for Manufacture","Manufacture"];
							for (var i = 0; i < purpose.length; i++){
								console.log(work_order_data.name+' Started: '+purpose[i]);
								frappe.call({
									method: "erpnext.manufacturing.doctype.work_order.work_order.make_stock_entry",
									args: {
										"work_order_id": work_order_data.name,
										"purpose": purpose[i],
										"qty": work_order_data.qty
									},
									async: false,
									callback: function(r) {
										//console.log(r.message);
										var stock_data = r.message;
										stock_data.docstatus = 1;
										stock_data.posting_date = frappe.datetime.get_today();
										stock_data.posting_time = frappe.datetime.now_time();
										stock_data.set_posting_time = 1;
										
										//console.log(stock_data);
										console.log(work_order_data.name+' Reading Done: '+purpose[i]);
										frappe.call({
											url: "/api/resource/Stock Entry",
											type: "POST",
											args: {
												data : stock_data
											},
											async: false,
										}).then((r) => {
											console.log(work_order_data.name+' Completed: '+purpose[i]);
											frappe.utils.play_sound('submit');
											//console.log(JSON.stringify(r));
											//location.reload();
											
										});
									}
								});
							}
							
						}
					}
				}
			});

			//location.reload();
			//console.log(names);
			console.log("Work orders processing completed.");
			frappe.msgprint("Work orders processing completed.");
			frappe.utils.play_sound('submit');
		});

		listview.page.add_action_item(__("Bulk Process Skip"), function() {
			//console.log(getIdsFromList());
			//console.log(listview.page);
			var names = [];
			$('.frappe-list').find("input:checked").each(function(){
				var name = $(this).attr('data-name');
				names.push(name);
			});
			//console.log(names);
			frappe.call({
				method: "duraprints.duraprints.doctype.compound_production.work_order_list.get_work_order_list_details",
				args: {
					"names": names
				},
				async: false,
				callback: function(r) {
					console.log(r.message);
					var work_order_list = r.message;
					for(var j=0; j<work_order_list.length; j++){
						var work_order_data = work_order_list[j];

						var sales_order_data;
						if(work_order_data.status != 'Completed'){
							/*if(work_order_data.sales_order != ''){
								frappe.call({
									method: "duraprints.duraprints.doctype.compound_production.work_order_list.get_sales_order",
									type: "post",
									async: false, 
									args: {
										"sales_order" : work_order_data.sales_order
									},
									callback: function(r) {
										sales_order_data = r.message;
										//location.reload();
										//console.log(sales_order_data);
									}
								});
								var updated_work_order_data = {};
								updated_work_order_data.planned_start_date = sales_order_data.transaction_date;
								updated_work_order_data.expected_delivery_date = sales_order_data.delivery_date;
								updated_work_order_data.process_execution = "Bulk Process";
							
								//frappe.call({
								//	url: "/api/resource/Work Order/"+work_order_data.name,
								//	type: "PUT",
								//	args: {
								//		data : updated_work_order_data
								//	},
								//	callback: function(e) {
								//		console.log(JSON.stringify(e));
								//		//location.reload();
								//	}
								//});
							
								//console.log(sales_order_data);
							}else{
								sales_order_data.transaction_date = "";
							}
							 */
							var purpose = ["Manufacture"];
							for (var i = 0; i < purpose.length; i++){
								console.log(work_order_data.name+' Started: '+purpose[i]);
								frappe.call({
									method: "erpnext.manufacturing.doctype.work_order.work_order.make_stock_entry",
									args: {
										"work_order_id": work_order_data.name,
										"purpose": purpose[i],
										"qty": work_order_data.qty
									},
									async: false,
									callback: function(r) {
										//console.log(r.message);
										var stock_data = r.message;
										stock_data.docstatus = 1;
										stock_data.posting_date = frappe.datetime.get_today();
										stock_data.posting_time = frappe.datetime.now_time();
										stock_data.set_posting_time = 1;
										
										//console.log(stock_data);
										console.log(work_order_data.name+' Reading Done: '+purpose[i]);
										
										frappe.call({
											url: "/api/resource/Stock Entry",
											type: "POST",
											args: {
												data : stock_data
											},
											async: false,
										}).then((r) => {
											console.log(work_order_data.name+' Completed: '+purpose[i]);
											frappe.utils.play_sound('submit');
											//console.log(JSON.stringify(r));
											//location.reload();
											//frappe.db.commit();
											
										});
									}
								});
							}
							
						}
					}
				}
			});

			console.log("Work orders processing completed.");
			frappe.msgprint("Work orders processing completed.");
			frappe.utils.play_sound('submit');
		});
	},
	add_fields: ["bom_no", "status", "sales_order", "qty",
		"produced_qty", "expected_delivery_date", "planned_start_date", "planned_end_date"],
	filters: [["status", "!=", "Stopped"]],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Not Started"), "orange", "status,=,Submitted"];
		} else {
			return [__(doc.status), {
				"Draft": "red",
				"Stopped": "red",
				"Not Started": "red",
				"In Process": "orange",
				"Completed": "green",
				"Cancelled": "darkgrey"
			}[doc.status], "status,=," + doc.status];
		}
	}
};