from frappe import _

def get_data():
    return {
        'fieldname': 'item',
        'transactions': [
            {
                'label': _('Invoices'),
                'items': ['Invoice']
            }
        ]
    }