# -*- coding: utf-8 -*-
{
    'name': 'Linea',
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

    ],
    "data": [
        "security/ir.model.access.csv",
        "views/linea_views.xml",
        "views/menus.xml",
        "views/linea_qweb_views.xml",
        "views/objetivos_views.xml",
    ],
    'installable': True,     # Habilita la instalación del módulo
    'application': True,     # Especifica que el módulo es una aplicación
    'assets': {
         'website.assets_frontend': [
                'linea/static/src/css/style.css', 
            ],
    },
    'license': 'LGPL-3',     # Licencia del módulo, ajusta según sea necesario
}
