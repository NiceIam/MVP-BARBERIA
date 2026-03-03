# 🔄 Guía de Migración a Google Sheets + Calendar

## Cambios Principales

### ❌ Eliminado
- PostgreSQL y todas sus dependencias
- `database.py`
- `setup_database.py`, `reset_database.py`, `check_database.py`
- Conexiones a base de datos relacional

### ✅ Agregado
- Google Sheets como base de datos
- Google Calendar para sincronización automática
- Service Account authentication
- Nuevos modelos de datos optimizados
- Utilidades para cálculo de disponibilidad

## Estructura Nueva

```
barberia-churco/
├── config/              # Configuración
│   ├── settings.py      # Variables de entorno
│   └── constants.py     # Constantes del negocio
├── models/              # Modelos de datos
│   ├── cliente.py
│   ├── cita.py
│   ├── servicio.py
│   └── sesion.py
├── services/            # Servicios externos
│   ├── google_sheets.py
│   ├── google_calendar.py
│   ├── evolution_api.py
│   └── whatsapp.py
├── chatbot/             # Motor del chatbot
│   ├── engine.py
│   └── validaciones.py
├── utils/               # Utilidades
│   ├── datetime_utils.py
│   ├── disponibilidad.py
│   └── formatters.py
├── scripts/             # Scripts de utilidad
│   └── seed_data.py
└── server.py            # Servidor FastAPI
```

## Pasos de Migración

### 1. Configurar Google Cloud

```bash
# 1. Ir a https://console.cloud.google.com
# 2. Crear proyecto: barberia-churco
# 3. Habilitar APIs:
#    - Google Sheets API
#    - Google Calendar API
# 4. Crear Service Account
# 5. Descargar credenciales JSON
# 6. Guardar como service_account.json
```

### 2. Crear Google Sheet

```bash
# 1. Crear nuevo Google Sheet
# 2. Nombrar: Barberia_Churco_DB
# 3. Crear 5 sheets (tabs):
#    - clientes
#    - citas
#    - servicios
#    - disponibilidad
#    - sesiones_chat
```

### 3. Configurar Headers

#### Sheet: clientes
```
id | telefono | nombre | fecha_registro | total_citas | ultima_cita
```

#### Sheet: citas
```
id | cliente_id | cliente_telefono | cliente_nombre | servicio_id | servicio_nombre | precio | fecha | hora_inicio | hora_fin | estado | calendar_event_id | fecha_creacion | fecha_modificacion | notas
```

#### Sheet: servicios
```
id | nombre | precio | duracion_minutos | activo | orden
```

#### Sheet: disponibilidad
```
id | dia_semana | hora_inicio | hora_fin | activo
```

#### Sheet: sesiones_chat
```
telefono | estado | datos_temp | ultima_actividad | cita_en_proceso
```

### 4. Compartir Recursos

```bash
# Copiar email del Service Account
# Ejemplo: barberia-churco@proyecto.iam.gserviceaccount.com

# Compartir Google Sheet con ese email (Editor)
# Compartir Google Calendar con ese email (Hacer cambios en eventos)
```

### 5. Configurar .env

```bash
cp .env.example .env
# Editar .env con tus valores
```

### 6. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 7. Poblar Datos Iniciales

```bash
python scripts/seed_data.py
```

### 8. Probar Conexiones

```bash
python -c "from services import SheetsClient; SheetsClient().test_connection()"
python -c "from services import CalendarClient; CalendarClient().test_connection()"
```

### 9. Iniciar Servidor

```bash
python server.py
```

## Diferencias Clave

### Antes (PostgreSQL)
```python
# Conexión
db = get_database()

# Crear cita
db.crear_cita(datos)

# Buscar citas
citas = db.obtener_citas_por_telefono(telefono)
```

### Ahora (Google Sheets)
```python
# Conexión
sheets = SheetsClient()

# Crear cita
sheets.crear_cita(cita)

# Buscar citas
citas = sheets.get_citas_por_telefono(telefono)
```

## Ventajas de la Nueva Arquitectura

1. **Sin infraestructura**: No necesitas servidor de BD
2. **Visual**: Puedes ver/editar datos en Google Sheets
3. **Sincronización**: Calendar se actualiza automáticamente
4. **Backup**: Google maneja backups automáticos
5. **Colaboración**: Múltiples personas pueden ver los datos
6. **Costo**: Gratis hasta límites muy altos

## Limitaciones

1. **Performance**: Más lento que PostgreSQL para queries complejas
2. **Límites de API**: 100 requests/100 segundos
3. **Concurrencia**: Menos robusto para alta concurrencia
4. **Queries**: No hay SQL, solo lectura/escritura de rangos

## Cuándo Migrar a BD Real

Considera migrar a PostgreSQL/MongoDB cuando:
- Más de 1000 citas/mes
- Más de 3 barberos
- Necesitas reportes complejos
- Problemas de performance
- Límites de API se vuelven problema

## Troubleshooting

### Error: "Permission denied"
```bash
# Verificar que el Service Account tenga permisos
# Compartir Sheet y Calendar con el email del SA
```

### Error: "Quota exceeded"
```bash
# Implementar caché
# Reducir frecuencia de requests
# Usar batch requests
```

### Error: "Invalid credentials"
```bash
# Verificar que service_account.json esté en la raíz
# Verificar que los scopes sean correctos
# Regenerar credenciales si es necesario
```

## Soporte

Ver `ARQUITECTURA_GOOGLE.md` para detalles técnicos completos.
