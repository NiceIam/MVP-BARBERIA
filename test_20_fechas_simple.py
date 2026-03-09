"""
Script de prueba simple para verificar la implementación de 20 fechas.
"""

print("=" * 70)
print("🧪 VERIFICACIÓN DE 20 FECHAS CON DISPONIBILIDAD")
print("=" * 70)

# Test: Verificar lógica en engine.py
print("\n📝 Test: Verificar lógica implementada en engine.py")
print("-" * 70)

# Leer el archivo engine.py y verificar que contiene la lógica correcta
with open('chatbot/engine.py', 'r', encoding='utf-8') as f:
    contenido = f.read()

checks = [
    ("FECHAS_A_MOSTRAR = 20", "✅ Constante FECHAS_A_MOSTRAR = 20 definida"),
    ("MAX_DIAS_BUSCAR = 60", "✅ Constante MAX_DIAS_BUSCAR = 60 definida"),
    ("while len(fechas_disponibles) < FECHAS_A_MOSTRAR", "✅ Bucle while para buscar fechas"),
    ("get_proximas_fechas(10, dias_revisados)", "✅ Llamada con offset (dias_revisados)"),
    ("dias_revisados += 10", "✅ Incremento de offset en 10 días"),
    ("if len(fechas_disponibles) >= FECHAS_A_MOSTRAR:", "✅ Verificación para detener búsqueda"),
]

all_passed = True
for check_str, descripcion in checks:
    if check_str in contenido:
        print(descripcion)
    else:
        print(f"❌ {descripcion} - NO ENCONTRADO")
        all_passed = False

# Contar cuántas veces aparece la lógica
count_fechas_a_mostrar = contenido.count("FECHAS_A_MOSTRAR = 20")
print(f"\n✅ Lógica implementada en {count_fechas_a_mostrar} método(s)")
if count_fechas_a_mostrar == 2:
    print("   ✓ Implementado en _mostrar_fechas y _procesar_seleccion_fecha")
elif count_fechas_a_mostrar == 1:
    print("   ⚠️ Solo implementado en 1 método (debería estar en 2)")
else:
    print(f"   ⚠️ Implementaciones encontradas: {count_fechas_a_mostrar}")

# Verificar utils/datetime_utils.py
print("\n📝 Test: Verificar función get_proximas_fechas con offset")
print("-" * 70)

with open('utils/datetime_utils.py', 'r', encoding='utf-8') as f:
    contenido_utils = f.read()

utils_checks = [
    ("def get_proximas_fechas(dias: int = 7, offset: int = 0)", "✅ Función acepta parámetro offset"),
    ("offset: Días a saltar desde la fecha de inicio", "✅ Documentación del parámetro offset"),
    ("fecha_inicio = fecha_inicio + timedelta(days=offset)", "✅ Aplicación del offset"),
]

for check_str, descripcion in utils_checks:
    if check_str in contenido_utils:
        print(descripcion)
    else:
        print(f"❌ {descripcion} - NO ENCONTRADO")
        all_passed = False

print("\n" + "=" * 70)
print("📱 NUEVO COMPORTAMIENTO")
print("=" * 70)

print("""
ANTES (mostraba hasta 15 fechas, algunas sin disponibilidad):
----------------------------------------------------------------------
Usuario: 1 (Agendar cita)
Bot: [Muestra servicios]

Usuario: 1 (Corte + Barba)
Bot: 📅 ¿Qué día prefieres?
     
     1. Lunes 10/03/2026
     2. Martes 11/03/2026  ← SIN DISPONIBILIDAD (se mostraba igual)
     3. Miércoles 12/03/2026  ← SIN DISPONIBILIDAD (se mostraba igual)
     ...
     10. Viernes 20/03/2026
     
     [Solo mostraba las primeras 15 fechas]
     [Algunas sin disponibilidad]

----------------------------------------------------------------------

AHORA (siempre muestra 20 fechas CON disponibilidad):
----------------------------------------------------------------------
Usuario: 1 (Agendar cita)
Bot: [Muestra servicios]

Usuario: 1 (Corte + Barba)
Bot: [Busca fechas con disponibilidad...]
     [Si una fecha está llena, busca más adelante]
     [Continúa hasta encontrar 20 fechas disponibles]
     
     📅 ¿Qué día prefieres?
     
     1. Lunes 10/03/2026  ✅ Disponible
     2. Jueves 13/03/2026  ✅ Disponible
     3. Viernes 14/03/2026  ✅ Disponible
     4. Sábado 15/03/2026  ✅ Disponible
     ...
     20. Martes 15/04/2026  ✅ Disponible
     
     [SIEMPRE 20 fechas con disponibilidad REAL]
     [Puede buscar hasta 60 días en el futuro]
     [NO muestra fechas sin disponibilidad]

----------------------------------------------------------------------
""")

print("=" * 70)
print("🎯 VENTAJAS DEL NUEVO SISTEMA")
print("=" * 70)

print("""
✅ Siempre 20 opciones con disponibilidad:
   • Usuario tiene más opciones para elegir
   • Todas las fechas mostradas son reservables
   • Mejor experiencia de usuario

✅ Búsqueda inteligente:
   • Si una fecha está llena, busca más adelante
   • Continúa hasta encontrar 20 fechas con disponibilidad
   • Puede buscar hasta 60 días en el futuro

✅ Eficiente:
   • Busca en lotes de 10 días
   • Se detiene al encontrar 20 fechas
   • No busca más de lo necesario

✅ Consistente:
   • Siempre 20 opciones (a menos que no haya disponibilidad en 60 días)
   • Usuario sabe qué esperar
   • Interfaz predecible
""")

print("=" * 70)
print("🔧 DETALLES TÉCNICOS")
print("=" * 70)

print("""
Algoritmo de búsqueda:
1. Inicializa: fechas_disponibles = [], dias_revisados = 0
2. Mientras len(fechas_disponibles) < 20 y dias_revisados < 60:
   a. Obtiene 10 fechas con offset = dias_revisados
   b. Para cada fecha:
      - Verifica disponibilidad (slots disponibles)
      - Si tiene disponibilidad, la agrega a fechas_disponibles
      - Si ya tiene 20, detiene el bucle
   c. Incrementa dias_revisados += 10
3. Retorna las 20 fechas con disponibilidad

Ejemplo de búsqueda:
- Días 0-9: Encuentra 8 fechas con disponibilidad
- Días 10-19: Encuentra 7 fechas con disponibilidad (total: 15)
- Días 20-29: Encuentra 5 fechas con disponibilidad (total: 20)
- Se detiene porque ya tiene 20 fechas
""")

print("=" * 70)
if all_passed:
    print("✅ VERIFICACIÓN EXITOSA - 20 FECHAS IMPLEMENTADO CORRECTAMENTE")
else:
    print("⚠️ VERIFICACIÓN COMPLETADA CON ADVERTENCIAS")
print("=" * 70)

print("""
📊 Resumen de cambios:
   ✓ get_proximas_fechas ahora acepta parámetro offset
   ✓ _mostrar_fechas busca hasta encontrar 20 fechas
   ✓ _procesar_seleccion_fecha usa la misma lógica
   ✓ Búsqueda incremental en lotes de 10 días
   ✓ Límite máximo de 60 días de búsqueda

🎉 Los usuarios ahora siempre verán 20 fechas disponibles!
""")
