from odoo import fields, http
from odoo.http import request

class RegistrarIngreso(http.Controller):
    @http.route('/registrar_ingreso', type='http', methods=['POST'], auth='user',website=True)
    def registrar_ingreso(self, **kw):
        user_id = kw.get('user_id')
        user = request.env['hr.employee'].sudo().search([('id', '=', user_id)], limit=1)
   
        if user:
            #crear registro de horario
            schedule = request.env['schedules'].create_schedule(user_id=user.id, hora_entrada=fields.Datetime.now(),hora_salida=False)

            return request.render('practice.registro_correcto_views', {'user': user, 'schedule': schedule,'mensaje_registro_correcto': 'Horario de ingreso registrado correctamente'})
        else:
            return request.render('practice.error_views', {'error_message': 'Usuario no encontrado' })
            