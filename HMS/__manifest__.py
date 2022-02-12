{
    'name': 'Hospital Management System',
    'description': 'Management system to manage patients data',
    'depends': ['base', 'crm'],
    'data': [
        'views/patient_view.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/crm_inherited_view.xml',
    ]
}