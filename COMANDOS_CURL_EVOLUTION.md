# 📱 Comandos CURL para Evolution API

## 🔑 Credenciales

```bash
BASE_URL="https://n8n-evolution-api-barberia.dtbfmw.easypanel.host"
API_KEY="429683C4C977415CAAFCCE10F7D57E11"
INSTANCE="barberiaChurco"
```

---

## 📋 Obtener Lista de Chats/Contactos

### Opción 1: Fetch Profile Picture Base64 (puede dar info de contactos)

```bash
curl -X POST "https://n8n-evolution-api-barberia.dtbfmw.easypanel.host/chat/fetchProfilePictureUrl/barberiaChurco" \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "573123613840"
  }'
```

### Opción 2: Fetch Instance Info

```bash
curl -X GET "https://n8n-evolution-api-barberia.dtbfmw.easypanel.host/instance/fetchInstances" \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  -H "Content-Type: application/json"
```

### Opción 3: Connection State

```bash
curl -X GET "https://n8n-evolution-api-barberia.dtbfmw.easypanel.host/instance/connectionState/barberiaChurco" \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11" \
  -H "Content-Type: application/json"
```

---

## 💡 Solución Alternativa: Usar Google Sheets

Si Evolution API no tiene endpoint para listar chats, la mejor opción es obtener los números desde Google Sheets donde están los clientes registrados.

### Script Python para obtener desde Sheets:

```python
from services import SheetsClient

sheets = SheetsClient()
clientes = sheets._read_range("clientes!A2:C")

for row in clientes:
    if len(row) >= 3:
        telefono = row[2]
        nombre = row[1]
        print(f"{telefono} - {nombre}")
```

---

## 🎯 Recomendación

**Para enviar mensajes masivos**, usa los números de clientes que ya están en Google Sheets porque:

1. ✅ Son clientes reales que ya interactuaron con el bot
2. ✅ Tienen datos verificados (nombre, teléfono)
3. ✅ Es más seguro (menos riesgo de bloqueo)
4. ✅ Puedes filtrar por fecha de última cita

---

## 📝 Comando para Obtener Clientes desde Sheets

Ejecuta este script en el servidor donde está el bot:

```bash
cd /ruta/a/MVP-BARBERIA

python -c "
from services import SheetsClient

sheets = SheetsClient()
clientes = sheets._read_range('clientes!A2:C')

print('📱 CLIENTES REGISTRADOS:')
print('=' * 70)

for i, row in enumerate(clientes, 1):
    if len(row) >= 3:
        telefono = row[2]
        nombre = row[1]
        print(f'{i}. {telefono} - {nombre}')

print('\n📋 SOLO NÚMEROS:')
numeros = [row[2] for row in clientes if len(row) >= 3]
print(', '.join(numeros))
"
```

---

## 🔍 Verificar Endpoint Correcto de Evolution API

Si quieres encontrar el endpoint correcto, ejecuta:

```bash
# Ver documentación de la API
curl -X GET "https://n8n-evolution-api-barberia.dtbfmw.easypanel.host/docs" \
  -H "apikey: 429683C4C977415CAAFCCE10F7D57E11"

# O ver el Swagger/OpenAPI
# Abre en navegador:
# https://n8n-evolution-api-barberia.dtbfmw.easypanel.host/docs
```

---

## 💡 Nota Importante

Evolution API v2 puede tener diferentes endpoints según la versión. Los endpoints más comunes son:

- `/chat/findMessages/{instance}` - Buscar mensajes
- `/message/sendText/{instance}` - Enviar mensaje (✅ este funciona)
- `/instance/fetchInstances` - Info de instancias (✅ este funciona)
- `/chat/fetchAllContacts/{instance}` - Contactos (❌ no disponible en tu versión)

**Conclusión:** Usa Google Sheets para obtener la lista de clientes.

---

## 🚀 Script Recomendado

Usa el script `enviar_mensaje_masivo.py` que ya creamos, pero modifícalo para leer desde Google Sheets en lugar de Evolution API.

O mejor aún, crea una lista manual de números de clientes que quieres contactar.

