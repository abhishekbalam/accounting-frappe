# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JournalEntry(Document):
	def autoname(self):
		count = frappe.db.count('Journal Entry')
		count += 1
		self.name = 'JE-' + str(count).zfill(4)
	
	def validate(self):
		entries = self.accounting_entries
		total_credit = 0
		total_debit = 0
		for e in entries:
			total_credit += e.credit
			total_debit += e.debit
		
		if total_credit != total_debit:
			frappe.throw('Total Credit should be equal to Total Debit!')
		else:
			self.total_credit = total_credit
			self.total_debit = total_debit

	def on_submit(self):
		for e in self.accounting_entries:
			doc = frappe.get_doc({
				'doctype': 'GL Entry',
				'posting_date': self.posting_date,
				'account': e.account,
				'debit_amount': e.debit,
				'credit_amount': e.credit,
				'balance': self.get_balance(e.account, e.debit, e.credit),
				'voucher_type': 'Journal Entry',
				'voucher_number': self.name,
				'party_type': '',
				'party': e.party_name,
				'against_voucher_type': '',
				'against_voucher_number': '',
			})
			doc.insert()
			doc.submit()
	
	def on_cancel(self):
		for e in self.accounting_entries:
			doc = frappe.get_doc({
				'doctype': 'GL Entry',
				'status': 'Cancelled',
				'posting_date': self.posting_date,
				'account': e.account,
				'debit_amount': e.credit, # Reverse
				'credit_amount': e.debit, # Reverse
				'balance': self.get_balance(e.account, e.credit, e.debit),
				'voucher_type': 'Journal Entry',
				'voucher_number': self.name,
				'party_type': '',
				'party': e.party_name,
				'against_voucher_type': '',
				'against_voucher_number': '',
			})
			doc.insert()
			doc.submit()

	def get_balance(self, account, debit, credit):
		try:
			total_debit = frappe.db.sql("Select SUM(debit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]
			total_credit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]
			return (total_debit+int(debit)) - (total_credit+int(credit))
		except:
			return int(debit) - int(credit)
		