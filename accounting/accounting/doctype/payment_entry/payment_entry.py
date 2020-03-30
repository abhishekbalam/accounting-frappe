# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe

class PaymentEntry(Document):

	def autoname(self):
		count = frappe.db.count('Payment Entry')
		count += 1
		self.name = 'PE-' + str(count).zfill(4)

	def on_submit(self):
		docs = {}
		common_doc = {
			'doctype': 'GL Entry',
			'posting_date': self.payment_date,
			'voucher_type': 'Payment Entry',
			'voucher_number': self.name,
			'party': self.party_name,
			'against_voucher_number': self.invoice,
		}
		if self.entry_type == 'Pay':
			docs = [
				{
					'account': 'Cash In Hand',
					'debit_amount': self.payment_amount,
					'credit_amount': 0,
				},
				{
					'account': 'Creditors',
					'debit_amount': 0,
					'credit_amount': self.payment_amount,
				}
			]
			for x in docs:
				x.update({
					'party_type': 'Supplier',
					'against_voucher_type': 'Purchase Invoice',
				})
				x.update(common_doc)
		else:
			docs = [
				{
					'account': 'Debtors',
					'debit_amount': self.payment_amount,
					'credit_amount': 0,
				},
				{
					'account': 'Cash In Hand',
					'debit_amount': 0,
					'credit_amount': self.payment_amount,
				}
			]
			for x in docs:
				x.update({
					'party_type': 'Customer',
					'against_voucher_type': 'Sales Invoice',
				})
				x.update(common_doc)

		for x in docs:
			print(x['debit_amount'], x['credit_amount'], x['account'])
			bal = self.get_balance(x['account'], x['debit_amount'], x['credit_amount'])
			x['balance'] = bal
			x = frappe.get_doc(x)
			x.insert()
			x.submit()
		
		invoice_doc = frappe.get_doc('Invoice', self.invoice)
		invoice_doc.amount_due = str(int(invoice_doc.amount_due) - self.payment_amount)
		if int(invoice_doc.amount_due) == 0:
			invoice_doc.status = 'Paid'
		invoice_doc.save()
	
	def on_cancel(self):
		# Bug hain, revisit.
		docs = {}
		common_doc = {
			'doctype': 'GL Entry',
			'posting_date': self.payment_date,
			'voucher_type': 'Payment Entry',
			'voucher_number': self.name,
			'party': self.party_name,
			'against_voucher_number': self.invoice,
		}
		if self.entry_type == 'Pay':
			docs = [
				{
					'account': 'Cash In Hand',
					'debit_amount': 0,
					'credit_amount': self.payment_amount,
				},
				{
					'account': 'Creditors',
					'debit_amount': self.payment_amount,
					'credit_amount': 0,
				}
			]
			for x in docs:
				x.update({
					'party_type': 'Supplier',
					'against_voucher_type': 'Purchase Invoice',
				})
				x.update(common_doc)
		else:
			docs = [
				{
					'account': 'Debtors',
					'debit_amount': 0,
					'credit_amount': self.payment_amount,
				},
				{
					'account': 'Cash In Hand',
					'debit_amount': self.payment_amount,
					'credit_amount': 0,
				}
			]
			for x in docs:
				x.update({
					'party_type': 'Customer',
					'against_voucher_type': 'Sales Invoice',
				})
				x.update(common_doc)

		for x in docs:
			print(x['debit_amount'], x['credit_amount'], x['account'])
			bal = self.get_balance(x['account'], x['debit_amount'], x['credit_amount'])
			x['balance'] = bal
			x = frappe.get_doc(x)
			x.insert()
			x.submit()
		

	def get_balance(self, account, debit, credit):
		try:
			total_debit = frappe.db.sql("Select SUM(debit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]
			total_credit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+account+"'")[0][0]
			return (total_debit+int(debit)) - (total_credit+int(credit))
		except:
			return int(debit) - int(credit)
		