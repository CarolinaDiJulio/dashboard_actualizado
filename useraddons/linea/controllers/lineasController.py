from datetime import date, datetime, timedelta
from odoo import fields, http
from odoo.http import request

class lineasController(http.Controller):
    @http.route('/linea/dashboard', type='http', auth='public', website=True)
    def dashboard_view(self):      

        ######### Variables ######## 

        # Fechas y hora actual
        hoy = date.today() # Segun zona horaria del ordenador 
        dia_semana =  datetime.today().strftime('%A') # Lunes, martes,etc...
        dia_hoy = fields.Date.today() # Segun zona horaria de odoo 
        hora_actual = (datetime.now() + timedelta(hours=2)).strftime('%H:%M') 

        # Días, horas y puestos fijos
        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        horas = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'] 
        puestos = ['1', '2', '3', '4', '5']

        # Inicio y fin de la semana actual
        inicio_semana = hoy - timedelta(days=hoy.weekday())  
        fin_semana = inicio_semana + timedelta(days=4) 

        ######### Gestionar linea ########

        # Obtener los registros de la tabla 'linea' para el día actual
        registros_linea_hoy = request.env['linea'].sudo().search([('timestamp', '>=', dia_hoy), ('timestamp', '<', fields.Date.add(dia_hoy, days=1))])

        # Diccionario de registros ordenados por hora y puesto 
        registros_ordenados = {hora: {puesto: 0 for puesto in puestos} for hora in horas} 

        for registro in registros_linea_hoy:
            puesto = registro.puesto
            timestamp = registro.timestamp + timedelta(hours=2) # Ajustar la zona horaria a UTC+2
            if puesto and timestamp:
                hora = timestamp.strftime('%H:00')
                if hora in registros_ordenados:
                    # Actualiza el contador para el puesto y hora específicos
                    registros_ordenados[hora][puesto] += 1 

        # Suma de todos los registros del dia : 4
        total_registros = sum(registros_ordenados[hora][puesto] for hora in registros_ordenados for puesto in puestos)

        ######### Gestionar objetivos ######## 

        # Obtener los registros de la tabla 'objetivos' para la semana actual
        objetivos_records = request.env['objetivos'].sudo().search([('timestamp', '>=', inicio_semana), ('timestamp', '<=', fin_semana)]) 
        
        # Diccionario de objetivos por día
        objetivos = {dia: {'objetivos': [], 'cantidad' : 0} for dia in dias_orden}

        for obj in objetivos_records:
            if obj.dia in objetivos:
                objetivos[obj.dia]['objetivos'].append(obj.objetivo) 
                if obj.dia.lower() == dia_semana:
                    # Actualizar la cantidad en el objetivo del día actual
                    obj.write({'cantidad': total_registros})
                objetivos[obj.dia]['cantidad'] += obj.cantidad
         
        # Renderizar la vista QWeb con los datos obtenidos 
        return request.render('linea.linea_qweb_view',{'docs': registros_linea_hoy, 'registros' : registros_ordenados, 'puestos' : puestos, 'horas': horas, 'hoy': hoy, 'dia_semana': dia_semana, 'hora_actual': hora_actual, 'objetivos': objetivos})