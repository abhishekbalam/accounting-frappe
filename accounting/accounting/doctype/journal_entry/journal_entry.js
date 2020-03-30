// Copyright (c) 2020, Abhishek Balam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	setup: function(frm) {
		frm.fields_dict['accounting_entries'].grid.get_field('account').get_query = function(doc, cdt, cdn) {
		return {
					filters: [
						['Account', 'is_group', '=', 0]
					]
				}
		}

	},
	validate: function(frm){
		var total_credit = 0;
		var total_debit = 0;
		
		frm.doc.accounting_entries.forEach(element => {
			total_credit += element.credit;
			total_debit += element.debit;
		});
		
		if(total_credit !== total_debit){
			frappe.throw('Total Credit should be equal to Total Debit!');
		}
		else{
			frm.set_value('total_credit', total_credit);
			frm.set_value('total_debit', total_debit);
		}
	}
});

frappe.ui.form.on('Journal Entry Account', {
	party_name: function(frm, cdt, cdn){
		let row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'party_type', '');
		let invoice = row.party_name;
		if(invoice !== undefined){
			if (invoice.indexOf('(S)') !== -1) {
				row.party_type = 'Supplier';
			}
			else if(invoice.indexOf('(C)') !== -1) {
				row.party_type = 'Customer'
			}
		}
	}
});
