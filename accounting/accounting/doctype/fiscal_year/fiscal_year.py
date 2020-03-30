# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import time

class FiscalYear(Document):
	def autoname(self):
		year = self.start_date.split('-')[0]+'-'+self.end_date.split('-')[0]
		self.name = year
		
	def validate(self):
		if  time.strptime(self.end_date, '%Y-%m-%d') < time.strptime(self.start_date, '%Y-%m-%d'):
			frappe.throw('End date has to be greater than start date.')
		
