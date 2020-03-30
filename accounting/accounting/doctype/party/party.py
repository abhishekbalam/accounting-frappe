# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class Party(Document):

	def autoname(self):
		self.name = self.party_name + " (" + self.party_type[0] + ")"
		print(self.name)