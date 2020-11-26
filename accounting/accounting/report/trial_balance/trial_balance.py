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
			'label': 'Credit (INR)',
			'fieldname': 'credit',
			'fieldtype': 'Currency',
			'options': 'INR',
			'default': 0,
			'width': 200
		},
		{
			'label': 'Debit (INR)',
			'fieldname': 'debit',
			'fieldtype': 'Currency',
			'options': 'INR',
			'default': 0,
			'width': 200
		}
	]

	# accounts_old = frappe.get_all('Account', filters=[['name', '!=', 'Gada Electronics']], fields=['name', 'is_group'])
	accounts = get_accounts()
	total_credit = 0
	total_debit = 0

	fiscal_year = frappe.get_doc('Fiscal Year', filters['fiscal_year'])
	start_date = str(fiscal_year.start_date)
	end_date = str(fiscal_year.end_date)

	for x in accounts:
		data.append({
			'account': '<b>' + x['group'] + '</b>',
			'credit': '',
			'debit': '',
			'indent': 0.0
		})
		for acc in x['accounts']:
			try:
				credit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` WHERE posting_date >= '" + \
					start_date + "' AND posting_date <= '" + end_date + "' GROUP BY account HAVING account='"+acc+ \
					"'")[0][0]
			except:
				credit = 0
			try:
				debit = frappe.db.sql("Select SUM(debit_amount) FROM `tabGL Entry` WHERE posting_date >= '" + \
					start_date + "' AND posting_date <= '" + end_date + "' GROUP BY account HAVING account='"+acc+ \
					"'")[0][0]
			except:
				debit = 0
			total_credit += credit
			total_debit += debit
			data.append({
				'account': acc,
				'credit': credit,
				'debit': debit,
				'indent': 1.0
			})

	data.append({
		'account': '<b>Totals</b>',
		'credit': total_credit,
		'debit': total_debit,
		'parent_account': ''
	})
	return columns, data

def get_accounts():
	group_accounts = frappe.get_list('Account', filters=[['name', '!=', 'Gada Electronics'], ['is_group', '=', '1']])
	group_list = []
	for x in group_accounts:
		group_list.append({
			'group': x.name,
			'accounts': [x.name for x in frappe.get_list('Account', filters={'parent_account': x.name})]
		})
	return group_list