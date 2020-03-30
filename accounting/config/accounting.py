from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
      {
        "label":_("To Begin With"),
        "icon": "octicon octicon-book",
        "items": [
            {
              "type": "doctype",
              "name": "Item",
              "label": _("Item"),
              "description": _("Item Details."),
            },
            {
              "type": "doctype",
              "name": "Party",
              "label": _("Party"),
              "description": _("Party Details."),
            }
          ]
      },
      {
        "label":_("Transactions"),
        "icon": "octicon octicon-briefcase",
        "items": [
            {
              "type": "doctype",
              "name": "Invoice",
              "label": _("Invoice Entry"),
              "description": _("Invoice."),
            },
            {
              "type": "doctype",
              "name": "Journal Entry",
              "label": _("Journal Entry"),
              "description": _("Journal Entry."),
            },
            {
              "type": "doctype",
              "name": "Payment Entry",
              "label": _("Payment Entry"),
              "description": _("Stock Details."),
            },
            
          ]
      },
      {
        "label":_("Reports"),
        "icon": "octicon octicon-briefcase",
        "items": [
            {
              "type": "doctype",
              "name": "Account",
              "route": "#Tree/Account",
              "label": _("Chart Of Accounts"),
              "description": _("Stock Details."),
            },
            {
              "type": "report",
              "name": "Trial Balance",
              "route": "#query-report/Trial Balance",
              "label": _("Trial Balance"),
              "description": _("Trial Balance"),
            },
            {
              "type": "report",
              "name": "General Ledger",
              "route": "#query-report/General Ledger",
              "label": _("General Ledger"),
              "description": _("General Ledger"),
            }
          ]
      }
  ]