from odoo import fields, http
from odoo.http import request

class PinValidationController(http.Controller):
    @http.route(['/ingresar_views', '/'], type='http', auth="public", website=True)
    def ingresar_views_form(self): 
        # Renderiza la vista ingresar_views.xml que contiene el formulario de ingreso de PIN
        return request.render('practice.ingresar_views')
    
    @http.route('/verificar_pin', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def verificar_pin(self, **kw):
        
        pin = kw.get('pin')
        
        user = self.obtener_usuario_por_pin(pin)
        
        if user:
            # Guardar user.id en la sesión
            request.session['user_id'] = user.id
            # Redirigir a la página de empleados
            return request.redirect('/empleados_views')
        else:
            # Si no se encuentra el usuario, redirigir a la página de error
            return request.redirect('/error_views')

    @http.route('/empleados_views', type='http', auth="user", website=True)
    def empleados_views_page(self,**kw):
        user_id = request.session.get('user_id')
    
        if not user_id:
        # Si no hay user_id en la sesión, redirigir a la página de error
            return request.redirect('/error_views')
    
        user=request.env['hr.employee'].sudo().browse(int(user_id))

        if not user or not user.active:
        # Si no existe el usuario o está inactivo, redirigir a la página de error
            return request.redirect('/error_views')
        
        hoy=fields.Date.today()
        schedule=request.env['schedules'].search([('usuario_id', '=', user.id),('fecha', '=', hoy)], limit=1)

        mostrar_ingreso = False
        mostrar_egreso = False

        if not schedule:
            mostrar_ingreso = True
        elif schedule.hora_entrada and not schedule.hora_salida:
            mostrar_egreso = True
        else:
            return request.render('practice.registro_correcto_views', {'user': user, 'schedule': schedule,'mensaje_registro_correcto': 'Ya ha registrado su horario de ingreso y salida'})
        
        return request.render('practice.empleados_views',{'user':user,'schedule':schedule, 'mostrar_ingreso':mostrar_ingreso, 'mostrar_egreso':mostrar_egreso})
    
    @http.route('/error_views', type='http', auth="public", website=True)
    def error_views_page(self):
         return request.render('practice.error_views',{'mensaje_error':'El PIN ingresado es incorrecto. Por favor, intente nuevamente.'})
    
    # Buscar al usuario por el PIN ingresado (supuesto que el PIN está almacenado en el campo `pin` del usuario)
    def obtener_usuario_por_pin(self, pin):
        user = request.env['hr.employee'].sudo().search([('pin', '=', pin)], limit=1)
        return user

    
