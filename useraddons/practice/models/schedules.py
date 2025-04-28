from odoo.exceptions import ValidationError
from odoo import api, models, fields

class Schedules (models.Model):
    _name = 'schedules'
    _description = 'Línea de trabajo de valizas'
    _sql_constraints = [('operario_horario_unico','UNIQUE(usuario_id,fecha)','El operario ya tiene un horario asignado ese día'),
                        ('horario_laboral_maximo','CHECK(EXTRACT(EPOCH FROM hora_salida-hora_entrada)<=(16*3600))','El operario no puede trabajar más de 16 horas'),
                        ('horario_laboral_minimo', 'CHECK(EXTRACT(EPOCH FROM hora_salida - hora_entrada) >= 0)', 'La hora de salida no puede ser anterior a la hora de entrada')]
    
    # Campos del modelo:
    hora_entrada = fields.Datetime(string='Hora de entrada')
    hora_salida = fields.Datetime(string='Hora de salida')
    usuario_id = fields.Many2one('hr.employee',string='Usuario', required=True)
    
    #campos calculados:    
    horas_trabajadas_formateadas = fields.Char(string='Horas', compute='_formatear_horas', store=True)
    horas_trabajadas= fields.Float(string='Horas trabajadas', compute='_calcular_horas_trabajadas', store=True)
    fecha = fields.Date(string='Fecha', store=True, compute='_calcular_fecha')

    # api
    @api.model
    def create_schedule(self, user_id, hora_entrada,hora_salida):
        fecha = hora_entrada.date() if hora_entrada else False
        schedule = self.create({
            'usuario_id': user_id,
            'hora_entrada': hora_entrada,
            'hora_salida': hora_salida,
            'fecha': fecha
        })
        return schedule
    
    @api.depends('hora_entrada', 'hora_salida')
    def _calcular_horas_trabajadas(self):
        for record in self:
            if record.hora_entrada and record.hora_salida:
                # Calculamos la diferencia en horas
                diferencia = record.hora_salida - record.hora_entrada
                record.horas_trabajadas = diferencia.total_seconds() / 3600  # Convertir de segundos a horas
            else:
                record.horas_trabajadas = 0.0  # Si no hay hora de entrada o salida, las horas trabajadas son 0

    @api.depends('hora_entrada')
    def _calcular_fecha(self):
        for record in self:
            record.fecha = record.hora_entrada.date() if record.hora_entrada else False

    @api.depends('horas_trabajadas')
    def _formatear_horas(self):
        for record in self:
            if record.horas_trabajadas:
                horas = int(record.horas_trabajadas)
                minutos = int((record.horas_trabajadas - horas) * 60)
                record.horas_trabajadas_formateadas = f'{horas}h {minutos}m'
            else:
                record.horas_trabajadas_formateadas = '0h 0m'

