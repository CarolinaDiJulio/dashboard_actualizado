from odoo import models, fields

class Operators(models.Model):
    _name = 'operators'
    _description = 'Línea de trabajo de valizas'
    # Campos del modelo:
    name = fields.Char(string='Nombre', required=True)
    surname = fields.Char(string='Apellidos')
    dni = fields.Char(string='DNI', required=True)
    phone = fields.Char(string='Teléfono')