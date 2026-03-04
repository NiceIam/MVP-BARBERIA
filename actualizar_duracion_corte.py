"""Script para actualizar las duraciones de los servicios."""
from services import SheetsClient
from loguru import logger


def main():
    """Actualiza las duraciones de los servicios en Google Sheets."""
    logger.info("🔄 Actualizando duraciones de servicios...")
    
    sheets = SheetsClient()
    
    # Verificar conexión
    if not sheets.test_connection():
        logger.error("❌ No se pudo conectar a Google Sheets")
        return
    
    # Leer todos los servicios
    rows = sheets._read_range("servicios!A2:F")
    
    actualizados = 0
    
    for idx, row in enumerate(rows, start=2):
        if len(row) > 0:
            servicio_id = row[0]
            
            # Actualizar Corte + Barba a 60 minutos
            if servicio_id == "srv_corte_barba":
                logger.info(f"📋 Servicio: {row[1]}")
                logger.info(f"   Duración actual: {row[3]} minutos")
                row[3] = 60
                range_name = f"servicios!A{idx}:F{idx}"
                if sheets._update_row(range_name, row):
                    logger.info(f"✅ Duración actualizada a 60 minutos")
                    actualizados += 1
                else:
                    logger.error(f"❌ Error actualizando Corte + Barba")
            
            # Actualizar Corte Normal a 45 minutos
            elif servicio_id == "srv_corte_normal":
                logger.info(f"📋 Servicio: {row[1]}")
                logger.info(f"   Duración actual: {row[3]} minutos")
                row[3] = 45
                range_name = f"servicios!A{idx}:F{idx}"
                if sheets._update_row(range_name, row):
                    logger.info(f"✅ Duración actualizada a 45 minutos")
                    actualizados += 1
                else:
                    logger.error(f"❌ Error actualizando Corte Normal")
    
    if actualizados > 0:
        logger.info(f"✅ {actualizados} servicio(s) actualizado(s)")
    else:
        logger.warning("⚠️ No se actualizó ningún servicio")


if __name__ == "__main__":
    main()
