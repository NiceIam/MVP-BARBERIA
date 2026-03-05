"""Demostración visual de cómo se ven los mensajes con la opción de menú."""


def simular_mensaje(titulo, mensaje_original):
    """Simula cómo se vería un mensaje con la opción de menú."""
    mensaje_con_menu = f"{mensaje_original}\n\n_Escribe *hola* para volver al menú principal._"
    
    print("─" * 70)
    print(f"📱 {titulo}")
    print("─" * 70)
    print(mensaje_con_menu)
    print()


def main():
    """Muestra ejemplos de diferentes tipos de mensajes."""
    print("=" * 70)
    print("📱 DEMOSTRACIÓN DE MENSAJES DEL CHATBOT")
    print("=" * 70)
    print()
    
    # Ejemplo 1: Menú Principal
    simular_mensaje(
        "MENÚ PRINCIPAL",
        """💈 *Bienvenido a Barbería Churco*

¿Qué deseas hacer?

1. Agendar cita
2. Consultar mi cita
3. Cancelar cita
4. Reagendar cita
5. Información de la barbería
6. Contactar al barbero

Responde con el número de la opción."""
    )
    
    # Ejemplo 2: Selección de Servicio
    simular_mensaje(
        "SELECCIÓN DE SERVICIO",
        """✂️ *Selecciona tu servicio:*

1. Corte + Barba
   💰 $28,000 COP
   ⏱️ 45 minutos

2. Corte Normal
   💰 $20,000 COP
   ⏱️ 40 minutos

Responde con el número del servicio."""
    )
    
    # Ejemplo 3: Selección de Fecha
    simular_mensaje(
        "SELECCIÓN DE FECHA",
        """📅 *¿Qué día prefieres?*

ℹ️ La agenda está llena hasta el domingo 8 de marzo. Si quieres agendar una cita para esta semana llámame a este número.

1. Lunes 10/03/2026
2. Martes 11/03/2026
3. Miércoles 12/03/2026
4. Jueves 13/03/2026
5. Viernes 14/03/2026

Responde con el número del día."""
    )
    
    # Ejemplo 4: Selección de Hora
    simular_mensaje(
        "SELECCIÓN DE HORA",
        """🕐 *¿A qué hora?*

1. 8:00 AM
2. 8:45 AM
3. 9:30 AM
4. 10:15 AM
5. 11:00 AM
6. 11:30 AM
7. 2:00 PM
8. 2:45 PM
9. 3:30 PM
10. 4:15 PM

Responde con el número de la hora.

💡 Si no encuentras un horario que te sirva, escribe *volver* para elegir otra fecha."""
    )
    
    # Ejemplo 5: Confirmación
    simular_mensaje(
        "CONFIRMACIÓN DE CITA",
        """📋 *Confirma tu cita:*

📅 Lunes 10 de marzo de 2026
🕐 2:00 PM - 2:45 PM
✂️ Corte + Barba
💰 $28,000 COP
👨‍💼 Barbero: Churco

Responde *SI* para confirmar o *NO* para cancelar."""
    )
    
    # Ejemplo 6: Cita Confirmada
    simular_mensaje(
        "CITA CONFIRMADA",
        """✅ *¡Cita confirmada!*

📆 Lunes 10 de marzo de 2026
🕐 2:00 PM
✂️ Corte + Barba
💰 $28,000 COP

Te esperamos en Barbería Churco.
Recuerda llegar 5 minutos antes."""
    )
    
    # Ejemplo 7: Error
    simular_mensaje(
        "MENSAJE DE ERROR",
        "Opción inválida. Por favor responde con un número del 1 al 5."
    )
    
    # Ejemplo 8: Sin Citas
    simular_mensaje(
        "SIN CITAS AGENDADAS",
        "No tienes citas agendadas."
    )
    
    # Ejemplo 9: Cancelación Exitosa
    simular_mensaje(
        "CANCELACIÓN EXITOSA",
        "✅ Cita cancelada exitosamente. Puedes agendar una nueva cuando quieras."
    )
    
    # Ejemplo 10: Información de la Barbería
    simular_mensaje(
        "INFORMACIÓN DE LA BARBERÍA",
        """💈 *Barbería Churco*

📍 *Dirección:*
Calle 17 # 25-23
Barrio Santa Teresita

⏰ *Horarios:*
Todos los días
• Mañana: 8:00 AM - 12:15 PM
• Tarde: 2:00 PM - 8:15 PM

✂️ *Servicios:*
• Corte + Barba: $28,000 COP (45 min)
• Corte Normal: $20,000 COP (40 min)

👨‍💼 *Barbero:*
Churco"""
    )
    
    print("=" * 70)
    print("✅ TODOS LOS MENSAJES INCLUYEN LA OPCIÓN DE VOLVER AL MENÚ")
    print("=" * 70)
    print()
    print("💡 Beneficios:")
    print("   • Los usuarios siempre saben cómo volver al menú")
    print("   • Reduce la frustración si se pierden en el flujo")
    print("   • Mejora la experiencia de usuario")
    print("   • Hace el chatbot más intuitivo y amigable")
    print()


if __name__ == "__main__":
    main()
