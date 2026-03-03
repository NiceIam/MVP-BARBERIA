"""Script para actualizar la duración del Corte Normal a 40 minutos."""
from services import SheetsClient
from loguru import logger


def main():
    """Actualiza la duración del Corte Normal en Google Sheets."""
    logger.info("🔄 Actualizando duración del Corte Normal...")
    
    sheets = SheetsClient()
    
    # Verificar conexión
    if not sheets.test_connection():
        logger.error("❌ No se pudo conectar a Google Sheets")
        return
    
    # Buscar el servicio Corte Normal
    servicio = sheets.get_servicio_por_id("srv_corte_normal")
    
    if not servicio:
        logger.error("❌ Servicio 'Corte Normal' no encontrado")
        return
    
    logger.info(f"📋 Servicio encontrado: {servicio.nombre}")
    logger.info(f"   Duración actual: {servicio.duracion_minutos} minutos")
    
    # Buscar la fila del servicio en Sheets
    rows = sheets._read_range("servicios!A2:F")
    for idx, row in enumerate(rows, start=2):
        if len(row) > 0 and row[0] == "srv_corte_normal":
            # Actualizar la duración (columna D, índice 3)
            row[3] = 40
            range_name = f"servicios!A{idx}:F{idx}"
            if sheets._update_row(range_name, row):
                logger.info(f"✅ Duración actualizada a 40 minutos")
            else:
                logger.error(f"❌ Error actualizando la duración")
            return
    
    logger.error("❌ No se encontró la fila del servicio en Sheets")


if __name__ == "__main__":
    main()
