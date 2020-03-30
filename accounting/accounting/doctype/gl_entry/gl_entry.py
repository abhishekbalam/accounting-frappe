# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class GLEntry(Document):
	def autoname(self):
		count = frappe.db.count('GL Entry')
		count += 1
		self.name = 'GL' + str(count).zfill(7)
	
	def on_submit(self):
		pass
		# self.balance = 100
		# credit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+self.account+"'")[0][0]
		# debit = frappe.db.sql("Select SUM(credit_amount) FROM `tabGL Entry` GROUP BY account HAVING account='"+self.account+"'")[0][0]
		# account_balance = debit - credit
		# self.balance = account_balance
		# print(credit, debit, account_balance, self.balance)