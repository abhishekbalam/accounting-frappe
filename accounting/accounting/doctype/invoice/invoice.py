# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.tdt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import time
from accounting.accounting.report.general_ledger.general_ledger import get_balance
from accounting.accounting.report.general_ledger.general_ledger import make_entry

class Invoice(Document):
	
	def validate(self):
		if time.strptime(self.issue_date, '%Y-%m-%d') > time.strptime(self.due_date, '%Y-%m-%d'):
			frappe.throw('Due Date has to be greater than Issue Date!')
		self.amount_due = 0
		for it in self.item_list:
			self.amount_due += it.amount
		self.verify_quantity()
		
	def autoname(self):
		count = frappe.db.count('Invoice', {'invoice_type': self.invoice_type }) + 1 
		self.name = self.invoice_type[0] + 'INV-' + str(count).zfill(4)
	
	def on_update(self):
		total_amount = 0
		for item in self.item_list:
			total_amount += item.amount
		if self.amount_due != total_amount:
			self.amount_due = total_amount

	def on_submit(self):
		self.verify_quantity()
		self.update_quantity(to_submit=True)
		self.make_gl_entry(to_submit=True)
		
	def on_cancel(self):
		self.update_quantity(to_submit=False)
		self.make_gl_entry(to_submit=False)
	
	def make_gl_entry(self, to_submit):
		amounts = [self.amount_due, 0]
		accounts = ['Creditors', 'Purchases', 'Sales', 'Debtors']
		is_purchase = (self.invoice_type == 'Purchase')
		remarks = (self.invoice_type + ' Invoice entry for ' + self.name) if to_submit else 'Reverse Entry for ' \
			+ self.invoice_type + ' Invoice - ' + self.name 

		common_doc = {
			'doctype': 'GL Entry',
			'posting_date': self.issue_date,
			'voucher_type': self.invoice_type + ' Invoice Entry',
			'voucher_number': self.name,
			'party': self.party_name,
			'remarks': remarks,
			'party_type' : 'Supplier' if is_purchase else 'Customer'
		}
		
		docs = []
		for i in [0, 1]:
			entry = common_doc.copy()
			entry.update({
				'account': accounts[0:2][i] if is_purchase else accounts[2:4][i],
				'credit_amount': amounts[i] if to_submit else amounts[int(not bool(i))],
				'debit_amount': amounts[int(not bool(i))] if to_submit else amounts[i],
			})
			print(i, entry['debit_amount'], entry['credit_amount'])
			entry['balance'] = get_balance(entry['account'], entry['debit_amount'], entry['credit_amount'])
			docs.append(entry)
		make_entry(docs)

	def verify_quantity(self):
		if self.invoice_type == 'Sales':
			for it in self.item_list:
				itemdoc = frappe.get_doc('Item', it.item)
				if it.quantity == 0:
					frappe.throw('Quantity cannot be 0!')
				if it.quantity > itemdoc.item_quantity:
					frappe.throw(it.item + ' quantity cannot exceed quantity in stock: ' + str(itemdoc.item_quantity))
				
	def update_quantity(self, to_submit):
		is_purchase = (self.invoice_type == 'Purchase')
		to_increase = not (is_purchase ^ to_submit)

		for it in self.item_list:
			itemdoc = frappe.get_doc('Item', it.item)
			itemdoc.item_quantity += it.quantity * (1 if to_increase else -1)
			itemdoc.save()
	