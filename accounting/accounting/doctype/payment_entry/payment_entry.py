# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.report.general_ledger.general_ledger import get_balance, make_entry

class PaymentEntry(Document):

	def autoname(self):
		count = frappe.db.count('Payment Entry') + 1
		self.name = 'PE-' + str(count).zfill(4)
	
	def on_submit(self):
		self.make_gl_entry(to_submit=True)
		self.update_amount_due(to_submit=True)
		
	def on_cancel(self):
		self.make_gl_entry(to_submit=False)
		self.update_amount_due(to_submit=False)
		
	def make_gl_entry(self, to_submit):
		amounts = [self.amount_due, 0]
		accounts = ['Cash In Hand', 'Creditors', 'Debtors', 'Cash In Hand']
		to_pay = (self.entry_type == 'Pay')
		remarks = ('Payment Entry for ' + self.invoice)
		if not to_submit:
			remarks = 'Reverse ' + remarks
		
		common_doc = {
			'doctype': 'GL Entry',
			'posting_date': self.payment_date,
			'voucher_type': 'Payment Entry',
			'voucher_number': self.name,
			'party': self.party_name,
			'remarks': remarks,
			'party_type' : 'Supplier' if to_pay else 'Customer',
			'against_voucher_type': ('Purchase' if to_pay else 'Sales') + ' Invoice',
			'against_voucher_number': self.invoice
		}
		docs = []
		for i in [0, 1]:
			entry = common_doc.copy()
			entry.update({
				'account': accounts[0:2][i] if to_pay else accounts[2:4][i],
				'credit_amount': amounts[i] if to_submit else amounts[int(not bool(i))],
				'debit_amount': amounts[int(not bool(i))] if to_submit else amounts[i],
			})
			print(i, entry['debit_amount'], entry['credit_amount'])
			entry['balance'] = get_balance(entry['account'], entry['debit_amount'], entry['credit_amount'])
			docs.append(entry)

		make_entry(docs)
	
	def update_amount_due(self, to_submit):
		invoice = frappe.get_doc('Invoice', self.invoice)
		total_due = 0
		for it in invoice.item_list:
			total_due += it.amount
		invoice.amount_due += self.payment_amount * (-1 if to_submit else 1)
		
		if invoice.amount_due == 0:
			invoice.payment_status = 'Paid'
		else:
			invoice.payment_status = 'Unpaid'
		
		invoice.save()
