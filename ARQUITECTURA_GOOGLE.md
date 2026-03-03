# 🏗️ Arquitectura Técnica - MVP Barbería Churco

## 1. Arquitectura Propuesta (Alto Nivel)

```
┌─────────────────┐
│   WhatsApp      │
│   (Cliente)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Evolution API   │
│   (Webhook)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (Orquestador)  │
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
│ Google Sheets   │  │   Google     │  │   Chatbot    │
│   (Database)    │  │   Calendar   │  │    Engine    │
└─────────────────┘  └──────────────┘  └──────────────┘
```

### Flujo de Datos
1. Usuario envía mensaje → Evolution API → FastAPI
2. FastAPI consulta disponibilidad en Google Sheets
3. Usuario confirma → FastAPI escribe en Sheets + crea evento en Calendar
4. Respuesta → Evolution API → WhatsApp

### Stack Técnico
- **Backend**: FastAPI (Python 3.11+)
- **Database**: Google Sheets API v4
- **Calendar**: Google Calendar API v3
- **Auth**: Service Account (OAuth2)
- **Chatbot**: Máquina de estados conversacional


## 2. Modelo de Datos en Google Sheets

### Archivo: `Barberia_Churco_DB`
**ID**: `1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT`

### Estructura de Sheets (5 tabs)

#### Sheet 1: `clientes`
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| id | STRING | UUID generado | `cli_abc123` |
| telefono | STRING | Número WhatsApp (sin +) | `573001234567` |
| nombre | STRING | Nombre del cliente | `Juan Pérez` |
| fecha_registro | DATETIME | ISO 8601 | `2025-03-02T14:30:00-05:00` |
| total_citas | INTEGER | Contador de citas | `5` |
| ultima_cita | DATE | Última visita | `2025-03-01` |

**Índice único**: `telefono`
**Validaciones**: 
- telefono debe tener 10-13 dígitos
- nombre mínimo 2 caracteres

---

#### Sheet 2: `citas`
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| id | STRING | UUID generado | `cita_xyz789` |
| cliente_id | STRING | FK a clientes.id | `cli_abc123` |
| cliente_telefono | STRING | Denormalizado para búsqueda | `573001234567` |
| cliente_nombre | STRING | Denormalizado | `Juan Pérez` |
| servicio_id | STRING | FK a servicios.id | `srv_corte_barba` |
| servicio_nombre | STRING | Denormalizado | `Corte + Barba` |
| precio | INTEGER | Precio en COP | `28000` |
| fecha | DATE | Fecha de la cita | `2025-03-05` |
| hora_inicio | TIME | Hora inicio | `14:00` |
| hora_fin | TIME | Hora fin calculada | `14:45` |
| estado | ENUM | ver estados abajo | `confirmada` |
| calendar_event_id | STRING | ID del evento en GCal | `evt_google_123` |
| fecha_creacion | DATETIME | Cuándo se agendó | `2025-03-02T14:30:00-05:00` |
| fecha_modificacion | DATETIME | Última modificación | `2025-03-02T14:30:00-05:00` |
| notas | STRING | Observaciones | `Cliente prefiere fade` |

**Estados posibles**:
- `pendiente`: Recién creada, esperando confirmación
- `confirmada`: Cliente confirmó por WhatsApp
- `completada`: Servicio realizado
- `cancelada`: Cliente canceló
- `no_asistio`: No show

**Índices**:
- `cliente_telefono` (búsqueda rápida)
- `fecha + hora_inicio` (validación disponibilidad)
- `estado` (filtros)

---

#### Sheet 3: `servicios`
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| id | STRING | Identificador único | `srv_corte_barba` |
| nombre | STRING | Nombre del servicio | `Corte + Barba` |
| precio | INTEGER | Precio en COP | `28000` |
| duracion_minutos | INTEGER | Duración estimada | `45` |
| activo | BOOLEAN | Si está disponible | `TRUE` |
| orden | INTEGER | Orden en menú | `1` |

**Datos iniciales**:
```
srv_corte_barba | Corte + Barba | 28000 | 45 | TRUE | 1
srv_corte_normal | Corte Normal | 20000 | 30 | TRUE | 2
```

---

#### Sheet 4: `disponibilidad`
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| id | STRING | UUID | `disp_lunes_am` |
| dia_semana | INTEGER | 0=Lun, 6=Dom | `0` |
| hora_inicio | TIME | Inicio bloque | `08:00` |
| hora_fin | TIME | Fin bloque | `12:00` |
| activo | BOOLEAN | Si aplica | `TRUE` |

**Datos iniciales** (horario de Churco):
```
disp_lun_am | 0 | 08:00 | 12:00 | TRUE
disp_lun_pm | 0 | 14:00 | 20:00 | TRUE
disp_mar_am | 1 | 08:00 | 12:00 | TRUE
disp_mar_pm | 1 | 14:00 | 20:00 | TRUE
... (repetir para todos los días)
```

---

#### Sheet 5: `sesiones_chat`
| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| telefono | STRING | ID de sesión | `573001234567` |
| estado | STRING | Estado conversacional | `esperando_servicio` |
| datos_temp | JSON | Datos temporales | `{"servicio_id": "srv_corte_barba"}` |
| ultima_actividad | DATETIME | Timestamp | `2025-03-02T14:30:00-05:00` |
| cita_en_proceso | STRING | ID cita temporal | `cita_xyz789` |

**Estados conversacionales**:
- `inicio`: Menú principal
- `esperando_servicio`: Eligiendo servicio
- `esperando_fecha`: Eligiendo fecha
- `esperando_hora`: Eligiendo hora
- `confirmando_cita`: Revisando datos
- `consulta_cita`: Buscando cita existente
- `cancelando_cita`: Proceso de cancelación
- `reagendando_cita`: Proceso de reagendamiento


## 3. Credenciales y Permisos Google

### Service Account Setup

**Email**: `churcobarberstudio@gmail.com`

#### Permisos requeridos en Google Cloud Console:
1. **Google Sheets API** - Habilitada
2. **Google Calendar API** - Habilitada

#### Scopes necesarios:
```python
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',  # Leer/escribir Sheets
    'https://www.googleapis.com/auth/calendar.events'  # Crear/modificar eventos
]
```

#### Archivo de credenciales:
- Descargar JSON desde Google Cloud Console
- Guardar como `service_account.json`
- **NUNCA** commitear a Git
- Agregar a `.gitignore`

#### Compartir recursos:
1. **Google Sheet**: Compartir con `churcobarberstudio@gmail.com` como **Editor**
2. **Google Calendar**: Compartir con `churcobarberstudio@gmail.com` como **Hacer cambios en eventos**

### Variables de Entorno

```env
# Google Sheets
GOOGLE_SHEETS_ID=1XEk1okxlRuTfCYsNXGSrtDXeYq0_S1FT
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json

# Google Calendar
GOOGLE_CALENDAR_ID=churcobarberstudio@gmail.com
TIMEZONE=America/Bogota
```

### Buenas Prácticas
- ✅ Usar Service Account (no OAuth user)
- ✅ Limitar scopes al mínimo necesario
- ✅ Rotar credenciales cada 90 días
- ✅ Monitorear uso de API (quotas)
- ✅ Implementar retry con exponential backoff
- ✅ Cachear lecturas de `servicios` y `disponibilidad`


## 4. Integración Google Calendar

### Estructura del Evento

```python
{
    "summary": "Corte + Barba - Juan Pérez",
    "description": "Cliente: Juan Pérez\nTeléfono: +57 300 123 4567\nServicio: Corte + Barba\nPrecio: $28.000 COP\nID Cita: cita_xyz789",
    "start": {
        "dateTime": "2025-03-05T14:00:00-05:00",
        "timeZone": "America/Bogota"
    },
    "end": {
        "dateTime": "2025-03-05T14:45:00-05:00",
        "timeZone": "America/Bogota"
    },
    "attendees": [
        {"email": "churcobarberstudio@gmail.com"}
    ],
    "reminders": {
        "useDefault": False,
        "overrides": [
            {"method": "popup", "minutes": 60},
            {"method": "popup", "minutes": 15}
        ]
    },
    "colorId": "9",  # Azul para citas confirmadas
    "extendedProperties": {
        "private": {
            "cita_id": "cita_xyz789",
            "cliente_telefono": "573001234567",
            "servicio_id": "srv_corte_barba",
            "precio": "28000"
        }
    }
}
```

### Prevención de Doble Reserva

**Algoritmo**:
1. Antes de crear cita, consultar Calendar API:
   ```python
   events = calendar.events().list(
       calendarId=CALENDAR_ID,
       timeMin=fecha_inicio_iso,
       timeMax=fecha_fin_iso,
       singleEvents=True
   ).execute()
   ```
2. Si `len(events['items']) > 0` → Horario ocupado
3. Validar también en Sheet `citas` (doble verificación)

**Regla**: Un horario está ocupado si existe:
- Evento en Calendar con estado != `cancelled`
- O cita en Sheets con estado `confirmada` o `pendiente`

### Sincronización de Cambios

#### Cancelación:
1. Usuario cancela por WhatsApp
2. Sistema actualiza Sheet: `estado = 'cancelada'`
3. Sistema cancela evento en Calendar:
   ```python
   calendar.events().delete(
       calendarId=CALENDAR_ID,
       eventId=calendar_event_id
   ).execute()
   ```

#### Reagendamiento:
1. Cancelar evento anterior
2. Crear nuevo evento
3. Actualizar Sheet con nuevo `calendar_event_id`

### Colores por Estado
- `9` (Azul): Confirmada
- `11` (Rojo): Cancelada
- `5` (Amarillo): Pendiente confirmación
- `10` (Verde): Completada


## 5. Flujo de Agendamiento (Paso a Paso)

### Flujo Completo: Agendar Cita

```
[INICIO] Usuario: "Hola"
    ↓
[MENÚ] Bot: "Bienvenido a Barbería Churco. ¿Qué deseas hacer?
         1. Agendar cita
         2. Consultar mi cita
         3. Cancelar cita
         4. Reagendar cita"
    ↓
[USUARIO] "1"
    ↓
[VALIDAR_CLIENTE]
    - Buscar en Sheet `clientes` por telefono
    - Si NO existe → Crear registro
    - Guardar sesión: estado = 'esperando_servicio'
    ↓
[MOSTRAR_SERVICIOS] Bot: "Selecciona tu servicio:
                          1. Corte + Barba - $28.000 (45 min)
                          2. Corte Normal - $20.000 (30 min)"
    ↓
[USUARIO] "1"
    ↓
[GUARDAR_SERVICIO]
    - Validar opción (1 o 2)
    - Guardar en sesión: datos_temp = {"servicio_id": "srv_corte_barba"}
    - Actualizar estado = 'esperando_fecha'
    ↓
[CALCULAR_FECHAS_DISPONIBLES]
    - Obtener próximos 7 días
    - Filtrar por disponibilidad (Sheet `disponibilidad`)
    - Excluir fechas pasadas
    ↓
[MOSTRAR_FECHAS] Bot: "¿Qué día prefieres?
                       1. Lunes 03/03
                       2. Martes 04/03
                       3. Miércoles 05/03
                       ..."
    ↓
[USUARIO] "3"
    ↓
[GUARDAR_FECHA]
    - Validar opción
    - Guardar en sesión: datos_temp["fecha"] = "2025-03-05"
    - Actualizar estado = 'esperando_hora'
    ↓
[CALCULAR_HORAS_DISPONIBLES]
    - Obtener bloques de disponibilidad para ese día
    - Consultar citas existentes en Sheet `citas`
    - Consultar eventos en Google Calendar
    - Generar slots libres cada 15 minutos
    - Filtrar slots que permitan duración del servicio
    ↓
[MOSTRAR_HORAS] Bot: "¿A qué hora?
                      1. 08:00 AM
                      2. 08:15 AM
                      3. 08:30 AM
                      ...
                      (Horarios ocupados no se muestran)"
    ↓
[USUARIO] "5" (ejemplo: 09:00 AM)
    ↓
[GUARDAR_HORA]
    - Validar opción
    - Guardar en sesión: datos_temp["hora"] = "09:00"
    - Actualizar estado = 'confirmando_cita'
    ↓
[MOSTRAR_RESUMEN] Bot: "Confirma tu cita:
                        📅 Miércoles 05/03/2025
                        🕐 09:00 AM - 09:45 AM
                        ✂️ Corte + Barba
                        💰 $28.000 COP
                        👨‍💼 Barbero: Churco
                        
                        Responde 'SI' para confirmar o 'NO' para cancelar"
    ↓
[USUARIO] "SI"
    ↓
[CREAR_CITA]
    1. Generar ID único: cita_xyz789
    2. Escribir en Sheet `citas`:
       - Todos los campos
       - estado = 'confirmada'
    3. Crear evento en Google Calendar
    4. Guardar calendar_event_id en Sheet
    5. Actualizar contador en Sheet `clientes`
    6. Limpiar sesión
    ↓
[CONFIRMACIÓN] Bot: "✅ ¡Cita confirmada!
                     
                     📅 Miércoles 05/03/2025
                     🕐 09:00 AM
                     ✂️ Corte + Barba
                     💰 $28.000 COP
                     
                     Te esperamos en Barbería Churco.
                     Recuerda llegar 5 minutos antes.
                     
                     ID de tu cita: cita_xyz789"
    ↓
[FIN]
```

### Validaciones Críticas en Cada Paso

#### 1. Validar Servicio
```python
if opcion not in ['1', '2']:
    return "Opción inválida. Responde 1 o 2."
```

#### 2. Validar Fecha
```python
# Fecha debe ser futura
if fecha_seleccionada < datetime.now().date():
    return "No puedes agendar en el pasado."

# Fecha debe estar en próximos 30 días
if fecha_seleccionada > datetime.now().date() + timedelta(days=30):
    return "Solo puedes agendar hasta 30 días adelante."
```

#### 3. Validar Hora
```python
# Verificar disponibilidad en Sheets
citas_existentes = buscar_citas(fecha, hora_inicio, hora_fin)
if len(citas_existentes) > 0:
    return "Ese horario ya está ocupado."

# Verificar en Google Calendar
eventos = buscar_eventos_calendar(fecha, hora_inicio, hora_fin)
if len(eventos) > 0:
    return "Ese horario ya está ocupado."

# Verificar que esté dentro de horario de atención
if not esta_en_horario_atencion(hora_inicio):
    return "Ese horario está fuera de nuestro horario de atención."
```

#### 4. Validar Confirmación
```python
if respuesta.upper() not in ['SI', 'SÍ', 'YES', 'CONFIRMAR']:
    limpiar_sesion()
    return "Cita cancelada. Escribe 'hola' para empezar de nuevo."
```


## 6. Flujos Adicionales

### Consultar Cita

```
[USUARIO] "2" (desde menú)
    ↓
[BUSCAR_CITAS]
    - Buscar en Sheet `citas` por cliente_telefono
    - Filtrar: estado IN ('confirmada', 'pendiente')
    - Ordenar por fecha ASC
    ↓
[SI NO HAY CITAS]
    Bot: "No tienes citas agendadas."
    ↓ [FIN]
    
[SI HAY 1 CITA]
    Bot: "Tu próxima cita:
          📅 Miércoles 05/03/2025
          🕐 09:00 AM
          ✂️ Corte + Barba
          💰 $28.000 COP
          ID: cita_xyz789"
    ↓ [FIN]
    
[SI HAY MÚLTIPLES]
    Bot: "Tienes 2 citas agendadas:
          
          1. Miércoles 05/03 - 09:00 AM - Corte + Barba
          2. Viernes 07/03 - 14:00 PM - Corte Normal
          
          Responde el número para ver detalles."
    ↓ [MOSTRAR_DETALLE]
```

### Cancelar Cita

```
[USUARIO] "3" (desde menú)
    ↓
[BUSCAR_CITAS_ACTIVAS]
    - Filtrar: estado = 'confirmada'
    - Filtrar: fecha >= hoy
    ↓
[SI NO HAY CITAS]
    Bot: "No tienes citas para cancelar."
    ↓ [FIN]
    
[SI HAY 1 CITA]
    Bot: "¿Deseas cancelar esta cita?
          📅 Miércoles 05/03/2025
          🕐 09:00 AM
          ✂️ Corte + Barba
          
          Responde 'SI' para confirmar."
    ↓
[USUARIO] "SI"
    ↓
[CANCELAR]
    1. Actualizar Sheet: estado = 'cancelada'
    2. Eliminar evento de Google Calendar
    3. Registrar fecha_modificacion
    ↓
    Bot: "✅ Cita cancelada exitosamente.
          Puedes agendar una nueva cuando quieras."
    ↓ [FIN]
    
[SI HAY MÚLTIPLES]
    Bot: "¿Qué cita deseas cancelar?
          1. Miércoles 05/03 - 09:00 AM
          2. Viernes 07/03 - 14:00 PM
          
          Responde el número."
    ↓ [CONFIRMAR_CANCELACIÓN]
```

### Reagendar Cita

```
[USUARIO] "4" (desde menú)
    ↓
[BUSCAR_CITAS_ACTIVAS]
    ↓
[SELECCIONAR_CITA] (si hay múltiples)
    ↓
[CONFIRMAR_REAGENDAMIENTO]
    Bot: "¿Deseas reagendar esta cita?
          Actual: Miércoles 05/03 - 09:00 AM
          
          Responde 'SI' para continuar."
    ↓
[USUARIO] "SI"
    ↓
[FLUJO_AGENDAR] (reutilizar flujo de agendamiento)
    - Mantener servicio_id
    - Pedir nueva fecha
    - Pedir nueva hora
    - Confirmar
    ↓
[ACTUALIZAR_CITA]
    1. Eliminar evento anterior de Calendar
    2. Crear nuevo evento en Calendar
    3. Actualizar Sheet `citas`:
       - fecha, hora_inicio, hora_fin
       - calendar_event_id (nuevo)
       - fecha_modificacion
    ↓
    Bot: "✅ Cita reagendada exitosamente.
          
          Nueva fecha:
          📅 Viernes 07/03/2025
          🕐 14:00 PM
          ✂️ Corte + Barba"
    ↓ [FIN]
```


## 7. Validaciones Críticas del Sistema

### Validación de Disponibilidad (Algoritmo Completo)

```python
def obtener_slots_disponibles(fecha: date, duracion_minutos: int) -> List[time]:
    """
    Retorna lista de horarios disponibles para una fecha y duración.
    """
    # 1. Obtener bloques de disponibilidad del día
    dia_semana = fecha.weekday()  # 0=Lun, 6=Dom
    bloques = sheets.get_disponibilidad(dia_semana)
    # Resultado: [(08:00, 12:00), (14:00, 20:00)]
    
    # 2. Generar slots cada 15 minutos
    slots_posibles = []
    for bloque in bloques:
        hora_actual = bloque.hora_inicio
        while hora_actual + timedelta(minutes=duracion_minutos) <= bloque.hora_fin:
            slots_posibles.append(hora_actual)
            hora_actual += timedelta(minutes=15)
    
    # 3. Filtrar slots ocupados en Sheets
    citas_dia = sheets.get_citas_por_fecha(fecha)
    slots_ocupados_sheets = []
    for cita in citas_dia:
        if cita.estado in ['confirmada', 'pendiente']:
            slots_ocupados_sheets.append((cita.hora_inicio, cita.hora_fin))
    
    # 4. Filtrar slots ocupados en Calendar
    eventos_dia = calendar.get_eventos(fecha)
    slots_ocupados_calendar = []
    for evento in eventos_dia:
        if evento.status != 'cancelled':
            slots_ocupados_calendar.append((evento.start, evento.end))
    
    # 5. Combinar slots ocupados
    slots_ocupados = slots_ocupados_sheets + slots_ocupados_calendar
    
    # 6. Filtrar slots disponibles
    slots_disponibles = []
    for slot in slots_posibles:
        slot_fin = slot + timedelta(minutes=duracion_minutos)
        
        # Verificar que no se solape con ningún slot ocupado
        disponible = True
        for ocupado_inicio, ocupado_fin in slots_ocupados:
            if hay_solapamiento(slot, slot_fin, ocupado_inicio, ocupado_fin):
                disponible = False
                break
        
        if disponible:
            slots_disponibles.append(slot)
    
    return slots_disponibles

def hay_solapamiento(a_inicio, a_fin, b_inicio, b_fin) -> bool:
    """Verifica si dos rangos de tiempo se solapan."""
    return a_inicio < b_fin and b_inicio < a_fin
```

### Validación de Datos de Entrada

```python
# Teléfono
def validar_telefono(telefono: str) -> bool:
    # Debe ser numérico, 10-13 dígitos
    return telefono.isdigit() and 10 <= len(telefono) <= 13

# Nombre
def validar_nombre(nombre: str) -> bool:
    # Mínimo 2 caracteres, solo letras y espacios
    return len(nombre) >= 2 and all(c.isalpha() or c.isspace() for c in nombre)

# Fecha
def validar_fecha(fecha: date) -> bool:
    hoy = datetime.now().date()
    max_fecha = hoy + timedelta(days=30)
    return hoy <= fecha <= max_fecha

# Hora
def validar_hora(hora: time, fecha: date) -> bool:
    # Si es hoy, la hora debe ser futura
    if fecha == datetime.now().date():
        ahora = datetime.now().time()
        return hora > ahora
    return True
```

### Manejo de Concurrencia

**Problema**: Dos usuarios intentan agendar el mismo horario simultáneamente.

**Solución**:
1. Usar `append` atómico de Google Sheets
2. Verificar disponibilidad JUSTO ANTES de escribir
3. Si falla, reintentar con exponential backoff
4. Máximo 3 reintentos

```python
def crear_cita_atomica(datos_cita: dict) -> bool:
    for intento in range(3):
        # Verificar disponibilidad
        if not esta_disponible(datos_cita['fecha'], datos_cita['hora_inicio']):
            return False
        
        try:
            # Intentar escribir
            sheets.append_row('citas', datos_cita)
            calendar.create_event(datos_cita)
            return True
        except Exception as e:
            if intento < 2:
                time.sleep(2 ** intento)  # 1s, 2s, 4s
            else:
                raise
    
    return False
```

### Validación de Integridad

```python
# Verificar que cita en Sheets tenga evento en Calendar
def verificar_integridad_cita(cita_id: str) -> bool:
    cita = sheets.get_cita(cita_id)
    if not cita.calendar_event_id:
        return False
    
    try:
        evento = calendar.get_event(cita.calendar_event_id)
        return evento.status != 'cancelled'
    except:
        return False

# Job diario: Sincronizar Sheets ↔ Calendar
def sincronizar_diario():
    citas = sheets.get_citas_activas()
    for cita in citas:
        if not verificar_integridad_cita(cita.id):
            # Recrear evento o marcar cita como error
            logger.error(f"Cita {cita.id} desincronizada")
```


## 8. Riesgos del MVP y Mitigaciones

### Riesgo 1: Límites de API de Google

**Problema**: 
- Sheets API: 100 requests/100 segundos/usuario
- Calendar API: 1,000,000 queries/día

**Impacto**: Sistema se bloquea en alta concurrencia

**Mitigación**:
```python
# 1. Implementar caché local
cache_servicios = {}  # Cachear servicios (cambian poco)
cache_disponibilidad = {}  # Cachear horarios

# 2. Batch requests cuando sea posible
sheets.batch_get(['clientes!A:F', 'citas!A:N'])

# 3. Exponential backoff en errores 429
@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def sheets_request():
    pass

# 4. Monitorear quotas
if requests_count > 80:
    logger.warning("Cerca del límite de API")
```

---

### Riesgo 2: Desincronización Sheets ↔ Calendar

**Problema**: Cita existe en Sheets pero no en Calendar (o viceversa)

**Impacto**: Doble reserva o citas fantasma

**Mitigación**:
```python
# 1. Transacción lógica
def crear_cita_completa(datos):
    try:
        # Paso 1: Escribir en Sheets
        cita_id = sheets.append_cita(datos)
        
        # Paso 2: Crear evento
        event_id = calendar.create_event(datos)
        
        # Paso 3: Actualizar Sheets con event_id
        sheets.update_cita(cita_id, {'calendar_event_id': event_id})
        
        return True
    except Exception as e:
        # Rollback: eliminar lo que se creó
        if cita_id:
            sheets.delete_cita(cita_id)
        if event_id:
            calendar.delete_event(event_id)
        raise

# 2. Job de reconciliación diario
def reconciliar():
    # Buscar citas sin event_id
    citas_huerfanas = sheets.get_citas_sin_evento()
    for cita in citas_huerfanas:
        # Recrear evento
        event_id = calendar.create_event(cita)
        sheets.update_cita(cita.id, {'calendar_event_id': event_id})
```

---

### Riesgo 3: Sesiones de Chat Perdidas

**Problema**: Usuario abandona conversación a mitad de flujo

**Impacto**: Datos temporales quedan en Sheet `sesiones_chat`

**Mitigación**:
```python
# 1. Timeout de sesión
TIMEOUT_MINUTOS = 15

def limpiar_sesiones_antiguas():
    ahora = datetime.now()
    sesiones = sheets.get_sesiones()
    for sesion in sesiones:
        if (ahora - sesion.ultima_actividad).minutes > TIMEOUT_MINUTOS:
            sheets.delete_sesion(sesion.telefono)

# 2. Ejecutar cada 5 minutos
scheduler.add_job(limpiar_sesiones_antiguas, 'interval', minutes=5)

# 3. Permitir reinicio de flujo
if mensaje.lower() in ['menu', 'inicio', 'hola', 'cancelar']:
    sheets.delete_sesion(telefono)
    return mostrar_menu()
```

---

### Riesgo 4: Zona Horaria Incorrecta

**Problema**: Eventos se crean en UTC en vez de America/Bogota

**Impacto**: Citas con hora incorrecta

**Mitigación**:
```python
import pytz

TIMEZONE = pytz.timezone('America/Bogota')

def crear_datetime_local(fecha: date, hora: time) -> datetime:
    """Crea datetime con timezone correcto."""
    dt = datetime.combine(fecha, hora)
    return TIMEZONE.localize(dt)

# Siempre usar en Calendar API
evento = {
    "start": {
        "dateTime": dt_inicio.isoformat(),
        "timeZone": "America/Bogota"
    }
}
```

---

### Riesgo 5: Datos Corruptos en Sheets

**Problema**: Usuario edita manualmente el Sheet y rompe formato

**Impacto**: Sistema falla al leer datos

**Mitigación**:
```python
# 1. Validación estricta al leer
def parse_cita(row: list) -> Cita:
    try:
        return Cita(
            id=row[0],
            cliente_id=row[1],
            # ... validar cada campo
        )
    except (IndexError, ValueError) as e:
        logger.error(f"Fila corrupta: {row}")
        return None

# 2. Proteger rangos críticos
# En Google Sheets: Proteger columnas de ID (solo lectura)

# 3. Backup diario
def backup_sheets():
    # Copiar Sheet completo a otro archivo
    sheets.copy_to(backup_sheet_id)

scheduler.add_job(backup_sheets, 'cron', hour=3)
```

---

### Riesgo 6: WhatsApp Desconectado

**Problema**: Evolution API pierde conexión con WhatsApp

**Impacto**: Mensajes no se envían/reciben

**Mitigación**:
```python
# 1. Health check cada 5 minutos
def verificar_whatsapp():
    status = evolution_api.get_instance_status()
    if status != 'open':
        logger.critical("WhatsApp desconectado")
        # Enviar alerta por email/SMS
        send_alert("WhatsApp desconectado")

# 2. Reintentar envío de mensajes
@retry(stop=stop_after_attempt(3))
def enviar_mensaje(telefono, texto):
    return evolution_api.send_message(telefono, texto)

# 3. Cola de mensajes pendientes
# Si falla, guardar en Sheet `mensajes_pendientes`
# Reenviar cuando se reconecte
```


## 9. Recomendaciones para Escalar

### Fase 2: Múltiples Barberos

**Cambios necesarios**:

1. **Sheet `barberos`**:
```
id | nombre | activo | color_calendar
barb_churco | Churco | TRUE | 9
barb_juan | Juan | TRUE | 10
```

2. **Modificar Sheet `citas`**:
```
+ barbero_id | STRING | FK a barberos.id
+ barbero_nombre | STRING | Denormalizado
```

3. **Modificar Sheet `disponibilidad`**:
```
+ barbero_id | STRING | Horarios por barbero
```

4. **Flujo de agendamiento**:
```
[DESPUÉS DE SERVICIO]
    ↓
[SELECCIONAR_BARBERO]
    Bot: "¿Con quién prefieres tu cita?
          1. Churco
          2. Juan"
    ↓
[CALCULAR_DISPONIBILIDAD] (filtrar por barbero_id)
```

---

### Fase 3: Notificaciones Automáticas

**Implementar**:

```python
# 1. Recordatorio 24h antes
def enviar_recordatorios():
    manana = datetime.now() + timedelta(days=1)
    citas = sheets.get_citas_por_fecha(manana.date())
    
    for cita in citas:
        if cita.estado == 'confirmada':
            mensaje = f"""
            🔔 Recordatorio de cita
            
            Mañana {cita.fecha.strftime('%d/%m')} a las {cita.hora_inicio}
            Servicio: {cita.servicio_nombre}
            Barbero: Churco
            
            Te esperamos en Barbería Churco.
            """
            whatsapp.send_message(cita.cliente_telefono, mensaje)

# Ejecutar diariamente a las 10 AM
scheduler.add_job(enviar_recordatorios, 'cron', hour=10)

# 2. Confirmación 2h antes
def solicitar_confirmacion():
    en_2h = datetime.now() + timedelta(hours=2)
    citas = sheets.get_citas_proximas(en_2h)
    
    for cita in citas:
        mensaje = f"""
        Tu cita es en 2 horas ({cita.hora_inicio}).
        
        Responde 'CONFIRMO' si asistirás o 'CANCELAR' si no puedes.
        """
        whatsapp.send_message(cita.cliente_telefono, mensaje)

# Ejecutar cada hora
scheduler.add_job(solicitar_confirmacion, 'interval', hours=1)
```

---

### Fase 4: Analytics y Reportes

**Sheet adicional: `metricas`**

```python
def calcular_metricas_diarias():
    hoy = datetime.now().date()
    
    metricas = {
        'fecha': hoy,
        'citas_agendadas': sheets.count_citas(hoy, 'confirmada'),
        'citas_completadas': sheets.count_citas(hoy, 'completada'),
        'citas_canceladas': sheets.count_citas(hoy, 'cancelada'),
        'no_shows': sheets.count_citas(hoy, 'no_asistio'),
        'ingresos': sheets.sum_ingresos(hoy),
        'clientes_nuevos': sheets.count_clientes_nuevos(hoy),
        'tasa_ocupacion': calcular_ocupacion(hoy)
    }
    
    sheets.append_row('metricas', metricas)

# Ejecutar a medianoche
scheduler.add_job(calcular_metricas_diarias, 'cron', hour=0, minute=5)
```

**Dashboard en Google Sheets**:
- Gráficos de ocupación semanal
- Ingresos mensuales
- Servicios más solicitados
- Horarios más populares

---

### Fase 5: Pagos Online

**Integración con Wompi/PayU**:

1. **Modificar Sheet `citas`**:
```
+ pago_estado | ENUM | pendiente, pagado, reembolsado
+ pago_referencia | STRING | ID de transacción
+ pago_metodo | STRING | efectivo, tarjeta, nequi
```

2. **Flujo**:
```
[DESPUÉS DE CONFIRMAR CITA]
    ↓
[OFRECER_PAGO]
    Bot: "¿Cómo deseas pagar?
          1. Efectivo en barbería
          2. Pagar ahora con tarjeta (10% descuento)"
    ↓
[SI ELIGE TARJETA]
    - Generar link de pago Wompi
    - Enviar por WhatsApp
    - Webhook de Wompi actualiza Sheet
```

---

### Fase 6: Programa de Fidelidad

**Sheet adicional: `puntos`**

```
cliente_id | puntos_acumulados | nivel | descuento_actual
cli_abc123 | 150 | oro | 15%
```

**Reglas**:
- 10 puntos por cada $1.000 gastado
- Niveles: Bronce (0-100), Plata (101-300), Oro (301+)
- Descuentos: 5%, 10%, 15%

```python
def aplicar_puntos(cita):
    puntos = cita.precio // 1000 * 10
    sheets.add_puntos(cita.cliente_id, puntos)
    
    nivel = sheets.get_nivel_cliente(cita.cliente_id)
    
    mensaje = f"""
    ✅ Cita completada
    
    Ganaste {puntos} puntos
    Nivel actual: {nivel}
    Total puntos: {sheets.get_puntos(cita.cliente_id)}
    """
    whatsapp.send_message(cita.cliente_telefono, mensaje)
```

---

### Fase 7: Migración a Base de Datos Real

**Cuándo migrar**:
- Más de 1000 citas/mes
- Más de 3 barberos
- Necesidad de queries complejas
- Problemas de performance

**Opciones**:
1. **Supabase** (PostgreSQL + API REST)
2. **Firebase Firestore** (NoSQL)
3. **MongoDB Atlas** (NoSQL)

**Ventajas**:
- Queries más rápidas
- Transacciones ACID
- Índices optimizados
- Webhooks nativos

**Mantener Google Calendar** para visualización del barbero.


## 10. Estructura de Archivos del Proyecto

```
barberia-churco/
├── .env                          # Credenciales (NO commitear)
├── .env.example                  # Plantilla
├── .gitignore
├── requirements.txt
├── service_account.json          # Credenciales Google (NO commitear)
│
├── main.py                       # Entry point
├── server.py                     # FastAPI server
│
├── config/
│   ├── __init__.py
│   ├── settings.py               # Variables de entorno
│   └── constants.py              # Constantes (horarios, precios)
│
├── services/
│   ├── __init__.py
│   ├── google_sheets.py          # Cliente Google Sheets
│   ├── google_calendar.py        # Cliente Google Calendar
│   ├── evolution_api.py          # Cliente Evolution API
│   └── whatsapp.py               # Wrapper de mensajería
│
├── models/
│   ├── __init__.py
│   ├── cliente.py                # Dataclass Cliente
│   ├── cita.py                   # Dataclass Cita
│   ├── servicio.py               # Dataclass Servicio
│   └── sesion.py                 # Dataclass Sesión
│
├── chatbot/
│   ├── __init__.py
│   ├── engine.py                 # Motor del chatbot
│   ├── estados.py                # Máquina de estados
│   ├── validaciones.py           # Validadores
│   └── mensajes.py               # Templates de mensajes
│
├── utils/
│   ├── __init__.py
│   ├── datetime_utils.py         # Helpers de fecha/hora
│   ├── disponibilidad.py         # Cálculo de slots
│   └── formatters.py             # Formateo de mensajes
│
├── jobs/
│   ├── __init__.py
│   ├── scheduler.py              # APScheduler config
│   ├── recordatorios.py          # Job de recordatorios
│   ├── limpieza.py               # Job de limpieza
│   └── sincronizacion.py         # Job de sync Sheets↔Calendar
│
└── tests/
    ├── __init__.py
    ├── test_sheets.py
    ├── test_calendar.py
    ├── test_chatbot.py
    └── test_disponibilidad.py
```

---

## 11. Dependencias Principales

```txt
# requirements.txt

# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0

# Google APIs
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.116.0
gspread==5.12.0

# WhatsApp
requests==2.31.0
httpx==0.26.0

# Utilidades
python-dotenv==1.0.0
pytz==2024.1
python-dateutil==2.8.2

# Jobs
APScheduler==3.10.4

# Logging
loguru==0.7.2

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
```

---

## 12. Configuración Inicial (Checklist)

### Google Cloud Console

- [ ] Crear proyecto: `barberia-churco`
- [ ] Habilitar Google Sheets API
- [ ] Habilitar Google Calendar API
- [ ] Crear Service Account
- [ ] Descargar JSON de credenciales
- [ ] Copiar email del Service Account

### Google Sheets

- [ ] Crear archivo: `Barberia_Churco_DB`
- [ ] Crear 5 sheets: `clientes`, `citas`, `servicios`, `disponibilidad`, `sesiones_chat`
- [ ] Configurar headers según modelo de datos
- [ ] Compartir con Service Account (Editor)
- [ ] Copiar ID del archivo (desde URL)

### Google Calendar

- [ ] Usar calendario principal de `churcobarberstudio@gmail.com`
- [ ] Compartir con Service Account (Hacer cambios en eventos)
- [ ] Configurar zona horaria: America/Bogota

### Evolution API

- [ ] Instancia activa y conectada
- [ ] Webhook configurado apuntando a tu servidor
- [ ] API Key guardada en `.env`

### Servidor

- [ ] Clonar repositorio
- [ ] Crear `.env` desde `.env.example`
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Colocar `service_account.json` en raíz
- [ ] Ejecutar tests: `pytest`
- [ ] Iniciar servidor: `python server.py`

---

## 13. Comandos de Desarrollo

```bash
# Iniciar servidor en desarrollo
python server.py

# Ejecutar tests
pytest -v

# Verificar conexión a Google Sheets
python -c "from services.google_sheets import SheetsClient; client = SheetsClient(); print(client.test_connection())"

# Verificar conexión a Google Calendar
python -c "from services.google_calendar import CalendarClient; client = CalendarClient(); print(client.test_connection())"

# Limpiar sesiones antiguas manualmente
python -c "from jobs.limpieza import limpiar_sesiones; limpiar_sesiones()"

# Sincronizar Sheets ↔ Calendar
python -c "from jobs.sincronizacion import sincronizar; sincronizar()"

# Poblar datos iniciales
python scripts/seed_data.py
```

---

## 14. Monitoreo y Logs

```python
# config/logging.py
from loguru import logger

logger.add(
    "logs/barberia_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Logs críticos
logger.info("Cita creada: {cita_id}", cita_id=cita.id)
logger.warning("Horario casi lleno: {fecha}", fecha=fecha)
logger.error("Error al crear evento en Calendar: {error}", error=str(e))
logger.critical("WhatsApp desconectado")
```

**Métricas a monitorear**:
- Requests/minuto a Google APIs
- Tiempo de respuesta del chatbot
- Tasa de conversión (mensajes → citas)
- Tasa de cancelación
- Errores de sincronización

---

## 15. Resumen Ejecutivo

### ✅ Decisiones Técnicas Clave

1. **Google Sheets como DB**: Simple, visual, sin infraestructura
2. **5 Sheets**: Normalización básica pero eficiente
3. **Denormalización estratégica**: `cliente_nombre` en `citas` para búsquedas rápidas
4. **Service Account**: Autenticación sin intervención humana
5. **Doble verificación**: Sheets + Calendar para prevenir doble reserva
6. **Slots de 15 min**: Balance entre flexibilidad y simplicidad
7. **Estados conversacionales**: Máquina de estados clara y mantenible
8. **Jobs programados**: Limpieza, recordatorios, sincronización
9. **Timezone explícito**: America/Bogota en todo el sistema
10. **Caché selectivo**: Servicios y disponibilidad (datos estáticos)

### 🎯 MVP Funcional en 1 Semana

**Día 1-2**: Setup + Google APIs + Modelo de datos
**Día 3-4**: Chatbot + Flujo de agendamiento
**Día 5**: Integración Calendar + Validaciones
**Día 6**: Testing + Ajustes
**Día 7**: Deploy + Monitoreo

### 📊 Capacidad del MVP

- **Citas/día**: ~50 (con 1 barbero, 12h atención)
- **Usuarios concurrentes**: ~10 (límite de API)
- **Citas/mes**: ~1500
- **Escalable hasta**: 3 barberos, 5000 citas/mes

### 🚀 Próximos Pasos

1. Revisar y aprobar esta arquitectura
2. Crear Google Sheet con estructura definida
3. Configurar Service Account
4. Implementar `google_sheets.py` y `google_calendar.py`
5. Implementar chatbot engine
6. Testing exhaustivo
7. Deploy

---

**¿Listo para implementar?** 🚀
