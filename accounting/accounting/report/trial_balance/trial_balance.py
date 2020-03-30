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
			# 'options': frappe.get_all('Account', filters={'is_group': 0}),
			'width': 200
		},
		{
			'label': 'Credit',
			'fieldname': 'credit',
			'fieldtype': 'Currency',
			'default': 0,
			'width': 200
		},
		{
			'label': 'Debit',
			'fieldname': 'debit',
			'fieldtype': 'Currency',
			'default': 0,
			'width': 200
		}
	]
	
	accounts = frappe.get_all('Account', filters={'is_group': 0})
	total_credit = 0
	total_debit = 0
	
	fiscal_year = frappe.get_doc('Fiscal Year', filters['fiscal_year'])
	start_date = str(fiscal_year.start_date)
	end_date = str(fiscal_year.end_date)
	
	empty = False
	for x in accounts:
		try:
			credit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` WHERE posting_date >= '" + \
				start_date + "' AND posting_date <= '" + end_date + "' GROUP BY account HAVING account='"+x.name + \
				"'")[0][0]
			debit = frappe.db.sql("Select SUM(debit_amount) FROM `tabGL Entry` WHERE posting_date >= '" + \
				start_date + "' AND posting_date <= '" + end_date + "' GROUP BY account HAVING account='"+x.name + \
				"'")[0][0]
		except:
			empty = True
			break
		data.append({
			'account': x.name,
			'credit': credit,
			'debit': debit
		})
		
		total_credit += credit
		total_debit += debit

	if empty:
		frappe.throw('No records for this year!')
	else:	
		data.append({
			'account': '<b>Totals</b>',
			'credit': total_credit,
			'debit': total_debit
		})
		
	return columns, data

# def get_balance(account):
	# frappe.db.sql("Select SUM(debit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]
	# frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]