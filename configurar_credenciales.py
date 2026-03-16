"""Script interactivo para configurar credenciales de Google."""
import os
import json
from pathlib import Path

print("=" * 70)
print("🔧 CONFIGURADOR DE CREDENCIALES DE GOOGLE")
print("=" * 70)

print("\n📋 Este script te ayudará a configurar las credenciales de Google.")
print("   Necesitas tener el archivo JSON de la Service Account.")

# Verificar si ya existe configuración
env_file = Path(".env")
service_account_file = Path("service_account.json")

print("\n1️⃣ Estado Actual:")
print("-" * 70)

if env_file.exists():
    print("✅ Archivo .env existe")
    with open(env_file, 'r') as f:
        content = f.read()
        if 'GOOGLE_SERVICE_ACCOUNT_FILE' in content:
            print("✅ Variable GOOGLE_SERVICE_ACCOUNT_FILE configurada")
        else:
            print("⚠️  Variable GOOGLE_SERVICE_ACCOUNT_FILE NO configurada")
else:
    print("❌ Archivo .env NO existe")

if service_account_file.exists():
    print("✅ Archivo service_account.json existe")
else:
    print("❌ Archivo service_account.json NO existe")

# Opciones
print("\n2️⃣ ¿Cómo quieres configurar las credenciales?")
print("-" * 70)
print("1. Tengo el archivo service_account.json")
print("2. Tengo el JSON como texto")
print("3. Necesito ayuda para obtener las credenciales")
print("4. Salir")

opcion = input("\nSelecciona una opción (1-4): ").strip()

if opcion == "1":
    # Opción 1: Archivo JSON
    print("\n📁 Configuración con archivo JSON")
    print("-" * 70)
    
    ruta = input("Ingresa la ruta del archivo JSON (o presiona Enter si está en la raíz): ").strip()
    
    if not ruta:
        ruta = "service_account.json"
    
    ruta_path = Path(ruta)
    
    if not ruta_path.exists():
        print(f"\n❌ ERROR: El archivo {ruta} no existe")
        print("\n💡 Asegúrate de:")
        print("   1. Haber descargado el archivo de Google Cloud Console")
        print("   2. Colocarlo en la raíz del proyecto")
        print("   3. Que se llame 'service_account.json'")
        exit(1)
    
    # Validar que es un JSON válido
    try:
        with open(ruta_path, 'r') as f:
            creds = json.load(f)
        
        # Verificar campos requeridos
        required = ['type', 'project_id', 'private_key', 'client_email']
        missing = [f for f in required if f not in creds]
        
        if missing:
            print(f"\n❌ ERROR: El JSON no tiene los campos requeridos: {', '.join(missing)}")
            exit(1)
        
        print(f"\n✅ JSON válido")
        print(f"   - Project: {creds.get('project_id')}")
        print(f"   - Email: {creds.get('client_email')}")
        
        # Copiar a service_account.json si no está ahí
        if ruta != "service_account.json":
            import shutil
            shutil.copy(ruta_path, "service_account.json")
            print(f"\n✅ Archivo copiado a service_account.json")
        
        # Crear/actualizar .env
        env_content = ""
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # Actualizar o agregar variable
        if 'GOOGLE_SERVICE_ACCOUNT_FILE=' in env_content:
            # Reemplazar
            lines = env_content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('GOOGLE_SERVICE_ACCOUNT_FILE='):
                    new_lines.append('GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json')
                else:
                    new_lines.append(line)
            env_content = '\n'.join(new_lines)
        else:
            # Agregar
            if env_content and not env_content.endswith('\n'):
                env_content += '\n'
            env_content += '\n# Google Service Account\n'
            env_content += 'GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json\n'
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ Archivo .env actualizado")
        
        print("\n" + "=" * 70)
        print("✅ CONFIGURACIÓN EXITOSA")
        print("=" * 70)
        print(f"\n📧 IMPORTANTE: Comparte tu Google Sheet y Calendar con:")
        print(f"   {creds.get('client_email')}")
        print("\n📋 Pasos:")
        print("   1. Abre tu Google Sheet")
        print("   2. Click en 'Compartir'")
        print("   3. Pega el email de arriba")
        print("   4. Dale permisos de 'Editor'")
        print("   5. Repite para Google Calendar")
        
    except json.JSONDecodeError as e:
        print(f"\n❌ ERROR: El archivo no es un JSON válido: {e}")
        exit(1)

elif opcion == "2":
    # Opción 2: JSON como texto
    print("\n📝 Configuración con JSON como texto")
    print("-" * 70)
    print("Pega el contenido completo del JSON (debe empezar con { y terminar con }):")
    print("(Presiona Enter dos veces cuando termines)")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    
    json_text = '\n'.join(lines)
    
    try:
        creds = json.loads(json_text)
        
        # Verificar campos requeridos
        required = ['type', 'project_id', 'private_key', 'client_email']
        missing = [f for f in required if f not in creds]
        
        if missing:
            print(f"\n❌ ERROR: El JSON no tiene los campos requeridos: {', '.join(missing)}")
            exit(1)
        
        print(f"\n✅ JSON válido")
        print(f"   - Project: {creds.get('project_id')}")
        print(f"   - Email: {creds.get('client_email')}")
        
        # Guardar como archivo
        with open('service_account.json', 'w') as f:
            json.dump(creds, f, indent=2)
        
        print(f"\n✅ Guardado como service_account.json")
        
        # Crear/actualizar .env
        env_content = ""
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()
        
        # JSON en una línea para variable de entorno
        json_oneline = json.dumps(creds)
        
        # Actualizar o agregar variable
        if 'GOOGLE_SERVICE_ACCOUNT_FILE=' in env_content:
            # Reemplazar
            lines = env_content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('GOOGLE_SERVICE_ACCOUNT_FILE='):
                    new_lines.append(f'GOOGLE_SERVICE_ACCOUNT_FILE={json_oneline}')
                else:
                    new_lines.append(line)
            env_content = '\n'.join(new_lines)
        else:
            # Agregar
            if env_content and not env_content.endswith('\n'):
                env_content += '\n'
            env_content += '\n# Google Service Account\n'
            env_content += f'GOOGLE_SERVICE_ACCOUNT_FILE={json_oneline}\n'
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ Archivo .env actualizado")
        
        print("\n" + "=" * 70)
        print("✅ CONFIGURACIÓN EXITOSA")
        print("=" * 70)
        print(f"\n📧 IMPORTANTE: Comparte tu Google Sheet y Calendar con:")
        print(f"   {creds.get('client_email')}")
        print("\n📋 Pasos:")
        print("   1. Abre tu Google Sheet")
        print("   2. Click en 'Compartir'")
        print("   3. Pega el email de arriba")
        print("   4. Dale permisos de 'Editor'")
        print("   5. Repite para Google Calendar")
        
    except json.JSONDecodeError as e:
        print(f"\n❌ ERROR: El texto no es un JSON válido: {e}")
        exit(1)

elif opcion == "3":
    # Opción 3: Ayuda
    print("\n📚 GUÍA PARA OBTENER CREDENCIALES")
    print("=" * 70)
    print("""
1. Ve a Google Cloud Console:
   https://console.cloud.google.com

2. Crea o selecciona un proyecto

3. Habilita las APIs necesarias:
   - Google Sheets API
   - Google Calendar API
   
   Ve a: APIs & Services > Library
   Busca cada API y click en "Enable"

4. Crea una Service Account:
   - Ve a: IAM & Admin > Service Accounts
   - Click en "+ CREATE SERVICE ACCOUNT"
   - Nombre: barberia-churco-bot
   - Rol: Editor
   - Click en "CREATE AND CONTINUE" > "DONE"

5. Genera la clave JSON:
   - Click en la cuenta de servicio creada
   - Ve a la pestaña "KEYS"
   - Click en "ADD KEY" > "Create new key"
   - Selecciona "JSON"
   - Click en "CREATE"
   - Se descargará un archivo JSON

6. Ejecuta este script de nuevo con la opción 1 o 2

7. IMPORTANTE: Comparte tu Google Sheet y Calendar con el email
   de la cuenta de servicio (client_email del JSON)
""")

else:
    print("\n👋 Saliendo...")
    exit(0)

print("\n🧪 ¿Quieres probar la configuración ahora? (s/n): ", end="")
probar = input().strip().lower()

if probar == 's':
    print("\n🔍 Ejecutando diagnóstico...")
    os.system("python diagnostico_google_auth.py")
else:
    print("\n💡 Puedes probar la configuración ejecutando:")
    print("   python diagnostico_google_auth.py")

print("\n✅ ¡Listo! Ahora puedes iniciar el servidor:")
print("   python server.py")
print()
