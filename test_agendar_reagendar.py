import sys
import io

# Force UTF-8 encoding on standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from chatbot.engine import ChatbotEngine
from services.google_calendar import CalendarClient

def run_interaction(engine, mensaje_actual):
    print(f"\n--- USER: '{mensaje_actual}' ---")
    respuesta = engine.procesar_mensaje("5551234567", mensaje_actual)
    print(respuesta)
    return respuesta

def main():
    print("Testing Date Generation Sequence - Batched")
    engine = ChatbotEngine()
    engine.sheets.eliminar_sesion("5551234567") # Clean any past session

    # AGENDAR FLUJO
    print(">>> 1. AGENDANDO CITA")
    run_interaction(engine, 'hola')
    run_interaction(engine, '1') # Agendar
    run_interaction(engine, 'DanielTestBatch') # Name
    run_interaction(engine, '1') # Servicio
    run_interaction(engine, '1') # Fecha 1
    run_interaction(engine, '1') # Hora 1
    
    # Check if we should confirm
    r = run_interaction(engine, 'SI') # Confirmar

    print("\n\n>>> 2. REAGENDANDO CITA")
    # REAGENDAR FLUJO
    run_interaction(engine, 'hola')
    run_interaction(engine, '4') # Reagendar
    # Asumimos que elegimos la 1, si hay varias
    run_interaction(engine, '1') # cita a reagendar si aparece, o confirmacion si es unica
    
    # Elegir nueva fecha y hora
    run_interaction(engine, 'SI') # SI continuar
    run_interaction(engine, '2') # Dia 2
    run_interaction(engine, '2') # Hora 2
    run_interaction(engine, 'SI') # Confirmar Reagendamiento
    
    print("\n\n>>> 3. CANCELAR CITA")
    run_interaction(engine, 'hola')
    run_interaction(engine, '3') # Cancelar
    run_interaction(engine, '1') 
    run_interaction(engine, 'SI') # Confirmar
    
    print("\n✓ PRUEBA FINALIZADA")

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    main()
