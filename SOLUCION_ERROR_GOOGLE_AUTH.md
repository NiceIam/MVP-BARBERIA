# 🔴 SOLUCIÓN: Error de Autenticación de Google

## ❌ Error Identificado

```
ERROR: ('invalid_grant: Invalid grant: account not found', 
{'error': 'invalid_grant', 'error_description': 'Invalid grant: account not found'})
```

## 🎯 Causa del Problema

Las credenciales de Google (Service Account) están:
- ❌ Expiradas
- ❌ Eliminadas
- ❌ Mal configuradas
- ❌ No existen

## 🔧 SOLUCIÓN RÁPIDA

### Opción 1: Verificar Variables de Entorno (PRODUCCIÓN)

Si estás en producción (Docker/servidor), verifica que las variables de entorno estén configuradas:

```bash
# En tu servidor/panel de control, verifica estas variables:
GOOGLE_SERVICE_ACCOUNT_FILE=<JSON completo de credenciales>
GOOGLE_SHEETS_ID=<ID de tu Google Sheet>
GOOGLE_CALENDAR_ID=<Email del calendario>
```

### Opción 2: Crear Archivo .env (DESARROLLO)

Si estás en desarrollo local, crea un archivo `.env` en la raíz de MVP-BARBERIA:

```env
# Google Service Account
GOOGLE_SERVICE_ACCOUNT_FILE={"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}

# Google Sheets
GOOGLE_SHEETS_ID=1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT

# Google Calendar
GOOGLE_CALENDAR_ID=churcobarberstudio@gmail.com
TIMEZONE=America/Bogota

# Evolution API
EVOLUTION_API_URL=https://n8n-evolution-api-barberia.dtbfmw.easypanel.host
EVOLUTION_API_KEY=5A4F8619174B-4484-863B-D636DEAFB2B0
EVOLUTION_INSTANCE_NAME=barberiaChurco

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 📋 PASOS DETALLADOS PARA RESOLVER

### 1. Crear Nueva Service Account

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Selecciona tu proyecto (o crea uno nuevo)
3. Ve a **IAM & Admin** > **Service Accounts**
4. Click en **+ CREATE SERVICE ACCOUNT**
5. Nombre: `barberia-churco-bot`
6. Descripción: `Bot para gestión de citas`
7. Click **CREATE AND CONTINUE**

### 2. Asignar Permisos

1. Rol: **Editor** (o permisos específicos)
2. Click **CONTINUE**
3. Click **DONE**

### 3. Generar Clave JSON

1. Click en la cuenta de servicio creada
2. Ve a la pestaña **KEYS**
3. Click **ADD KEY** > **Create new key**
4. Selecciona **JSON**
5. Click **CREATE**
6. Se descargará un archivo JSON

### 4. Habilitar APIs

1. Ve a **APIs & Services** > **Library**
2. Busca y habilita:
   - **Google Sheets API**
   - **Google Calendar API**

### 5. Compartir Google Sheet y Calendar

**IMPORTANTE:** Debes compartir tus recursos con la cuenta de servicio:

1. Abre el archivo JSON descargado
2. Copia el valor de `client_email` (ejemplo: `barberia-churco-bot@proyecto.iam.gserviceaccount.com`)
3. Ve a tu Google Sheet
4. Click en **Compartir**
5. Pega el email de la cuenta de servicio
6. Dale permisos de **Editor**
7. Repite para Google Calendar

### 6. Configurar en tu Sistema

#### Si estás en PRODUCCIÓN (Docker/Servidor):

1. Ve a tu panel de control (EasyPanel, Heroku, etc.)
2. Busca la sección de **Variables de Entorno**
3. Agrega/actualiza:

```
GOOGLE_SERVICE_ACCOUNT_FILE = <pega todo el contenido del JSON en una línea>
```

**Ejemplo:**
```
GOOGLE_SERVICE_ACCOUNT_FILE={"type":"service_account","project_id":"barberia-123","private_key_id":"abc123...","private_key":"-----BEGIN PRIVATE KEY-----\nMIIE...","client_email":"barberia-bot@barberia-123.iam.gserviceaccount.com",...}
```

4. Reinicia el servicio/contenedor

#### Si estás en DESARROLLO LOCAL:

1. Crea archivo `.env` en MVP-BARBERIA/
2. Copia el contenido del JSON en una línea
3. Pégalo en la variable `GOOGLE_SERVICE_ACCOUNT_FILE`

O simplemente:

1. Renombra el archivo descargado a `service_account.json`
2. Colócalo en la raíz de MVP-BARBERIA/
3. Actualiza `.env`:
```env
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
```

## 🧪 Verificar la Solución

Ejecuta el script de diagnóstico:

```bash
cd MVP-BARBERIA
python diagnostico_google_auth.py
```

Deberías ver:

```
✅ DIAGNÓSTICO EXITOSO - Credenciales funcionan correctamente
```

## 🚀 Reiniciar el Servicio

### En Producción:
```bash
# Reinicia tu contenedor/servicio desde el panel de control
```

### En Desarrollo:
```bash
cd MVP-BARBERIA
python server.py
```

## ⚠️ Problemas Comunes

### 1. "JSON inválido"
- Asegúrate de que el JSON esté en UNA SOLA LÍNEA
- No debe tener saltos de línea dentro de la variable de entorno
- Usa comillas dobles, no simples

### 2. "Account not found" persiste
- Verifica que la cuenta de servicio existe en Google Cloud Console
- Verifica que no fue eliminada
- Crea una nueva si es necesario

### 3. "Permission denied"
- Verifica que compartiste el Sheet y Calendar con el `client_email`
- Verifica que tiene permisos de Editor

### 4. "API not enabled"
- Habilita Google Sheets API
- Habilita Google Calendar API
- En Google Cloud Console > APIs & Services > Library

## 📞 Verificación Final

Después de aplicar la solución:

1. ✅ El bot debe responder a mensajes de WhatsApp
2. ✅ Debe poder leer/escribir en Google Sheets
3. ✅ Debe poder crear eventos en Google Calendar
4. ✅ No debe aparecer el error "invalid_grant"

## 💡 Prevención Futura

1. **Backup de credenciales:** Guarda el JSON en un lugar seguro
2. **Documentación:** Anota el email de la cuenta de servicio
3. **Monitoreo:** Configura alertas para errores de autenticación
4. **Rotación:** Considera rotar credenciales cada 6-12 meses

---

**Última actualización:** 15 de Marzo, 2026  
**Estado:** Guía de solución completa
