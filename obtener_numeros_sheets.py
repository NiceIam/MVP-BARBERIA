"""Script para obtener números de teléfono desde Google Sheets."""
import os
import sys
from datetime import datetime

print("=" * 70)
print("📱 OBTENER NÚMEROS DESDE GOOGLE SHEETS")
print("=" * 70)

try:
    from services import SheetsClient
    
    print("\n🔍 Conectando a Google Sheets...")
    sheets = SheetsClient()
    
    # Obtener clientes
    print("📋 Obteniendo clientes...")
    clientes_data = sheets._read_range("clientes!A2:C")
    
    if not clientes_data:
        print("❌ No se encontraron clientes en Google Sheets")
        sys.exit(1)
    
    print(f"✅ Se encontraron {len(clientes_data)} clientes")
    
    # Procesar clientes
    clientes = []
    for row in clientes_data:
        if len(row) >= 3:
            cliente_id = row[0]
            nombre = row[1]
            telefono = row[2]
            clientes.append({
                'id': cliente_id,
                'nombre': nombre,
                'telefono': telefono
            })
    
    print(f"\n📊 Total de clientes con teléfono: {len(clientes)}")
    
    # Mostrar primeros 50
    print("\n📋 LISTA DE CLIENTES (primeros 50):")
    print("=" * 70)
    
    for i, cliente in enumerate(clientes[:50], 1):
        print(f"{i}. {cliente['telefono']} - {cliente['nombre']}")
    
    if len(clientes) > 50:
        print(f"\n... y {len(clientes) - 50} más")
    
    # Solo números
    print("\n📱 SOLO NÚMEROS (primeros 50):")
    print("=" * 70)
    numeros = [c['telefono'] for c in clientes[:50]]
    print(", ".join(numeros))
    
    # Exportar a archivo
    print("\n💾 Exportando a archivo...")
    filename = f"numeros_clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("NÚMEROS DE CLIENTES - BARBERÍA CHURCO\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(clientes)}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("LISTA COMPLETA:\n")
        f.write("-" * 70 + "\n")
        for i, cliente in enumerate(clientes, 1):
            f.write(f"{i}. {cliente['telefono']} - {cliente['nombre']}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("SOLO NÚMEROS (separados por coma):\n")
        f.write("-" * 70 + "\n")
        todos_numeros = [c['telefono'] for c in clientes]
        f.write(", ".join(todos_numeros))
        f.write("\n\n")
        
        f.write("SOLO NÚMEROS (uno por línea):\n")
        f.write("-" * 70 + "\n")
        for numero in todos_numeros:
            f.write(f"{numero}\n")
    
    print(f"✅ Archivo creado: {filename}")
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"Total de clientes: {len(clientes)}")
    print(f"Archivo exportado: {filename}")
    print(f"\n💡 Usa estos números para enviar mensajes masivos con:")
    print(f"   python enviar_mensaje_masivo.py")
    
except ImportError as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Instala las dependencias:")
    print("   pip install -r requirements.txt")
    
except FileNotFoundError as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Configura las credenciales de Google:")
    print("   1. Descarga service_account.json")
    print("   2. Colócalo en la raíz del proyecto")
    print("   3. O ejecuta: python configurar_credenciales.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Verifica:")
    print("   1. Credenciales de Google configuradas")
    print("   2. Google Sheets ID correcto")
    print("   3. Sheet 'clientes' existe")

print("\n")
