// Copyright (c) 2016, Abhishek Balam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Trial Balance'] = {
	'filters': [
		{
			'fieldname':'fiscal_year',
			'label': __('Fiscal Year'),
			'fieldtype': 'Link',
			'options': 'Fiscal Year',
			'reqd': 1,
			'default': '2019-2020',
			'width': '100px',
			get_data: function(txt) {
				return frappe.db.get_link_options('Fiscal Year', txt);
			}
		}
	]
	// "formatter": function(value, row, column, data, default_formatter) {
	// 	if (column.fieldname=="account") {
	// 		value = data.account_name || value;
	// 		// column.link_onclick =
	// 			// "erpnext.financial_statements.open_general_ledger(" + JSON.stringify(data) + ")";
	// 		column.is_tree = true;
	// 	}
	// 	value = default_formatter(value, row, column, data);

	// 	if (!data.parent_account) {
	// 		value = $(`<span>${value}</span>`);

	// 		var $value = $(value).css("font-weight", "bold");
	// 		if (data.warn_if_negative && data[column.fieldname] < 0) {
	// 			$value.addClass("text-danger");
	// 		}

	// 		value = $value.wrap("<p></p>").parent().html();
	// 	}
	// 	return value;
	// },
	// "tree": true,
	// "name_field": "account",
	// "parent_field": "parent_account",
	// "initial_depth": 1
};