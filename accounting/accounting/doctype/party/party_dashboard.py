from frappe import _

def get_data():
    return {
        'fieldname': 'party_name',
        'transactions': [
            {
                'label': _('Accounting'),
                'items': ['Payment Entry', 'Invoice']
            }
        ]
    }