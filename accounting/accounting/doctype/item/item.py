# -*- coding: utf-8 -*-
# Copyright (c) 2020, Abhishek Balam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe

class Item(Document):
	def autoname(self):
		self.name = self.item_name + " (" + self.item_supplier[:-3] + ")"


def after_doctype_insert():
	frappe.db.add_unique("Item", ("item_name","item_supplier"))
