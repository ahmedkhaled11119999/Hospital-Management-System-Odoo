{
    'name': 'Hospital Management System',
    'description': 'Management system to manage patients data',
    'depends': ['base', 'crm'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/crm_inherited_view.xml',
        'reports/report.xml',
        'reports/templates.xml'
    ]
}