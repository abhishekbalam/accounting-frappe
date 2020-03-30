// Copyright (c) 2020, Abhishek Balam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item', {
	refresh: function(frm) {
		frm.set_query("item_supplier", function(){
			return {
				filters: [
					["party_type", "=", "supplier"]
				]
			}
		})
	}
});
