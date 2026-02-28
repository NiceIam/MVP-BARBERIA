# 📊 Diagrama de Flujos del Chatbot de Barbería

## 🎯 Flujos Principales Implementados

### 1. FLUJO DE RESERVA DE CITA
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 1: Reservar)
SELECCIONAR SERVICIO
  ↓
SELECCIONAR BARBERO
  ↓
SELECCIONAR FECHA
  ↓
SELECCIONAR HORA
  ↓
INGRESAR DATOS (Nombre + Teléfono)
  ↓
CONFIRMACIÓN DE CITA
  ↓
MENÚ PRINCIPAL
```

**Puntos clave:**
- 7 servicios disponibles (cortes, barba, diseños, tratamientos)
- 4 opciones de barberos (3 específicos + cualquiera disponible)
- Horarios dinámicos según día de la semana
- Validación de datos del cliente
- Generación de ID único por cita

---

### 2. FLUJO DE CONSULTA DE CITA
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 2: Consultar)
SOLICITAR IDENTIFICACIÓN
  ↓
BUSCAR CITA (por nombre o teléfono)
  ↓
MOSTRAR DETALLES DE CITA
  ↓
MENÚ PRINCIPAL
```

**Puntos clave:**
- Búsqueda por nombre o teléfono
- Muestra todas las citas del cliente
- Información completa: servicio, barbero, fecha, hora, precio

---

### 3. FLUJO DE CANCELACIÓN DE CITA
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 3: Cancelar)
SOLICITAR IDENTIFICACIÓN
  ↓
BUSCAR CITA (por nombre o teléfono)
  ↓
CANCELAR CITA(S)
  ↓
CONFIRMACIÓN DE CANCELACIÓN
  ↓
MENÚ PRINCIPAL
```

**Puntos clave:**
- Búsqueda por nombre o teléfono
- Cancela todas las citas del cliente
- Mensaje de confirmación

---

### 4. FLUJO DE CONSULTA DE SERVICIOS
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 4: Ver servicios)
MOSTRAR SERVICIOS Y PRECIOS
  ↓
OPCIONES:
  - Reservar cita → FLUJO DE RESERVA
  - Volver al menú → MENÚ PRINCIPAL
```

**Servicios incluidos:**
1. Corte de Cabello - $15,000 (30 min)
2. Corte + Barba - $25,000 (45 min)
3. Barba - $12,000 (20 min)
4. Corte Niño - $12,000 (25 min)
5. Diseño/Degradado - $20,000 (40 min)
6. Afeitado Clásico - $18,000 (35 min)
7. Tratamiento Capilar - $30,000 (50 min)

---

### 5. FLUJO DE CONSULTA DE PROMOCIONES
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 5: Ver promociones)
MOSTRAR PROMOCIONES ACTIVAS
  ↓
OPCIONES:
  - Reservar cita → FLUJO DE RESERVA
  - Volver al menú → MENÚ PRINCIPAL
```

**Promociones incluidas:**
- Lunes y Martes: 15% descuento
- Combo Padre e Hijo: 2x1 domingos
- Tarjeta de fidelidad: 5+1 gratis
- Cumpleaños: 20% descuento

---

### 6. FLUJO DE CONSULTA DE BARBEROS
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 6: Ver barberos)
MOSTRAR EQUIPO DE BARBEROS
  ↓
OPCIONES:
  - Reservar cita → FLUJO DE RESERVA
  - Volver al menú → MENÚ PRINCIPAL
```

**Barberos incluidos:**
1. Carlos - Especialista en cortes modernos
2. Miguel - Especialista en barbas y afeitados
3. Juan - Especialista en diseños y degradados

---

### 7. FLUJO DE INFORMACIÓN DE CONTACTO
```
INICIO
  ↓
MENÚ PRINCIPAL
  ↓ (Opción 7: Contacto)
MOSTRAR INFORMACIÓN DE CONTACTO
  ↓
OPCIONES:
  - Reservar cita → FLUJO DE RESERVA
  - Volver al menú → MENÚ PRINCIPAL
```

**Información incluida:**
- Dirección física
- Teléfono de contacto
- Horarios de atención
- Redes sociales

---

## 🔄 Flujos Secundarios

### RECONOCIMIENTO DE INTENCIONES
El chatbot reconoce lenguaje natural:
- "quiero un corte" → Inicia reserva
- "cuánto cuesta" → Muestra servicios
- "dónde están ubicados" → Muestra contacto
- "hay ofertas" → Muestra promociones

### NAVEGACIÓN
- Comando "menu" → Vuelve al menú principal desde cualquier estado
- Comando "salir" → Termina la conversación
- Validación de entradas en cada paso

---

## 🎨 Estados del Chatbot

```python
INICIO              # Mensaje de bienvenida
MENU_PRINCIPAL      # Menú con 7 opciones
SELECCIONAR_SERVICIO    # Lista de servicios
SELECCIONAR_BARBERO     # Lista de barberos
SELECCIONAR_FECHA       # Fechas disponibles (7 días)
SELECCIONAR_HORA        # Horas según día
CONFIRMAR_DATOS         # Captura nombre y teléfono
CONSULTAR_CITA          # Búsqueda de citas
CANCELAR_CITA           # Cancelación de citas
VER_SERVICIOS           # Catálogo de servicios
VER_PROMOCIONES         # Ofertas actuales
VER_BARBEROS            # Equipo de trabajo
CONTACTO                # Información de contacto
```

---

## 💡 Características Especiales

### Validaciones
- ✅ Formato de teléfono (solo números)
- ✅ Selección de opciones válidas
- ✅ Disponibilidad de horarios
- ✅ Datos completos del cliente

### Experiencia de Usuario
- 🎯 Respuestas contextuales
- 🔄 Navegación flexible
- 📱 Formato amigable con emojis
- ⚡ Flujo rápido y eficiente

### Escalabilidad
- 📊 Estructura modular
- 🔌 Fácil integración con BD
- 🌐 Preparado para WhatsApp/Telegram
- 📈 Métricas y seguimiento
