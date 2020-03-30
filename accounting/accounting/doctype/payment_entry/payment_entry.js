// Copyright (c) 2020, Abhishek Balam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	onload: function(frm) {
	    frm.trigger('query_for_type');
		frm.set_query('from_account', function() {
		    return {
		        filters: [
		                ['Account', 'is_group', '=', 0]
		            ]
		    };
		});
		frm.set_query('to_account', function() {
		    return {
		        filters: [
		                ['Account', 'is_group', '=', 0]
		            ]
		    };
		});
	},
	entry_type: function(frm, cdt, cdn) {
		frm.set_value('invoice', '');
		frm.set_value('party_name', '');
		frm.set_value('party_type', '');
		frm.set_value('amount_due', '');
		
		if (frm.doc.entry_type !== 'Internal Transfer'){
			frm.trigger('query_for_type');
		}
		else {
			frm.set_value('from_account', '')
			frm.set_value('to_account', '')
		}
	},
	query_for_type: function(frm){
		let invoice_type = (frm.doc.entry_type == 'Pay') ? 'Purchase' : 'Sales';
		frm.set_query('invoice', function() {
		    return {
		        filters: [
						['Invoice', 'invoice_type', '=', invoice_type],
						['Invoice', 'status', '=', 'Unpaid'],
						['Invoice', 'docstatus', '!=', 2]
		            ]
		    }
		});
		if(invoice_type == 'Purchase'){
			frm.set_value('from_account', 'Cash In Hand')
			frm.set_value('to_account', 'Creditors')
		}
		else {
			frm.set_value('from_account', 'Debtors')
			frm.set_value('to_account', 'Cash In Hand')
		}
	},
	party_name: function(frm, cdt, cdn){
		let invoice = frm.doc.party_name;
		if (invoice.indexOf('(S)') !== -1) {
			frm.set_value('party_type', 'Supplier');
		}
		else if(invoice.indexOf('(C)') !== -1) {
			frm.set_value('party_type', 'Customer');
		}
		frm.refresh_field('party_type');
	}
});