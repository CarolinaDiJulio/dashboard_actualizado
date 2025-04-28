# -*- coding: utf-8 -*-
{
    'name': 'Practice',
    'version': '1.0',
    'summary': 'Muestra el estado de la línea',
    'description': """
        Este módulo proporciona un dashboard con información sobre los usuarios.
    """,
    'author': 'D2PLUS',
    'website': 'https://www.d2plus.com',  # Opcional
    'category': 'Manufacturing',
    'sequence': 25,  # Orden en el menú de aplicaciones
    'depends': [
        'base',   # Dependencia principal para usar el modelo base
        'web',    # Dependencia para la interfaz web de Odoo
        'website', # Dependencia para el sitio web de Odoo
        'hr',     # Dependencia para el módulo de recursos humanos
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/operators_views.xml",
        "views/schedules_views.xml",
        "views/ingresar_views.xml",
        "views/empleados_views.xml",
        "views/error_views.xml",
        "views/registro_correcto_views.xml",
    ],
    'installable': True,     # Habilita la instalación del módulo
    'application': True,     # Especifica que el módulo es una aplicación
    'assets': {
        'website.assets_frontend': [
                'practice/static/src/js/my_script.js',  # Ruta a tu archivo JS
            ],
    },
    'license': 'LGPL-3',     # Licencia del módulo, ajusta según sea necesario
}
