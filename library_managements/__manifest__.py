{
    'name': 'Library Borrowing',
    'summary': 'Manage members, books, borrowing, and returns',
    'version': '19.0.2.1.0',
    'category': 'Services/Library',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_member_views.xml',
        'views/library_loan_views.xml',
        'views/library_book_views.xml',
        'views/library_management_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 6,
    'license': 'LGPL-3',
}
