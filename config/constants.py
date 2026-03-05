"""Constantes del negocio."""
from datetime import time

# Barbero
BARBERO_NOMBRE = "Churco"
BARBERO_ID = "barb_churco"

# Servicios
SERVICIOS = {
    "srv_corte_barba": {
        "id": "srv_corte_barba",
        "nombre": "Corte + Barba",
        "precio": 28000,
        "duracion_minutos": 50,
        "activo": True,
        "orden": 1
    },
    "srv_corte_normal": {
        "id": "srv_corte_normal",
        "nombre": "Corte Normal",
        "precio": 20000,
        "duracion_minutos": 40,
        "activo": True,
        "orden": 2
    }
}

# Horarios de atención (todos los días)
HORARIOS_ATENCION = [
    {"hora_inicio": time(8, 0), "hora_fin": time(12, 10)},   # Mañana: última cita 11:20 termina a 12:10
    {"hora_inicio": time(14, 0), "hora_fin": time(19, 50)}   # Tarde: última cita 19:00 termina a 19:50
]

# Estados de cita
ESTADO_PENDIENTE = "pendiente"
ESTADO_CONFIRMADA = "confirmada"
ESTADO_COMPLETADA = "completada"
ESTADO_CANCELADA = "cancelada"
ESTADO_NO_ASISTIO = "no_asistio"

ESTADOS_ACTIVOS = [ESTADO_PENDIENTE, ESTADO_CONFIRMADA]

# Estados conversacionales
ESTADO_INICIO = "inicio"
ESTADO_ESPERANDO_SERVICIO = "esperando_servicio"
ESTADO_ESPERANDO_FECHA = "esperando_fecha"
ESTADO_ESPERANDO_HORA = "esperando_hora"
ESTADO_CONFIRMANDO_CITA = "confirmando_cita"
ESTADO_CONSULTA_CITA = "consulta_cita"
ESTADO_CANCELANDO_CITA = "cancelando_cita"
ESTADO_REAGENDANDO_CITA = "reagendando_cita"

# Nombres de sheets
SHEET_CLIENTES = "clientes"
SHEET_CITAS = "citas"
SHEET_SERVICIOS = "servicios"
SHEET_DISPONIBILIDAD = "disponibilidad"
SHEET_SESIONES = "sesiones_chat"

# Colores de Google Calendar
COLOR_CONFIRMADA = "9"   # Azul
COLOR_CANCELADA = "11"   # Rojo
COLOR_PENDIENTE = "5"    # Amarillo
COLOR_COMPLETADA = "10"  # Verde
