// Copyright (c) 2020, Abhishek Balam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice', {
	onload: function(frm) {
		frm.set_query('item' ,'item_list', () => {
			if (frm.doc.invoice_type == 'Purchase') {
				return {
					filters: {
						'item_supplier': frm.doc.party_name,
					}
				}
			}
			else {
				return {
					filters: [
						['item_quantity', '!=', '0']
					]
				}
			}
		});
		frm.trigger('query_for_party');
	},
	invoice_type: function(frm) {
		frm.set_value('party_name','');
		frm.fields_dict.item_list.frm.clear_table('item_list');
		frm.fields_dict.item_list.frm.refresh_fields();
		frm.trigger('query_for_party');
	},
	validate: function(frm){
		if (frappe.datetime.get_day_diff(frm.doc.due_date, frm.doc.issue_date) <= 0){
			frm.set_value('issue_date', '');
			frm.set_value('due_date', '');
			frappe.throw('Due Date has to be greater than Issue Date!')
		}
	},
	query_for_party: function(frm){
		var party_type = (frm.doc.invoice_type == 'Sales') ? 'customer' : 'supplier';
		frm.set_query('party_name', function() {
		    return {
		        filters: [
		                ['Party', 'party_type', '=', party_type]
		            ]
		    }
		});
		if (frm.doc.invoice_type == 'Purchase'){
			frm.fields_dict.item_list.frm.add_fetch('item', 'cost_price', 'rate');
		}
		else{
			frm.fields_dict.item_list.frm.add_fetch('item', 'selling_price', 'rate');
		}
	}
});

frappe.ui.form.on('Invoice Item', {
	amount: function(frm){
		frm.trigger('check_quantity');
		frm.trigger('calculate_due');
	},
	quantity: function(frm, cdt, cdn) {
			let row = locals[cdt][cdn];
			if (frm.doc.invoice_type == "Sales"){
				frappe.db.get_value('Item', {name: row.item }, 'item_quantity', (r) => {
					let max_qty = r['item_quantity'];
					if(row.quantity > max_qty){
						frappe.model.set_value(cdt, cdn, 'quantity', '');
						frappe.throw(row.item + ' quantity cannot exceed quantity in stock: ' + String(max_qty));
					}
				}, row.item);
			}
			let amount = row.quantity * row.rate;
			frappe.model.set_value(cdt, cdn, 'amount', amount);
	},
	calculate_due: function(frm){
		var total_amount = 0;
		frm.doc.item_list.forEach(element => {
			total_amount += element.amount;
		});
		frm.set_value('amount_due', total_amount);
		frm.refresh_field('amount_due');	
	}
});