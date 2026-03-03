# 🔐 Configuración Inicial

## Antes de Empezar

Este proyecto requiere configurar credenciales sensibles. Sigue estos pasos:

### 1. Crear archivo .env

```bash
cp .env.example .env
```

### 2. Editar .env con tus credenciales

Abre el archivo `.env` y configura:

```env
# Database Configuration
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_bd?sslmode=disable

# Evolution API Configuration
EVOLUTION_API_URL=https://tu-evolution-api.com/
EVOLUTION_API_KEY=tu_api_key_aqui
EVOLUTION_INSTANCE_NAME=NombreDeTuInstancia

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Verificar que .env esté en .gitignore

El archivo `.env` NO debe subirse a Git. Verifica que esté en `.gitignore`:

```bash
cat .gitignore | grep .env
```

Deberías ver:
```
.env
.env.local
.env.production
.env.*
```

## 🚀 Continuar con la Instalación

Una vez configurado el `.env`, sigue con:

1. [GUIA_INSTALACION.md](GUIA_INSTALACION.md) - Instalación completa
2. [README.md](README.md) - Documentación general

## ⚠️ Importante

- NUNCA compartas tu archivo `.env`
- NUNCA subas `.env` a Git
- Usa `.env.example` como plantilla para otros desarrolladores
