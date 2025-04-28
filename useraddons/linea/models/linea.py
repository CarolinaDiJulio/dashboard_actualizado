from odoo import models, fields

class linea(models.Model):
    _name = 'linea'
    _description = 'linea de trabajo'

    timestamp = fields.Datetime(string = 'Fecha de creación', default=fields.Datetime.now)
    puesto =fields.Selection(
                selection=[
                    ('1', 'Puesto 1'),
                    ('2', 'Puesto 2'),
                    ('3', 'Puesto 3'),
                    ('4', 'Puesto 4'),
                    ('5', 'Puesto 5'),
                ],
                string='Puesto',
                required=True,
            )
    imei = fields.Char(string = 'IMEI')