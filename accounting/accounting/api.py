from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_accounts():
	accounts = frappe.get_all('Account', limit=0, filters={'is_group': 0})
	accounts = [ x for x,y in accounts]
	return accounts