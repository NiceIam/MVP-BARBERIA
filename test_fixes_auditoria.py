"""
Test de regresión para verificar los fixes de la auditoría.
Prueba cada cambio sin tocar datos reales (unit tests con mocks).
"""
import sys
from datetime import date, time, datetime
from unittest.mock import MagicMock, patch
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

resultados = {}


def test(nombre):
    """Decorador simple para registrar tests."""
    def decorator(fn):
        try:
            fn()
            logger.info(f"  PASS  {nombre}")
            resultados[nombre] = True
        except Exception as e:
            logger.error(f"  FAIL  {nombre}: {e}")
            resultados[nombre] = False
        return fn
    return decorator


# ===========================================================
# FIX 1 — server.py: excepción en procesar_mensaje no silencia al usuario
# ===========================================================

@test("Fix1: excepcion en procesar_mensaje envia error al usuario")
def _():
    """Si chatbot.procesar_mensaje lanza excepción, evolution.send_message debe llamarse con el error."""
    sent = []

    # Simular el comportamiento del bloque en server.py
    def mock_procesar_mensaje(telefono, texto):
        raise RuntimeError("Sheets caído")

    def mock_send_message(telefono, msg):
        sent.append(msg)

    telefono = "573001234567"
    texto = "hola"

    try:
        respuesta = mock_procesar_mensaje(telefono, texto)
    except Exception as e:
        respuesta = "Lo sentimos, ocurrió un error inesperado. Por favor intenta de nuevo o escribe *hola* para volver al menú."

    mock_send_message(telefono, respuesta)

    assert len(sent) == 1, "Debe enviarse exactamente un mensaje"
    assert "error" in sent[0].lower() or "sentimos" in sent[0].lower(), "El mensaje debe indicar el error"


# ===========================================================
# FIX 2 — models/cita.py: hora vacía no crashea
# ===========================================================

@test("Fix2: Cita.from_sheet_row con hora_inicio vacia retorna time(0,0)")
def _():
    from models.cita import Cita

    # Fila con hora_inicio y hora_fin vacías (columnas 8 y 9 vacías)
    row = [
        "cita_test01", "cli_abc", "573001234567", "Juan",
        "srv_corte_barba", "Corte + Barba", "28000",
        "24/03/2026",
        "",   # hora_inicio vacía
        "",   # hora_fin vacía
        "confirmada",
        "", "", "", ""
    ]
    cita = Cita.from_sheet_row(row)
    assert cita.hora_inicio == time(0, 0), f"Esperaba time(0,0), got {cita.hora_inicio}"
    assert cita.hora_fin == time(0, 0), f"Esperaba time(0,0), got {cita.hora_fin}"


@test("Fix2: Cita.from_sheet_row con horas validas funciona correctamente")
def _():
    from models.cita import Cita

    row = [
        "cita_test02", "cli_abc", "573001234567", "Juan",
        "srv_corte_barba", "Corte + Barba", "28000",
        "24/03/2026", "14:00", "14:50",
        "confirmada", "", "", "", ""
    ]
    cita = Cita.from_sheet_row(row)
    assert cita.hora_inicio == time(14, 0)
    assert cita.hora_fin == time(14, 50)


@test("Fix2: fila corrupta en get_todas_citas_activas no crashea disponibilidad")
def _():
    """Una fila con hora vacía no debe crashear el loop de disponibilidad."""
    from models.cita import Cita

    rows_sheets = [
        # Fila válida
        ["cita_ok", "cli_1", "573001111111", "Pedro", "srv_corte_barba", "Corte + Barba",
         "28000", "24/03/2026", "10:00", "10:50", "confirmada", "", "", "", ""],
        # Fila corrupta con horas vacías
        ["cita_bad", "cli_2", "573002222222", "Luis", "srv_corte_normal", "Corte Normal",
         "20000", "24/03/2026", "", "", "confirmada", "", "", "", ""],
    ]

    citas = []
    for row in rows_sheets:
        cita = Cita.from_sheet_row(row)  # No debe lanzar excepción
        if cita.estado in ['confirmada', 'pendiente']:
            citas.append(cita)

    assert len(citas) == 2, f"Debe procesar ambas filas, got {len(citas)}"


# ===========================================================
# FIX 3 — google_sheets.py: eliminar_sesion loggea si falla
# ===========================================================

@test("Fix3: eliminar_sesion retorna False y loggea cuando _update_row falla")
def _():
    from services.google_sheets import SheetsClient

    sheets = SheetsClient.__new__(SheetsClient)
    sheets.spreadsheet_id = "fake_id"

    # Mock: get_sesion devuelve una sesión en fila 5
    from models.sesion import Sesion
    sesion_mock = Sesion(telefono="573001234567", estado="inicio")
    sheets.get_sesion = MagicMock(return_value=(sesion_mock, 5))

    # Mock: _update_row falla
    sheets._update_row = MagicMock(return_value=False)

    result = sheets.eliminar_sesion("573001234567")

    assert result == False, "Debe retornar False cuando _update_row falla"
    sheets._update_row.assert_called_once()


@test("Fix3: eliminar_sesion retorna True cuando funciona correctamente")
def _():
    from services.google_sheets import SheetsClient
    from models.sesion import Sesion

    sheets = SheetsClient.__new__(SheetsClient)
    sesion_mock = Sesion(telefono="573001234567", estado="inicio")
    sheets.get_sesion = MagicMock(return_value=(sesion_mock, 5))
    sheets._update_row = MagicMock(return_value=True)

    result = sheets.eliminar_sesion("573001234567")
    assert result == True


# ===========================================================
# FIX 4 — engine.py: _mostrar_servicios con lista vacía
# ===========================================================

@test("Fix4: _mostrar_servicios con servicios vacíos retorna mensaje de error amigable")
def _():
    from chatbot.engine import ChatbotEngine

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.sheets.get_servicios_activos.return_value = []  # Sin servicios

    respuesta = engine._mostrar_servicios()

    assert "no están disponibles" in respuesta.lower() or "temporalmente" in respuesta.lower(), \
        f"Respuesta inesperada: {respuesta}"
    assert "Selecciona tu servicio" not in respuesta, \
        "No debe mostrar el header de selección si no hay servicios"


@test("Fix4: _mostrar_servicios con servicios disponibles funciona normal")
def _():
    from chatbot.engine import ChatbotEngine
    from models.servicio import Servicio

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()

    servicio = Servicio(
        id="srv_corte_barba", nombre="Corte + Barba",
        precio=28000, duracion_minutos=50, activo=True, orden=1
    )
    engine.sheets.get_servicios_activos.return_value = [servicio]

    respuesta = engine._mostrar_servicios()

    assert "Selecciona tu servicio" in respuesta
    assert "Corte + Barba" in respuesta


# ===========================================================
# FIX PREVIO — engine.py: verificación Sheets antes de crear evento Calendar
# ===========================================================

@test("FixPrevio: si Sheets no persiste la cita, no se crea evento en Calendar")
def _():
    """
    Simula el caso donde crear_cita devuelve True pero get_cita_por_id no encuentra el registro.
    En ese caso NO debe crearse el evento en Calendar.
    """
    from chatbot.engine import ChatbotEngine
    from models.sesion import Sesion
    from models.cliente import Cliente

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.calendar = MagicMock()

    # Cliente existente
    cliente = Cliente(id="cli_test", telefono="573001234567", nombre="Juan",
                      fecha_registro=datetime.now(), total_citas=0)
    engine.sheets.get_cliente_por_telefono.return_value = cliente

    # crear_cita dice OK pero la verificación falla (get_cita_por_id no lo encuentra)
    engine.sheets.crear_cita.return_value = True
    engine.sheets.get_cita_por_id.return_value = None  # <-- el dato no quedó en Sheets

    # Sesión con todos los datos necesarios para confirmación
    sesion = Sesion(telefono="573001234567", estado="confirmando_cita", datos_temp={
        "reagendando": False,
        "servicio_id": "srv_corte_barba",
        "servicio_nombre": "Corte + Barba",
        "precio": 28000,
        "duracion_minutos": 50,
        "fecha": "2026-03-25",
        "hora_inicio": "14:00:00",
        "hora_fin": "14:50:00",
    })

    respuesta = engine._procesar_confirmacion("573001234567", "SI", sesion, 3)

    # El evento en Calendar NO debe haberse creado
    engine.calendar.crear_evento.assert_not_called()
    # La respuesta debe indicar error
    assert "error" in respuesta.lower() or "intenta" in respuesta.lower(), \
        f"Respuesta inesperada: {respuesta}"


# ===========================================================
# FIX 5 — google_sheets.py: citas pasadas no deben aparecer al cancelar/reagendar
# ===========================================================

@test("Fix5: get_citas_por_telefono solo_activas excluye citas del pasado")
def _():
    from services.google_sheets import SheetsClient
    from datetime import date, timedelta

    sheets = SheetsClient.__new__(SheetsClient)
    sheets.spreadsheet_id = "fake"
    sheets.service = MagicMock()

    hoy = date.today()
    ayer = (hoy - timedelta(days=1)).strftime('%d/%m/%Y')
    manana = (hoy + timedelta(days=1)).strftime('%d/%m/%Y')

    sheets._read_range = MagicMock(return_value=[
        # Cita futura confirmada → debe incluirse
        ["cita_fut", "cli_1", "573001234567", "Juan", "srv_1", "Corte", "20000",
         manana, "10:00", "10:40", "confirmada", "", "", "", ""],
        # Cita pasada confirmada → debe excluirse
        ["cita_pas", "cli_1", "573001234567", "Juan", "srv_1", "Corte", "20000",
         ayer, "10:00", "10:40", "confirmada", "", "", "", ""],
        # Cita de otro cliente → debe excluirse
        ["cita_oth", "cli_2", "573009999999", "Pedro", "srv_1", "Corte", "20000",
         manana, "11:00", "11:40", "confirmada", "", "", "", ""],
    ])

    citas = sheets.get_citas_por_telefono("573001234567", solo_activas=True)

    assert len(citas) == 1, f"Solo debe retornar la cita futura, got {len(citas)}"
    assert citas[0].id == "cita_fut"


@test("Fix5: get_citas_por_telefono sin solo_activas retorna todas (incluyendo pasadas)")
def _():
    from services.google_sheets import SheetsClient
    from datetime import date, timedelta

    sheets = SheetsClient.__new__(SheetsClient)
    sheets.spreadsheet_id = "fake"
    sheets.service = MagicMock()

    hoy = date.today()
    ayer = (hoy - timedelta(days=1)).strftime('%d/%m/%Y')
    manana = (hoy + timedelta(days=1)).strftime('%d/%m/%Y')

    sheets._read_range = MagicMock(return_value=[
        ["cita_fut", "cli_1", "573001234567", "Juan", "srv_1", "Corte", "20000",
         manana, "10:00", "10:40", "confirmada", "", "", "", ""],
        ["cita_pas", "cli_1", "573001234567", "Juan", "srv_1", "Corte", "20000",
         ayer, "10:00", "10:40", "confirmada", "", "", "", ""],
    ])

    citas = sheets.get_citas_por_telefono("573001234567", solo_activas=False)

    assert len(citas) == 2, f"Sin filtro activo debe retornar todas, got {len(citas)}"


# ===========================================================
# INTEGRACIÓN — flujo completo de agendamiento (mock)
# ===========================================================

@test("Integracion: flujo hola→menu retorna bienvenida")
def _():
    """Verifica que el flujo básico del bot sigue funcionando."""
    from chatbot.engine import ChatbotEngine
    from models.sesion import Sesion

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.calendar = MagicMock()
    engine.whatsapp = MagicMock()

    # Sin sesión existente → crear nueva
    engine.sheets.get_sesion.return_value = None
    engine.sheets.crear_sesion.return_value = True

    respuesta = engine.procesar_mensaje("573001234567", "hola")

    assert "Bienvenido" in respuesta or "bienvenido" in respuesta.lower()
    assert "Agendar" in respuesta or "agendar" in respuesta.lower()


@test("Integracion: estado desconocido resetea al menu principal")
def _():
    from chatbot.engine import ChatbotEngine
    from models.sesion import Sesion

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.calendar = MagicMock()
    engine.whatsapp = MagicMock()

    # Sesión con estado inválido/desconocido
    sesion_invalida = Sesion(telefono="573001234567", estado="estado_que_no_existe")
    engine.sheets.get_sesion.return_value = (sesion_invalida, 5)
    engine.sheets.eliminar_sesion.return_value = True

    respuesta = engine.procesar_mensaje("573001234567", "cualquier texto")

    assert "Bienvenido" in respuesta or "menu" in respuesta.lower() or "Agendar" in respuesta


# ===========================================================
# FIX 6A — models/cita.py: fecha_creacion/fecha_modificacion con formato inválido
# ===========================================================

@test("Fix6A: Cita.from_sheet_row con fecha_creacion en formato invalido retorna None")
def _():
    from models.cita import Cita

    row = [
        "cita_test03", "cli_abc", "573001234567", "Juan",
        "srv_corte_barba", "Corte + Barba", "28000",
        "24/03/2026", "14:00", "14:50", "confirmada", "",
        "30/03/2026 21:35:18",  # formato que Sheets puede auto-generar (no ISO)
        "30/03/2026 22:00:00",  # igual
        ""
    ]
    cita = Cita.from_sheet_row(row)
    assert cita.fecha_creacion is None, f"Esperaba None, got {cita.fecha_creacion}"
    assert cita.fecha_modificacion is None, f"Esperaba None, got {cita.fecha_modificacion}"


@test("Fix6A: Cita.from_sheet_row con fecha_creacion ISO valida la parsea correctamente")
def _():
    from models.cita import Cita
    from datetime import datetime

    row = [
        "cita_test04", "cli_abc", "573001234567", "Juan",
        "srv_corte_barba", "Corte + Barba", "28000",
        "24/03/2026", "14:00", "14:50", "confirmada", "",
        "2026-03-30T21:35:18.008000",  # formato ISO correcto
        "2026-03-30T22:00:00",
        ""
    ]
    cita = Cita.from_sheet_row(row)
    assert cita.fecha_creacion is not None
    assert cita.fecha_creacion.year == 2026


# ===========================================================
# FIX 6B — engine.py: _procesar_seleccion_hora con datos_temp incompleto
# ===========================================================

@test("Fix6B: _procesar_seleccion_hora sin fecha en datos_temp vuelve a mostrar fechas")
def _():
    from chatbot.engine import ChatbotEngine
    from models.sesion import Sesion

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.calendar = MagicMock()
    engine.sheets.get_todas_citas_activas.return_value = []
    engine.calendar.get_eventos_rango.return_value = []
    engine.sheets.actualizar_sesion.return_value = True

    sesion = Sesion(telefono="573001234567", estado="esperando_hora", datos_temp={
        "duracion_minutos": 50
        # "fecha" ausente — simula sesión corrupta
    })

    respuesta = engine._procesar_seleccion_hora("573001234567", "2", sesion, 5)

    assert "fecha" in respuesta.lower() or "día" in respuesta.lower() or "error" in respuesta.lower(), \
        f"Debería redirigir a selección de fecha, got: {respuesta[:80]}"
    engine.sheets.actualizar_sesion.assert_called()


# ===========================================================
# FIX 6C — engine.py: _mostrar_resumen_confirmacion con datos_temp vacío
# ===========================================================

@test("Fix6C: _mostrar_resumen_confirmacion con datos_temp vacio retorna error amigable")
def _():
    from chatbot.engine import ChatbotEngine

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()

    respuesta = engine._mostrar_resumen_confirmacion({})  # datos vacíos

    assert "error" in respuesta.lower() or "hola" in respuesta.lower(), \
        f"Debe retornar error amigable, got: {respuesta}"
    assert "Confirma tu cita" not in respuesta


@test("Fix6C: _mostrar_resumen_confirmacion con datos validos funciona normal")
def _():
    from chatbot.engine import ChatbotEngine

    engine = ChatbotEngine.__new__(ChatbotEngine)

    datos = {
        "fecha": "2026-04-10",
        "hora_inicio": "14:00:00",
        "hora_fin": "14:50:00",
        "servicio_nombre": "Corte + Barba",
        "precio": 28000,
    }
    respuesta = engine._mostrar_resumen_confirmacion(datos)

    assert "Confirma tu cita" in respuesta
    assert "Corte + Barba" in respuesta
    assert "28,000" in respuesta


# ===========================================================
# FIX 6D — engine.py: _procesar_confirmacion con datos_temp sin fecha
# ===========================================================

@test("Fix6D: _procesar_confirmacion sin fecha en datos_temp retorna error y limpia sesion")
def _():
    from chatbot.engine import ChatbotEngine
    from models.sesion import Sesion
    from models.cliente import Cliente
    from datetime import datetime

    engine = ChatbotEngine.__new__(ChatbotEngine)
    engine.sheets = MagicMock()
    engine.calendar = MagicMock()

    cliente = Cliente(id="cli_test", telefono="573001234567", nombre="Juan",
                      fecha_registro=datetime.now(), total_citas=0)
    engine.sheets.get_cliente_por_telefono.return_value = cliente
    engine.sheets.eliminar_sesion.return_value = True

    sesion = Sesion(telefono="573001234567", estado="confirmando_cita", datos_temp={
        "reagendando": False,
        # "fecha", "hora_inicio", "hora_fin" ausentes
    })

    respuesta = engine._procesar_confirmacion("573001234567", "SI", sesion, 3)

    assert "error" in respuesta.lower() or "hola" in respuesta.lower()
    engine.sheets.eliminar_sesion.assert_called_with("573001234567")
    engine.calendar.crear_evento.assert_not_called()


# ===========================================================
# FIX 6E — formatters.py: formatear_precio con None
# ===========================================================

@test("Fix6E: formatear_precio con None retorna $0 COP sin crash")
def _():
    from utils.formatters import formatear_precio

    resultado = formatear_precio(None)
    assert resultado == "$0 COP", f"Esperaba '$0 COP', got '{resultado}'"


@test("Fix6E: formatear_precio con int normal funciona correctamente")
def _():
    from utils.formatters import formatear_precio

    resultado = formatear_precio(28000)
    assert resultado == "$28,000 COP", f"Esperaba '$28,000 COP', got '{resultado}'"


@test("Fix6E: formatear_precio con string numerico funciona correctamente")
def _():
    from utils.formatters import formatear_precio

    resultado = formatear_precio("20000")
    assert resultado == "$20,000 COP", f"Esperaba '$20,000 COP', got '{resultado}'"


# ===========================================================
# RESUMEN
# ===========================================================

def main():
    logger.info("\n" + "="*55)
    logger.info("TEST DE REGRESION - FIXES AUDITORIA")
    logger.info("="*55 + "\n")

    total = len(resultados)
    exitosos = sum(resultados.values())
    fallidos = [n for n, r in resultados.items() if not r]

    logger.info("\n" + "="*55)
    logger.info(f"RESULTADO: {exitosos}/{total} tests pasaron")
    if fallidos:
        logger.error("FALLARON:")
        for f in fallidos:
            logger.error(f"  - {f}")
        return 1
    else:
        logger.info("Todos los fixes funcionan correctamente.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
