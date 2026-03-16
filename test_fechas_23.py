import sys
import io

# Force UTF-8 encoding on standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
from chatbot.engine import ChatbotEngine

def run_interaction(engine, interaction_sequence):
    mensaje_actual = interaction_sequence.pop(0)
    print(f"\n--- USER: '{mensaje_actual}' ---")
    respuesta = engine.procesar_mensaje("5551234567", mensaje_actual)
    print(respuesta)
    return respuesta

def main():
    print("Testing Date Generation Sequence")
    engine = ChatbotEngine()
    engine.sheets.eliminar_sesion("5551234567") # Clean any past session

    # Say hello to get options
    run_interaction(engine, ['hola'])
    
    # Send 1 to Make an appointment
    run_interaction(engine, ['1'])
    
    # Enter Name 
    run_interaction(engine, ['Daniel'])
    
    # Select cut
    run_interaction(engine, ['1'])
    
    # This next interaction should output the days option. Let's see it.
    engine.sheets.eliminar_sesion("5551234567")

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    main()
