from datetime import date, datetime, timedelta
from odoo import fields, http
from odoo.http import request

class lineasController(http.Controller):
    @http.route('/linea/dashboard', type='http', auth='public', website=True)
    def dashboard_view(self):

        hoy = date.today()
        dia_hoy = fields.Date.today() # Día actual segun la zona horaria de Odoo
        dia_semana =  datetime.today().strftime('%A')
        hora_actual = (datetime.now() + timedelta(hours=2)).strftime('%H:%M') # Ajustar la zona horaria a UTC+2

        # Obtener los registros de la tabla 'linea' para el día actual
        docs = request.env['linea'].sudo().search([
            ('timestamp', '>=', dia_hoy), 
            ('timestamp', '<', fields.Date.add(dia_hoy, days=1))])

        #registros = {} 
        # for doc in docs:
        #     puesto = doc.puesto
        #     timestamp = doc.timestamp + timedelta(hours=2) # Ajustar la zona horaria a UTC+2
        #     if puesto and timestamp:
        #         hora = timestamp.strftime('%H:00')
        #         clave =(hora,puesto)
        #         if clave in registros:
        #             registros[clave] += 1
        #         else:
        #             registros[clave] = 1

        horas = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'] 
        puestos = ['1', '2', '3', '4', '5']
        registros_ordenados =  {
            hora: {puesto: 0 for puesto in puestos}
            for hora in horas}

        for doc in docs:
            puesto = doc.puesto
            timestamp = doc.timestamp + timedelta(hours=2) # Ajustar la zona horaria a UTC+2
            if puesto and timestamp:
                hora = timestamp.strftime('%H:00')
                clave =(hora,puesto)
                if clave in registros_ordenados:
                    registros_ordenados[clave] += 1
                else:
                    registros_ordenados[clave] = 1

        for hora in horas:
            registros_ordenados[hora] = {puesto: 0 for puesto in puestos} 
        
        for (hora, puesto), count in registros_ordenados.items():
            if hora in registros_ordenados:
                registros_ordenados[hora][puesto] = count
        
        ######### OBJETIVOS ##########
        inicio_semana = hoy - timedelta(days=hoy.weekday())  
        fin_semana = inicio_semana + timedelta(days=4)      

        objetivos_records = request.env['objetivos'].sudo().search([
            ('timestamp', '>=', inicio_semana),
            ('timestamp', '<=', fin_semana)
        ])

        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        objetivos = {dia: {'objetivos': [], 'cantidad' : 0} for dia in dias_orden}

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
        
        # Renderizar la vista QWeb
        return request.render('linea.linea_qweb_view',{'docs': docs, 'registros' : registros_ordenados, 'puestos' : puestos, 'horas': horas, 'hoy': hoy, 'dia_semana': dia_semana, 'hora_actual': hora_actual, 'objetivos': objetivos})