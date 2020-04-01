# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.report.general_ledger.general_ledger import get_balance, make_entry

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
		self.make_gl_entries(is_submit=True)
	
	def on_cancel(self):
		self.make_gl_entries(is_submit=False)

	def make_gl_entries(self, is_submit=True):
		doc_list = []
		remarks = 'Journal Entry for ' + self.name
		if not is_submit:
			remarks += 'Reverse ' + remarks
		for e in self.accounting_entries:
			doc = {
				'doctype': 'GL Entry',
				'posting_date': self.posting_date,
				'account': e.account,
				'debit_amount': e.debit if is_submit else e.credit,
				'credit_amount': e.credit if is_submit else e.debit,
				'balance': get_balance(e.account, e.debit, e.credit),
				'voucher_type': 'Journal Entry',
				'voucher_number': self.name,
				'party_type': '',
				'party': e.party_name,
				'against_voucher_type': '',
				'against_voucher_number': '',
				'remarks': remarks
			}
			doc_list.append(doc)
		make_entry(doc_list)
