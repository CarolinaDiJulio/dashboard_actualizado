from datetime import datetime, timedelta
from odoo import api, models, fields

class objetivos(models.Model):
    _name = 'objetivos'
    _description = 'objetivos de la linea de trabajo'

    timestamp= fields.Date(string = 'Fecha:',required=True, default=fields.Date.today())
    dia = fields.Char(string = 'Dia:', compute='_compute_dia', store=True)
    objetivo = fields.Char(string = 'Objetivo:')
    cantidad = fields.Integer(string = 'Cantidad:', default = 0)
 
    @api.depends('timestamp')
    def _compute_dia(self):
        dias_en_espanol = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo'
        }
        for record in self:
            if record.timestamp:
                record.dia = dias_en_espanol[record.timestamp.weekday()]
            else:
                record.dia = False
    @api.onchange('timestamp')
    def _onchange_timestamp(self):
            dias_en_espanol = {
                0: 'Lunes',
                1: 'Martes',
                2: 'Miércoles',
                3: 'Jueves',
                4: 'Viernes',
                5: 'Sábado',
                6: 'Domingo'
            }
            for record in self:
                if record.timestamp:
                    dia_semana_num = record.timestamp.weekday()
                    record.dia = dias_en_espanol[dia_semana_num]