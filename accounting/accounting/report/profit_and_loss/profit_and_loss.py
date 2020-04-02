# Copyright (c) 2013, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = [
		{
			'label': 'Account',
			'fieldname': 'account',
			'fieldtype': 'Data',
			'width': 200
		},
		{
			'label': 'Balance (INR)',
			'fieldname': 'balance',
			'fieldtype': 'Currency',
			'default': 0,
			'width': 200
		}
	]
	
	accounts = frappe.get_all('Account', filters={'is_group': 0})
	accounts = ['Sales', 'Purchases']
	fiscal_year = frappe.get_doc('Fiscal Year', filters['fiscal_year'])
	start_date = str(fiscal_year.start_date)
	end_date = str(fiscal_year.end_date)
	
	all_balances = []
	for name in accounts:
		try:
			balance = abs(frappe.db.sql("Select SUM(debit_amount) - SUM(credit_amount) FROM `tabGL Entry` WHERE posting_date >= '" + \
				start_date + "' AND posting_date <= '" + end_date + "' GROUP BY account HAVING account='"+ name + \
				"'")[0][0])
		except:
			balance = 0

		data.append({
			'account': name,	
			'balance': balance,
			'indent': 1.0
		})
		all_balances.append(balance)

	data.insert(0, {
		'account': '<span style="font-weight:500">Income (Credit)</span>',
		'balance': '',
		'indent': 0.0
	})
	data.insert(2, {
		'account': '<span style="font-weight:500">Expenses (Debit)</span>',
		'balance': '',
		'indent': 0.0
	})
	p_or_f = all_balances[0] - all_balances[1]
	data.append({
		'account': '<b style="color:green">Profit</b>' if p_or_f >=0 else '<b style="color:red">Loss</b>' ,
		'balance': abs(p_or_f),
		'indent': 0.0
	})

	return columns, data
