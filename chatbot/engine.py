"""Motor principal del chatbot."""
from datetime import datetime, date, time, timedelta
from typing import Optional, Tuple
from loguru import logger

from services import SheetsClient, CalendarClient, WhatsAppService
from models import Cliente, Cita, Servicio, Sesion
from config.constants import *
from utils.datetime_utils import (
    get_fecha_actual, get_proximas_fechas, calcular_hora_fin,
    formatear_fecha, formatear_hora
)
from utils.disponibilidad import obtener_slots_disponibles
from utils.formatters import (
    formatear_cita_resumen, formatear_confirmacion_cita, formatear_lista_citas
)
from chatbot.validaciones import (
    validar_nombre, validar_opcion_numerica,
    validar_confirmacion, validar_cancelacion, validar_comando_menu
)


class ChatbotEngine:
    """Motor del chatbot conversacional."""
    
    def __init__(self):
        """Inicializa el motor del chatbot."""
        self.sheets = SheetsClient()
        self.calendar = CalendarClient()
        self.whatsapp = WhatsAppService()
    
    def procesar_mensaje(self, telefono: str, mensaje: str) -> str:
        """
        Procesa un mensaje entrante y retorna la respuesta.
        
        Args:
            telefono: Número de teléfono del usuario
            mensaje: Texto del mensaje
        
        Returns:
            Respuesta del chatbot
        """
        # Verificar si es comando para volver al menú
        if validar_comando_menu(mensaje):
            self.sheets.eliminar_sesion(telefono)
            # Siempre mostrar menú principal
            sesion = Sesion(telefono=telefono, estado=ESTADO_INICIO)
            self.sheets.crear_sesion(sesion)
            return self._menu_principal()
        
        # Obtener o crear sesión
        sesion_data = self.sheets.get_sesion(telefono)
        
        if sesion_data is None:
            # Nueva sesión - siempre mostrar menú principal primero
            sesion = Sesion(telefono=telefono, estado=ESTADO_INICIO)
            self.sheets.crear_sesion(sesion)
            return self._menu_principal()
        
        sesion, row_index = sesion_data
        
        # Procesar según el estado actual
        if sesion.estado == ESTADO_INICIO:
            return self._procesar_menu_principal(telefono, mensaje, sesion, row_index)
        elif sesion.estado == "esperando_nombre":
            return self._procesar_nombre(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_ESPERANDO_SERVICIO:
            return self._procesar_seleccion_servicio(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_ESPERANDO_FECHA:
            return self._procesar_seleccion_fecha(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_ESPERANDO_HORA:
            return self._procesar_seleccion_hora(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_CONFIRMANDO_CITA:
            return self._procesar_confirmacion(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_CONSULTA_CITA:
            return self._procesar_consulta_cita(telefono, mensaje, sesion, row_index)
        elif sesion.estado == "seleccionando_cita_cancelar":
            return self._procesar_seleccion_cita_cancelar(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_CANCELANDO_CITA:
            return self._procesar_cancelacion(telefono, mensaje, sesion, row_index)
        elif sesion.estado == "seleccionando_cita_reagendar":
            return self._procesar_seleccion_cita_reagendar(telefono, mensaje, sesion, row_index)
        elif sesion.estado == ESTADO_REAGENDANDO_CITA:
            return self._procesar_reagendamiento(telefono, mensaje, sesion, row_index)
        
        # Estado desconocido - resetear
        self.sheets.eliminar_sesion(telefono)
        return self._menu_principal()

    
    def _menu_principal(self) -> str:
        """Retorna el menú principal."""
        return """
💈 *Bienvenido a Barbería Churco*

¿Qué deseas hacer?

1. Agendar cita
2. Consultar mi cita
3. Cancelar cita
4. Reagendar cita
5. Información de la barbería
6. Contactar al barbero

Responde con el número de la opción.
        """.strip()
    
    def _procesar_menu_principal(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección del menú principal."""
        if not validar_opcion_numerica(mensaje, 6):
            return "Opción inválida. Por favor responde con un número del 1 al 6."
        
        opcion = int(mensaje)
        
        if opcion == 1:
            # Agendar cita
            return self._iniciar_agendamiento(telefono, sesion, row_index)
        elif opcion == 2:
            # Consultar cita
            return self._iniciar_consulta(telefono, sesion, row_index)
        elif opcion == 3:
            # Cancelar cita
            return self._iniciar_cancelacion(telefono, sesion, row_index)
        elif opcion == 4:
            # Reagendar cita
            return self._iniciar_reagendamiento(telefono, sesion, row_index)
        elif opcion == 5:
            # Información de la barbería
            self.sheets.eliminar_sesion(telefono)
            return self._mostrar_informacion_barberia()
        elif opcion == 6:
            # Contactar al barbero
            self.sheets.eliminar_sesion(telefono)
            return self._mostrar_contacto_barbero()
        
        return "Opción inválida."
    
    def _iniciar_agendamiento(
        self,
        telefono: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Inicia el flujo de agendamiento."""
        # Verificar si el cliente existe
        cliente = self.sheets.get_cliente_por_telefono(telefono)
        
        if cliente is None:
            # Cliente nuevo - pedir nombre primero
            sesion.estado = "esperando_nombre"
            sesion.datos_temp = {}
            self.sheets.actualizar_sesion(sesion, row_index)
            return "Para agendar tu cita, primero necesito saber tu nombre. ¿Cuál es tu nombre?"
        
        # Cliente existente - mostrar servicios
        sesion.estado = ESTADO_ESPERANDO_SERVICIO
        sesion.datos_temp = {"cliente_id": cliente.id}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        return self._mostrar_servicios()
    
    def _procesar_nombre(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa el nombre del cliente."""
        if not validar_nombre(mensaje):
            return "Por favor ingresa un nombre válido (solo letras)."
        
        # Crear cliente
        cliente = self.sheets.crear_cliente(telefono, mensaje)
        
        # Continuar con el flujo de agendamiento - mostrar servicios
        sesion.estado = ESTADO_ESPERANDO_SERVICIO
        sesion.datos_temp = {"cliente_id": cliente.id}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        return f"¡Gracias {mensaje}! 😊\n\n" + self._mostrar_servicios()
    
    def _mostrar_servicios(self) -> str:
        """Muestra los servicios disponibles."""
        servicios = self.sheets.get_servicios_activos()
        
        mensaje = "✂️ *Selecciona tu servicio:*\n\n"
        for idx, servicio in enumerate(servicios, 1):
            mensaje += f"{idx}. {servicio.nombre}\n"
            mensaje += f"   💰 ${servicio.precio:,} COP\n"
            mensaje += f"   ⏱️ {servicio.duracion_minutos} minutos\n\n"
        mensaje += "Responde con el número del servicio."
        
        return mensaje
    
    def _mostrar_informacion_barberia(self) -> str:
        """Muestra información de la barbería."""
        return """
💈 *Barbería Churco*

📍 *Dirección:*
Calle 16 #20-06

⏰ *Horarios:*
Todos los días
• Mañana: 8:00 AM - 12:00 PM
• Tarde: 2:00 PM - 8:00 PM

✂️ *Servicios:*
• Corte + Barba: $28,000 COP (60 min)
• Corte Normal: $20,000 COP (45 min)

👨‍💼 *Barbero:*
Churco

📅 *Turnos disponibles:*
Bloques de 1 hora comenzando cada hora en punto

Escribe 'hola' para volver al menú principal.
        """.strip()
    
    def _mostrar_contacto_barbero(self) -> str:
        """Muestra información de contacto del barbero."""
        return """
💈 *Sígueme y escríbeme por IG si gustas* 💈

📸 Instagram: https://www.instagram.com/churcosbarberstudio?igsh=cGt2aXo3MTl5cmFk

¡Te responderé lo más pronto posible! 😊

Escribe 'hola' para volver al menú principal.
        """.strip()

    
    def _procesar_seleccion_servicio(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de servicio."""
        servicios = self.sheets.get_servicios_activos()
        
        if not validar_opcion_numerica(mensaje, len(servicios)):
            return f"Opción inválida. Por favor responde con un número del 1 al {len(servicios)}."
        
        opcion = int(mensaje)
        servicio = servicios[opcion - 1]
        
        # Guardar servicio en sesión
        sesion.datos_temp["servicio_id"] = servicio.id
        sesion.datos_temp["servicio_nombre"] = servicio.nombre
        sesion.datos_temp["precio"] = servicio.precio
        sesion.datos_temp["duracion_minutos"] = servicio.duracion_minutos
        sesion.estado = ESTADO_ESPERANDO_FECHA
        self.sheets.actualizar_sesion(sesion, row_index)
        
        # Mostrar fechas disponibles
        return self._mostrar_fechas()
    
    def _mostrar_fechas(self) -> str:
        """Muestra las fechas disponibles."""
        fechas = get_proximas_fechas(15)
        
        mensaje = "📅 *¿Qué día prefieres?*\n\n"
        mensaje += "ℹ️ La agenda está llena hasta el domingo 8 de marzo. Si quieres agendar una cita para esta semana llámame a este número.\n\n"
        
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        for idx, fecha in enumerate(fechas, 1):
            dia_nombre = dias_semana[fecha.weekday()]
            mensaje += f"{idx}. {dia_nombre} {fecha.strftime('%d/%m/%Y')}\n"
        
        mensaje += "\nResponde con el número del día."
        return mensaje
        return mensaje
    
    def _procesar_seleccion_fecha(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de fecha."""
        fechas = get_proximas_fechas(15)
        
        if not validar_opcion_numerica(mensaje, len(fechas)):
            return f"Opción inválida. Por favor responde con un número del 1 al {len(fechas)}."
        
        opcion = int(mensaje)
        fecha_seleccionada = fechas[opcion - 1]
        
        # Calcular horas disponibles ANTES de guardar la fecha
        duracion_minutos = sesion.datos_temp.get("duracion_minutos", 30)
        citas_dia = self.sheets.get_citas_por_fecha(fecha_seleccionada)
        eventos_calendar = self.calendar.get_eventos_dia(fecha_seleccionada)
        slots = obtener_slots_disponibles(fecha_seleccionada, duracion_minutos, citas_dia, eventos_calendar)
        
        if not slots:
            # No hay horarios - mantener estado y pedir otra fecha
            return "😔 No hay horarios disponibles para ese día. Por favor elige otra fecha:\n\n" + self._mostrar_fechas()
        
        # Hay horarios disponibles - guardar fecha y continuar
        sesion.datos_temp["fecha"] = fecha_seleccionada.isoformat()
        sesion.estado = ESTADO_ESPERANDO_HORA
        self.sheets.actualizar_sesion(sesion, row_index)
        
        # Mostrar horas disponibles
        return self._formatear_horas_disponibles(slots)
    
    def _mostrar_horas_disponibles(self, fecha: date, duracion_minutos: int) -> str:
        """Muestra las horas disponibles para una fecha."""
        # Obtener citas existentes
        citas_dia = self.sheets.get_citas_por_fecha(fecha)
        
        # Obtener eventos de Calendar
        eventos_calendar = self.calendar.get_eventos_dia(fecha)
        
        # Calcular slots disponibles
        slots = obtener_slots_disponibles(fecha, duracion_minutos, citas_dia, eventos_calendar)
        
        if not slots:
            return "😔 No hay horarios disponibles para ese día. Por favor elige otra fecha."
        
        return self._formatear_horas_disponibles(slots)
    
    def _formatear_horas_disponibles(self, slots: list) -> str:
        """Formatea la lista de horas disponibles."""
        mensaje = "🕐 *¿A qué hora?*\n\n"
        for idx, hora in enumerate(slots[:20], 1):  # Máximo 20 opciones
            mensaje += f"{idx}. {formatear_hora(hora)}\n"
        
        mensaje += "\nResponde con el número de la hora."
        return mensaje

    
    def _procesar_seleccion_hora(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de hora."""
        fecha = date.fromisoformat(sesion.datos_temp["fecha"])
        duracion_minutos = sesion.datos_temp["duracion_minutos"]
        
        # Recalcular slots disponibles
        citas_dia = self.sheets.get_citas_por_fecha(fecha)
        eventos_calendar = self.calendar.get_eventos_dia(fecha)
        slots = obtener_slots_disponibles(fecha, duracion_minutos, citas_dia, eventos_calendar)
        
        if not validar_opcion_numerica(mensaje, min(len(slots), 20)):
            return f"Opción inválida. Por favor responde con un número del 1 al {min(len(slots), 20)}."
        
        opcion = int(mensaje)
        hora_seleccionada = slots[opcion - 1]
        hora_fin = calcular_hora_fin(hora_seleccionada, duracion_minutos)
        
        # Guardar hora en sesión
        sesion.datos_temp["hora_inicio"] = hora_seleccionada.isoformat()
        sesion.datos_temp["hora_fin"] = hora_fin.isoformat()
        sesion.estado = ESTADO_CONFIRMANDO_CITA
        self.sheets.actualizar_sesion(sesion, row_index)
        
        # Mostrar resumen para confirmación
        return self._mostrar_resumen_confirmacion(sesion.datos_temp)
    
    def _mostrar_resumen_confirmacion(self, datos: dict) -> str:
        """Muestra el resumen de la cita para confirmación."""
        fecha = date.fromisoformat(datos["fecha"])
        hora_inicio = time.fromisoformat(datos["hora_inicio"])
        hora_fin = time.fromisoformat(datos["hora_fin"])
        
        mensaje = f"""
📋 *Confirma tu cita:*

📅 {formatear_fecha(fecha)}
🕐 {formatear_hora(hora_inicio)} - {formatear_hora(hora_fin)}
✂️ {datos["servicio_nombre"]}
💰 ${datos["precio"]:,} COP
👨‍💼 Barbero: Churco

Responde *SI* para confirmar o *NO* para cancelar.
        """.strip()
        
        return mensaje
    
    def _procesar_confirmacion(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la confirmación de la cita."""
        if validar_cancelacion(mensaje):
            self.sheets.eliminar_sesion(telefono)
            return "Cita cancelada. Escribe 'hola' cuando quieras agendar de nuevo."
        
        if not validar_confirmacion(mensaje):
            return "Por favor responde *SI* para confirmar o *NO* para cancelar."
        
        # Verificar si es reagendamiento
        es_reagendamiento = sesion.datos_temp.get("reagendando", False)
        
        # Obtener cliente
        cliente = self.sheets.get_cliente_por_telefono(telefono)
        if not cliente:
            self.sheets.eliminar_sesion(telefono)
            return "Error: Cliente no encontrado. Por favor inicia de nuevo."
        
        # Preparar datos de la cita
        fecha = date.fromisoformat(sesion.datos_temp["fecha"])
        hora_inicio = time.fromisoformat(sesion.datos_temp["hora_inicio"])
        hora_fin = time.fromisoformat(sesion.datos_temp["hora_fin"])
        
        if es_reagendamiento:
            # REAGENDAMIENTO - Actualizar cita existente
            cita_id = sesion.datos_temp.get("cita_id")
            result = self.sheets.get_cita_por_id(cita_id)
            
            if not result:
                self.sheets.eliminar_sesion(telefono)
                return "Error: Cita no encontrada."
            
            cita, cita_row = result
            
            # Eliminar evento anterior de Calendar
            if cita.calendar_event_id:
                self.calendar.eliminar_evento(cita.calendar_event_id)
            
            # Actualizar datos de la cita
            cita.fecha = fecha
            cita.hora_inicio = hora_inicio
            cita.hora_fin = hora_fin
            cita.estado = ESTADO_CONFIRMADA
            
            # Guardar en Sheets
            self.sheets.actualizar_cita(cita, cita_row)
            
            # Crear nuevo evento en Calendar
            event_id = self.calendar.crear_evento(
                cita_id=cita.id,
                cliente_nombre=cliente.nombre,
                cliente_telefono=telefono,
                servicio_nombre=cita.servicio_nombre,
                precio=cita.precio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado=ESTADO_CONFIRMADA
            )
            
            if event_id:
                logger.info(f"✅ Event ID recibido para reagendamiento: {event_id}")
                cita.calendar_event_id = event_id
                if self.sheets.actualizar_cita(cita, cita_row):
                    logger.info(f"✅ Cita reagendada actualizada con event_id en Sheets")
                else:
                    logger.error(f"❌ Error actualizando cita reagendada con event_id")
            else:
                logger.warning(f"⚠️ No se recibió event_id de Calendar para reagendamiento")
            
            # Limpiar sesión
            self.sheets.eliminar_sesion(telefono)
            
            return "✅ Cita reagendada exitosamente!\n\n" + formatear_confirmacion_cita(cita)
        
        else:
            # AGENDAMIENTO NUEVO - Crear nueva cita
            cita = Cita(
                id="",  # Se genera en crear_cita
                cliente_id=cliente.id,
                cliente_telefono=telefono,
                cliente_nombre=cliente.nombre,
                servicio_id=sesion.datos_temp["servicio_id"],
                servicio_nombre=sesion.datos_temp["servicio_nombre"],
                precio=sesion.datos_temp["precio"],
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado=ESTADO_CONFIRMADA
            )
            
            # Guardar en Sheets
            if not self.sheets.crear_cita(cita):
                return "Error al crear la cita. Por favor intenta de nuevo."
            
            # Crear evento en Calendar
            event_id = self.calendar.crear_evento(
                cita_id=cita.id,
                cliente_nombre=cliente.nombre,
                cliente_telefono=telefono,
                servicio_nombre=cita.servicio_nombre,
                precio=cita.precio,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                estado=ESTADO_CONFIRMADA
            )
            
            if event_id:
                logger.info(f"✅ Event ID recibido: {event_id}")
                # Actualizar cita con event_id
                result = self.sheets.get_cita_por_id(cita.id)
                if result:
                    cita_guardada, cita_row = result
                    cita_guardada.calendar_event_id = event_id
                    if self.sheets.actualizar_cita(cita_guardada, cita_row):
                        logger.info(f"✅ Cita actualizada con event_id en Sheets")
                    else:
                        logger.error(f"❌ Error actualizando cita con event_id")
                else:
                    logger.error(f"❌ No se pudo recuperar la cita {cita.id} para actualizar event_id")
            else:
                logger.warning(f"⚠️ No se recibió event_id de Calendar")
            
            # Limpiar sesión
            self.sheets.eliminar_sesion(telefono)
            
            # Retornar confirmación
            return formatear_confirmacion_cita(cita)

    
    def _iniciar_consulta(
        self,
        telefono: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Inicia el flujo de consulta de citas."""
        citas = self.sheets.get_citas_por_telefono(telefono, solo_activas=True)
        
        if not citas:
            self.sheets.eliminar_sesion(telefono)
            return "No tienes citas agendadas."
        
        if len(citas) == 1:
            self.sheets.eliminar_sesion(telefono)
            return formatear_cita_resumen(citas[0])
        
        # Múltiples citas - guardar en sesión
        sesion.estado = ESTADO_CONSULTA_CITA
        sesion.datos_temp = {"citas_ids": [c.id for c in citas]}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        return formatear_lista_citas(citas)
    
    def _procesar_consulta_cita(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de cita para ver detalles."""
        citas_ids = sesion.datos_temp.get("citas_ids", [])
        
        if not validar_opcion_numerica(mensaje, len(citas_ids)):
            return f"Opción inválida. Por favor responde con un número del 1 al {len(citas_ids)}."
        
        opcion = int(mensaje)
        cita_id = citas_ids[opcion - 1]
        
        result = self.sheets.get_cita_por_id(cita_id)
        if not result:
            self.sheets.eliminar_sesion(telefono)
            return "Error: Cita no encontrada."
        
        cita, _ = result
        self.sheets.eliminar_sesion(telefono)
        return formatear_cita_resumen(cita)
    
    def _iniciar_cancelacion(
        self,
        telefono: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Inicia el flujo de cancelación de citas."""
        citas = self.sheets.get_citas_por_telefono(telefono, solo_activas=True)
        
        if not citas:
            self.sheets.eliminar_sesion(telefono)
            return "No tienes citas para cancelar."
        
        if len(citas) == 1:
            # Una sola cita - pedir confirmación directa
            sesion.estado = ESTADO_CANCELANDO_CITA
            sesion.datos_temp = {"cita_id": citas[0].id}
            self.sheets.actualizar_sesion(sesion, row_index)
            
            mensaje = f"""
¿Deseas cancelar esta cita?

{formatear_cita_resumen(citas[0])}

Responde *SI* para confirmar la cancelación.
            """.strip()
            return mensaje
        
        # Múltiples citas - pedir selección
        sesion.estado = "seleccionando_cita_cancelar"
        sesion.datos_temp = {"citas_ids": [c.id for c in citas]}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        mensaje = "¿Qué cita deseas cancelar?\n\n"
        mensaje += formatear_lista_citas(citas)
        return mensaje
    
    def _procesar_cancelacion(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la cancelación de una cita."""
        if not validar_confirmacion(mensaje):
            self.sheets.eliminar_sesion(telefono)
            return "Cancelación abortada."
        
        cita_id = sesion.datos_temp.get("cita_id")
        result = self.sheets.get_cita_por_id(cita_id)
        
        if not result:
            self.sheets.eliminar_sesion(telefono)
            return "Error: Cita no encontrada."
        
        cita, cita_row = result
        
        # Actualizar estado en Sheets
        cita.estado = ESTADO_CANCELADA
        self.sheets.actualizar_cita(cita, cita_row)
        
        # Eliminar evento de Calendar
        if cita.calendar_event_id:
            self.calendar.eliminar_evento(cita.calendar_event_id)
        
        # Limpiar sesión
        self.sheets.eliminar_sesion(telefono)
        
        return "✅ Cita cancelada exitosamente. Puedes agendar una nueva cuando quieras."
    
    def _procesar_seleccion_cita_cancelar(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de cita para cancelar cuando hay múltiples."""
        citas_ids = sesion.datos_temp.get("citas_ids", [])
        
        if not validar_opcion_numerica(mensaje, len(citas_ids)):
            return f"Opción inválida. Por favor responde con un número del 1 al {len(citas_ids)}."
        
        opcion = int(mensaje)
        cita_id = citas_ids[opcion - 1]
        
        result = self.sheets.get_cita_por_id(cita_id)
        if not result:
            self.sheets.eliminar_sesion(telefono)
            return "Error: Cita no encontrada."
        
        cita, _ = result
        
        # Cambiar estado a cancelando y guardar cita_id
        sesion.estado = ESTADO_CANCELANDO_CITA
        sesion.datos_temp = {"cita_id": cita.id}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        mensaje = f"""
¿Deseas cancelar esta cita?

{formatear_cita_resumen(cita)}

Responde *SI* para confirmar la cancelación.
        """.strip()
        return mensaje
    
    def _iniciar_reagendamiento(
        self,
        telefono: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Inicia el flujo de reagendamiento."""
        citas = self.sheets.get_citas_por_telefono(telefono, solo_activas=True)
        
        if not citas:
            self.sheets.eliminar_sesion(telefono)
            return "No tienes citas para reagendar."
        
        if len(citas) == 1:
            # Una sola cita - pedir confirmación
            sesion.estado = ESTADO_REAGENDANDO_CITA
            sesion.datos_temp = {
                "cita_id": citas[0].id,
                "servicio_id": citas[0].servicio_id,
                "servicio_nombre": citas[0].servicio_nombre,
                "precio": citas[0].precio,
                "duracion_minutos": 60 if "Barba" in citas[0].servicio_nombre else 45
            }
            self.sheets.actualizar_sesion(sesion, row_index)
            
            mensaje = f"""
¿Deseas reagendar esta cita?

{formatear_cita_resumen(citas[0])}

Responde *SI* para continuar.
            """.strip()
            return mensaje
        
        # Múltiples citas
        sesion.estado = "seleccionando_cita_reagendar"
        sesion.datos_temp = {"citas_ids": [c.id for c in citas]}
        self.sheets.actualizar_sesion(sesion, row_index)
        
        mensaje = "¿Qué cita deseas reagendar?\n\n"
        mensaje += formatear_lista_citas(citas)
        return mensaje
    
    def _procesar_reagendamiento(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa el reagendamiento de una cita."""
        # Si está esperando confirmación inicial
        if "fecha" not in sesion.datos_temp:
            if not validar_confirmacion(mensaje):
                self.sheets.eliminar_sesion(telefono)
                return "Reagendamiento cancelado."
            
            # Iniciar selección de nueva fecha
            sesion.estado = ESTADO_ESPERANDO_FECHA
            sesion.datos_temp["reagendando"] = True  # Marcar que es reagendamiento
            self.sheets.actualizar_sesion(sesion, row_index)
            return self._mostrar_fechas()
        
        # Si llegó aquí, el flujo de fecha/hora ya se procesó en los otros métodos
        # Este método solo se llama para la confirmación inicial
        return "Flujo de reagendamiento en proceso..."
    
    def _procesar_seleccion_cita_reagendar(
        self,
        telefono: str,
        mensaje: str,
        sesion: Sesion,
        row_index: int
    ) -> str:
        """Procesa la selección de cita para reagendar cuando hay múltiples."""
        citas_ids = sesion.datos_temp.get("citas_ids", [])
        
        if not validar_opcion_numerica(mensaje, len(citas_ids)):
            return f"Opción inválida. Por favor responde con un número del 1 al {len(citas_ids)}."
        
        opcion = int(mensaje)
        cita_id = citas_ids[opcion - 1]
        
        result = self.sheets.get_cita_por_id(cita_id)
        if not result:
            self.sheets.eliminar_sesion(telefono)
            return "Error: Cita no encontrada."
        
        cita, _ = result
        
        # Cambiar estado a reagendando y guardar datos de la cita
        sesion.estado = ESTADO_REAGENDANDO_CITA
        sesion.datos_temp = {
            "cita_id": cita.id,
            "servicio_id": cita.servicio_id,
            "servicio_nombre": cita.servicio_nombre,
            "precio": cita.precio,
            "duracion_minutos": 60 if "Barba" in cita.servicio_nombre else 45
        }
        self.sheets.actualizar_sesion(sesion, row_index)
        
        mensaje = f"""
¿Deseas reagendar esta cita?

{formatear_cita_resumen(cita)}

Responde *SI* para continuar.
        """.strip()
        return mensaje
