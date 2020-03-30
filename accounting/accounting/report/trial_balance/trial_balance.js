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
};