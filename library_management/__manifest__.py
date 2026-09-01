{
    'name':'Library Management',
    'version':'1.0',
    'category':'student',
    'author':'Pyae Sone',
    'depends':['contacts'],
    'data':[
        # Security
        'security/ir.model.access.csv',
        'security/library_security.xml',
        # Sequence & Data
        'data/library_sequence.xml',
        'data/library_demo_data.xml', 
        # Wizard
        'wizard/book_report_wizard_view.xml',
        # View
        'views/library_book_views.xml',
        'views/res_partner_views.xml',
        'views/library_category_views.xml',
        'views/library_author_views.xml',
        'views/library_borrow_views.xml',
        # Menu
        'views/library_menu.xml',
    ],
    'installable':True,
    'application':True,
    'auto_install':False,
    'sequence':1,
}