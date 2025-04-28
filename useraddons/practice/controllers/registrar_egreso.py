from odoo import fields, http
from odoo.http import request

class RegistrarEgreso(http.Controller):
    @http.route('/registrar_egreso', type='http', methods=['POST'], auth='user',website=True)
    def registrar_egreso(self, **kw):
        user_id = kw.get('user_id')
        user = request.env['hr.employee'].sudo().search([('id', '=', user_id)], limit=1)
        
        if user:
            hoy = fields.Date.today()
            schedule=request.env['schedules'].search([('usuario_id', '=', user.id),('fecha', '=', hoy)], limit=1)
            
            if schedule:
                # Actualizar el campo hora_salida con la hora actual
                schedule.write({'hora_salida': fields.Datetime.now()})
                
                return request.render('practice.registro_correcto_views', {'user': user, 'schedule': schedule,'mensaje_registro_correcto': 'Horario de salida registrado correctamente'})
                
            else:
                return request.render('practice.error_views', {'error_message': 'Error al registrar salida'})
        else:
                return request.render  ('practice.error_views', {
                    'error_message': 'Usuario no encontrado',
                })
        
        