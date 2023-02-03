// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

// url /home/frappe/frappe-bench/apps/duraprints/duraprints/duraprints/doctype/compound_production

cur_frm.fields_dict['fabric_code'].get_query = function(doc) {
	return {
		filters: [
			['Item', 'item_group', 'in', 'Polyester fabrics,Cotton fabrics,Silk fabrics,Viscose fabrics']
		]
	}
}
cur_frm.fields_dict['process_code'].get_query = function(doc) {
	return {
		filters: [
			['Item', 'item_group', 'in', 'Process']
		]
	}
}

frappe.ui.form.on("Compound Item", {
	width: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		if (frm.doc.default_design_uom) {
			row.design_uom = frm.doc.default_design_uom;
			refresh_field("design_uom", cdn, "items");
		}
		if (frm.doc.default_gap) {
			row.gap = frm.doc.default_gap;
			refresh_field("gap", cdn, "items");
		}
	},
});

frappe.ui.form.on('Compound Production', {
	default_design_uom: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			d.design_uom = frm.doc.default_design_uom;
		});
		refresh_field("items");
	},
	default_gap: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			d.gap = frm.doc.default_gap;
		});
		refresh_field("items");
	},
	default_width: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			d.width = frm.doc.default_width;
		});
		refresh_field("items");
	},
	default_height: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			d.height = frm.doc.default_height;
		});
		refresh_field("items");
	},
	refresh: function(frm, cdt, cdn) {
		if(!frm.doc.__islocal){
			frm.add_custom_button(__('Fetch Images'), function(){
				frm.call({
					method: "duraprints.duraprints.doctype.compound_production.compound_production.get_all_attachments",
					args: {
						document: frappe.model.get_doc(cdt, cdn),
					},
					callback: function(r) {
						//console.log(JSON.stringify(r));
						console.log(r);
						if(r.message.length != 0){
							for(var i=0; i<r.message.length; i++){
								var child = cur_frm.add_child("items");
								//frappe.model.set_value(child.doctype, child.name, "item_code", "My Item Code")
								
								var img_url = r.message[i].file_url;
								var filename = img_url.substring(img_url.lastIndexOf('/')+1);
								var filenameText = filename.replace(/\.[^/.]+$/, "");
								
								var resolution = 10;
								var imgHeight = r.message[i].height/resolution;
								var imgWidth = r.message[i].width/resolution;
					
					
									
								frappe.model.set_value(child.doctype, child.name, "image", img_url);
								frappe.model.set_value(child.doctype, child.name, "image_name", filenameText);
								frappe.model.set_value(child.doctype, child.name, "design_uom", frm.doc.default_design_uom);
								frappe.model.set_value(child.doctype, child.name, "gap", frm.doc.default_gap);
								frappe.model.set_value(child.doctype, child.name, "width", imgWidth);
								frappe.model.set_value(child.doctype, child.name, "height", imgHeight);
								//frappe.model.set_value(child.doctype, child.name, "width", frm.doc.default_width);
								//frappe.model.set_value(child.doctype, child.name, "height", frm.doc.default_height);
								
								cur_frm.refresh_field("items");
							}
						}else{
							alert("Attach images first.");
						}
						
					}
				});
			});

			frm.add_custom_button(__('Create Items'), function(){
				var compound_production = frappe.model.get_doc(cdt, cdn);
				//console.log(compound_production);
				///console.log(compound_production.name);
				//console.log(compound_production.creation);
				if(typeof compound_production.creation != 'undefined'){
					var custom_date = compound_production.date.split("-");
					//var uoms = JSON.parse(compound_production.fabric_uoms);
					//console.log(uoms);
					var compound_production_id = compound_production.name;
					var attributes = JSON.parse(compound_production.fabric_properties);
					var gsm,width,type,construction,source = "";
					var is_customer_provided_item = compound_production.is_customer_provided_fabric;
					var customer_name = "";
					if(is_customer_provided_item == 1){
						var customer_name = compound_production.customer;
					}
					for(var i=0; i<attributes.length; i++){

						if(attributes[i].attribute == 'GSM'){
							gsm = attributes[i].attribute_value;
						}
						if(attributes[i].attribute == 'Width'){
							width = attributes[i].attribute_value;
						}
						if(attributes[i].attribute == 'Type'){
							type = attributes[i].attribute_value;
						}
						if(attributes[i].attribute == 'Construction'){
							construction = attributes[i].attribute_value;
						}
						if(attributes[i].attribute == 'Source'){
							source = attributes[i].attribute_value;
						}
						
					}
					//console.log("GSM: " +gsm);
					var sCount = 0;
					$.each(cur_frm.doc.items || [], function(i, row) {
						if(typeof row.item_code == 'undefined' || row.item_code == ""){
							
							console.log(row);
							
							var img_url = row.image;
							var image_title = row.image_name;
							var item_code = row.item_code;
							var design_gap = row.gap;
							var design_uom = row.design_uom;
							var design_notes = row.design_notes;
							var design_height = row.height;
							var design_width = row.width;						

							var wastage = row.wastage;
							var wastage_percentage = 1;
							if( wastage != 0 && wastage > 0 ){
								wastage_percentage = 1 + (wastage/100);
							}

							if(urlExists(img_url) != 200) {
								img_url = "";
								cur_frm.doc.items[i].image = "";
							}
							
							if(design_height > 0){
								var uoms = JSON.parse(compound_production.fabric_uoms);
								uoms.push({"uom": "Unit", "conversion_factor": (parseFloat(design_height) + parseFloat(design_gap))*0.0254 })
								console.log(uoms);
							}
							if((image_title == undefined || image_title.length == 0) && (img_url != undefined && img_url.length != 0)){
								var filename = img_url.substring(img_url.lastIndexOf('/')+1);
								image_title = filename.replace(/\.[^/.]+$/, "");
								//console.log(image_title);
								cur_frm.doc.items[i].image_name = image_title;
								
							}
							cur_frm.refresh_fields('items');
							var fabric_group = compound_production.fabric_group.split(" ");
							
							console.log(uoms);

							var item_creation = { 
								"item_name" : compound_production.customer_abbreviation + '-' + compound_production.fabric_code + '-' + image_title + '-' + custom_date[2]+custom_date[1],
								"item_code" : compound_production.customer_abbreviation + '-' + compound_production.fabric_code + '-' + image_title + '-' + custom_date[2]+custom_date[1],
								"item_group" : "Printed " + fabric_group[0].toLowerCase(),
								"image" : img_url,
								"stock_uom" : "Meter",
								"compound_production_id" : compound_production_id,
								"weight_uom" : "Kg",
								"weight_per_unit" : compound_production.fabric_weight_per_unit,
								"default_material_request_type" : "Manufacture",
								"is_purchase_item" : 0,
								"fabric_name" : compound_production.fabric_name, 
								"fabric_gsm" : gsm,
								"fabric_width": width,
								"fabric_type" : type,
								"fabric_source" : source,
								"fabric_construction" : construction,
								"fabric_material": fabric_group[0],
								"fabric_wastage": wastage,
								"design_width": design_width,
								"design_height": design_height,
								"design_gap": design_gap,
								"design_uom": design_uom,
								"design_notes": design_notes,
								"design_name": image_title,
								"uoms" : uoms,
								"item_defaults" : [
									{
										"docstatus" : "0",
										"default_warehouse" : "Finished Goods - DP",
										"company" : "duraprints"
									}
								],
								"is_customer_provided_item" : compound_production.is_customer_provided_fabric,
								"customer": customer_name
							}

							//console.log(item_creation);
							//console.log(JSON.stringify(item_creation));

							if( image_title != undefined && image_title.length != 0 ){	
								//console.log("about to create item");
								frappe.call({
									url: "/api/resource/Item",
									type: "POST",
									async: false,
									args: {
										data: item_creation
									},
									callback: function(r) {
										//console.log(JSON.stringify(r));
										
										cur_frm.doc.items[i].item_code = r.data.item_code;
										cur_frm.doc.items[i].item_name = r.data.item_name;
										cur_frm.refresh_fields('items');
										
										
										//console.log(r.data);
										//console.log(r.data.item_name);
										
										sCount++;
										/*
										frappe.call({
											url: "/api/resource/BOM",
											type: "POST",
											async: false,
											args: {
												data: { 
													"item" : r.data.item_code,
													"docstatus": 1,
													"items": [
														{
															"qty": wastage_percentage,
															"item_code": compound_production.fabric_code,
															'uom': "Meter"
														},
														{
															"qty": 1,
															"item_code": compound_production.process_code,
															'uom': "Meter"
														}
													]
												}
											},
											callback: function(t) {
												console.log(JSON.stringify(r));
												cur_frm.doc.items[i].item_bom = t.data.name;
												cur_frm.refresh_fields('items');
											}
										});
										*/						
										
										
									}
								});
								
							}else{
								frappe.msgprint("Design file or design name is required on row # "+ (i+1));
								return;
							}
						}
					});
					cur_frm.save();
					if(sCount > 0){
						frappe.msgprint("Successfully created "+sCount+" items");
					}else{
						frappe.msgprint("Operation completed.");
					}
				}else{
					frappe.msgprint("Please save the document before creating items.");
				}
			});

			frm.add_custom_button(__('Create BOMs'), function(){
				var compound_production = frappe.model.get_doc(cdt, cdn);

				if(typeof compound_production.creation != 'undefined'){
					var sCount = 0;
					$.each(cur_frm.doc.items || [], function(i, row) {
						if( typeof row.item_code != 'undefined' && (typeof row.item_bom == 'undefined' || row.item_bom == "") ){
							
							console.log(row);			

							var wastage = row.wastage;
							var wastage_percentage = 1;
							if( wastage != 0 && wastage > 0 ){
								wastage_percentage = 1 + (wastage/100);
							}

							frappe.call({
								url: "/api/resource/BOM",
								type: "post",
								async: false,
								args: {
									data: { 
										"item" : row.item_code,
										"docstatus": 1, 
										"items": [
											{
												"qty": wastage_percentage,
												"item_code": compound_production.fabric_code,
												'uom': "Meter"
											},
											{
												"qty": 1,
												"item_code": compound_production.process_code,
												'uom': "Meter"
											}
										]
									}
								},
								callback: function(r) {
									//console.log(JSON.stringify(r));
									cur_frm.doc.items[i].item_bom = r.data.name;
									cur_frm.refresh_fields('items');
								}
							});

							cur_frm.save();
							
						}
					});

					frappe.msgprint("Operation completed.");
				}else{
					frappe.msgprint("Please save the document before creating items.");
				}
			});

			frm.add_custom_button(__('Create Sales Order'), function(){
				var compound_production = frappe.model.get_doc(cdt, cdn);

				if(typeof compound_production.creation != 'undefined'){
					
					var sales_order_items = [];
					var date = compound_production.date;
					var d = new Date(date);
					var delivery_date = new Date(d);
					delivery_date.setDate(delivery_date.getDate()+15);
					var missing_bom = 0;
					$.each(cur_frm.doc.items || [], function(i, row) {
						if(typeof row.item_bom == 'undefined' || row.item_bom == ""){
							missing_bom++;
						}
					});
					if(missing_bom == 0){

					
						$.each(cur_frm.doc.items || [], function(i, row) {
							if(typeof row.item_code != 'undefined' && row.item_code != ""){
								
								console.log(row);			

								var wastage = row.wastage;
								var wastage_percentage = 1;
								if( wastage != 0 && wastage > 0 ){
									wastage_percentage = 1 + (wastage/100);
								}
								sales_order_items.push({
									"item_code": row.item_code,
									"qty": 1,
									'uom': "Meter",
									'delivery_date': compound_production.date,
									'wastage_type': 'Included'
								});
							}
						});
						console.log(sales_order_items);
						
						
						frappe.call({
							url: "/api/resource/Sales Order",
							type: "POST",
							async: false,
							args: {
								data: { 
									"customer" : compound_production.customer,
									"docstatus": 0, 
									"delivery_date": compound_production.date,
									"items": sales_order_items
								}
							},
							callback: function(r) {
								console.log(JSON.stringify(r));
								//cur_frm.doc.items[i].item_bom = r.data.name;
								//cur_frm.refresh_fields('items');
							}
						});
						frappe.utils.play_sound('submit');
						frappe.msgprint("Sales Order, Created in draft mode.");
					}else{
						frappe.msgprint(missing_bom +" BOMs are missing, Please click on Create BOMs again.");
					}
				}else{
					frappe.msgprint("Please save the document before creating items.");
				}
			});
			
			

			

			
		}
	},
	customer: function(frm, cdt, cdn) {
		var compound_production = frappe.model.get_doc(cdt, cdn);
		if(typeof compound_production.customer != 'undefined'){
			frm.call({
				method: "duraprints.duraprints.doctype.compound_production.compound_production.get_customer",
				args: {
					customer: compound_production.customer
				},
				callback: function(r) {
					//console.log(r);
					frappe.model.set_value(cdt, cdn, "customer_abbreviation", r.message.customer_abbreviation);
				}
			});
		}
	},
	fabric_code: function(frm, cdt, cdn) {
		var compound_production = frappe.model.get_doc(cdt, cdn);
		var uoms = [];
		var attributes = [];
		if(typeof compound_production.fabric_code != 'undefined'){
			frm.call({
				method: "duraprints.duraprints.doctype.compound_production.compound_production.get_item_name",
				args: {
					code: compound_production.fabric_code
				},
				callback: function(r) {
					for(var i=0; i<r.message.uoms.length; i++){
						//console.log(r.message.uoms[i].uom);
						uoms[i] = {"uom" :r.message.uoms[i].uom, "conversion_factor": r.message.uoms[i].conversion_factor}
					}
					//console.log(uoms);
					if(r.message.attributes.length > 1){
						for(var i=0; i<r.message.attributes.length; i++){
							console.log(r.message.attributes[i].attribute);
							attributes[i] = {"attribute" :r.message.attributes[i].attribute, "attribute_value": r.message.attributes[i].attribute_value}
						}
					}
					//console.log(attributes);
					
					//console.log(r);
					frappe.model.set_value(cdt, cdn, "fabric_name", r.message.name);
					frappe.model.set_value(cdt, cdn, "fabric_group", r.message.group);
					frappe.model.set_value(cdt, cdn, "fabric_weight_per_unit", r.message.weight_per_unit);
					frappe.model.set_value(cdt, cdn, "fabric_uoms", JSON.stringify(uoms) );
					frappe.model.set_value(cdt, cdn, "fabric_properties", JSON.stringify(attributes) );
				}
			});
		}
	},
	process_code: function(frm, cdt, cdn) {
		var compound_production = frappe.model.get_doc(cdt, cdn);
		if(typeof compound_production.process_code != 'undefined'){
			frm.call({
				method: "duraprints.duraprints.doctype.compound_production.compound_production.get_item_name",
				args: {
					code: compound_production.process_code
				},
				callback: function(r) {
					console.log(r);
					frappe.model.set_value(cdt, cdn, "process_name", r.message.name);
				}
			});
		}
	}
});

frappe.ui.form.on("Compound Production", "before_save", function(frm,cdt, cdn) {
	var compound_production = frappe.model.get_doc(cdt, cdn);
	var custom_date = compound_production.date.split("-");
	//var item_name = compound_production.customer_abbreviation + '-' + compound_production.fabric_code + '-' + custom_date[2]+custom_date[1];
	
	var item_name = compound_production.fabric_code + '-' + custom_date[2]+custom_date[1];
	frappe.model.set_value(cdt, cdn, "title", item_name);
	
	$.each(frm.doc.items || [], function(i, d) {
		if( (d.image_name == undefined || d.image_name.length == 0) && (d.image != undefined && d.image.length != 0)){
			var filename = d.image.substring(d.image.lastIndexOf('/')+1);
			d.image_name  = filename.replace(/\.[^/.]+$/, "");
		}
	});
	//refresh_field("items");
	//frm.save();

});

function urlExists(url) {
	var http = jQuery.ajax({
	   	type:	"HEAD",
	   	url: url,
		async: false
	})
	return http.status;
		 // this will return 200 on success, and 0 or negative value on error
}