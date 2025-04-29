from datetime import date, datetime, timedelta
from odoo import fields, http
from odoo.http import request

class lineasController(http.Controller):
    @http.route('/linea/dashboard', type='http', auth='public', website=True)
    def dashboard_view(self):       
 
        hoy = date.today() # Fecha segun la zona horaria del ordenador 
        dia_semana =  datetime.today().strftime('%A')  # Dia de la semana (lunes, martes,etc..) 
        dia_hoy = fields.Date.today() # Fecha segun la zona horaria de odoo 
        hora_actual = (datetime.now() + timedelta(hours=2)).strftime('%H:%M') # Ajustar la zona horaria a UTC+2

        # Horas y puestos fijos
        horas = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'] 
        puestos = ['1', '2', '3', '4', '5']

        # Obtener los registros de la tabla 'linea' para el día actual
        registros_linea_hoy = request.env['linea'].sudo().search([('timestamp', '>=', dia_hoy), ('timestamp', '<', fields.Date.add(dia_hoy, days=1))])

        # Diccionario de registros por hora y puesto
        # {('07:00', '3'): 1, ('11:00', '3'): 2, ('11:00', '4'): 1}
        #registros = {} 
        registros_ordenados = {}

        for hora in horas:
            registros_ordenados[hora] = {puesto: 0 for puesto in puestos} 

        for registro in registros_linea_hoy:
            puesto = registro.puesto
            timestamp = registro.timestamp + timedelta(hours=2) # Ajustar la zona horaria a UTC+2
            if puesto and timestamp:
                hora = timestamp.strftime('%H:00')
                if hora in registros_ordenados:
            # Actualiza el contador para el puesto y hora específicos
                    registros_ordenados[hora][puesto] += 1
                # clave =(hora,puesto)
                # if clave in registros:
                #     registros[clave] += 1
                # else:
                #     registros[clave] = 1

        # # registros ordenados por hora {'07:00': {'1': 0, '2': 0, '3': 1, '4': 0, '5': 0}, '08:00': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}, ...}
        # registros_ordenados =  {}

        # for hora in horas:
        #     registros_ordenados[hora] = {puesto: 0 for puesto in puestos} 
        
        # # Llenar registros ordenados con los valores del diccionario 'registros'
        # for (hora, puesto), count in registros.items():
        #     if hora in registros_ordenados:
        #         registros_ordenados[hora][puesto] = count
         
        ######### OBJETIVOS ########
        inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de la semana actual
        fin_semana = inicio_semana + timedelta(days=4) # Viernes de la semana actual

        # objetivos(49, 50, 51, 52, 53) -> son los id de los registros de la tabla objetivos
        objetivos_records = request.env['objetivos'].sudo().search([
            ('timestamp', '>=', inicio_semana),
            ('timestamp', '<=', fin_semana)
        ])

        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        objetivos = {dia: {'objetivos': [], 'cantidad' : 0} for dia in dias_orden}

        # Suma de todos los registros del dia : 4
        total_registros = sum(
                    registros_ordenados[hora][puesto] for hora in registros_ordenados for puesto in puestos
                )
        
        for obj in objetivos_records:
            if obj.dia in objetivos:
                objetivos[obj.dia]['objetivos'].append(obj.objetivo) 
                if obj.dia.lower() == dia_semana:
                    # Solo actualizar el objetivo del día actual
                    obj.write({'cantidad': total_registros})
                objetivos[obj.dia]['cantidad'] += obj.cantidad
        
        print(registros_ordenados)
        return request.render('linea.linea_qweb_view',{'docs': registros_linea_hoy, 'registros' : registros_ordenados, 'puestos' : puestos, 'horas': horas, 'hoy': hoy, 'dia_semana': dia_semana, 'hora_actual': hora_actual, 'objetivos': objetivos})