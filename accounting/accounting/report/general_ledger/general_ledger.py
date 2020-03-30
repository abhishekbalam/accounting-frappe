from __future__ import unicode_literals
import frappe

def get_columns(filters):
	doc_fields = frappe.get_meta('GL Entry').fields
	columns = []
	for x in doc_fields:
		width = 120
		if 'against_voucher' in x.fieldname:
			width = 180
		if x.fieldname == 'amended_from':
			continue
		col = {
			'label': x.label,
			'fieldname': x.fieldname,
			'fieldtype': x.fieldtype,
			'options': x.options,
			'width': width
		}
		columns.append(col)
	return columns

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	fieldnames = [ x['fieldname'] for x in columns ]

	query = "SELECT "
	for i in range(0, len(fieldnames)):
		query += fieldnames[i]
		if i != (len(fieldnames) - 1):
			query += ","
	query += " FROM `tabGL Entry` WHERE posting_date >= '" + \
			filters['from_date'] + "' AND posting_date <= '" + filters['to_date'] + \
			"' ORDER BY name DESC"
	print(query)
	result = frappe.db.sql(query)
	
	for x in range(0, len(result)):
		doc = {}
		for y in range(0, len(fieldnames)):
			doc[fieldnames[y]] = result[x][y]
		data.append(doc)
	
	return columns, data

def get_balance(account, debit, credit):
	try:
		total_debit = frappe.db.sql('''
			SELECT SUM(debit_amount)
			FROM `tabGL Entry`
			GROUP BY account
			HAVING account=%s''', account)[0][0]
		total_credit = frappe.db.sql('''
			SELECT SUM(credit_amount)
			FROM `tabGL Entry` 
			GROUP BY account 
			HAVING account=%s''', account)[0][0]
		return (total_debit+int(debit)) - (total_credit+int(credit))
	except:
		# print(debit, credit)
		return int(debit) - int(credit)	

def make_entry(doc_list):
	for d in doc_list:
		doc = frappe.get_doc(d)
		doc.insert()
		doc.submit()
