#!/bin/bash

# Script de ejecución rápida para solucionar el error y arrancar el chatbot

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║       💈 CHATBOT BARBERÍA - INICIO RÁPIDO 💈            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar que Python esté instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado"
    exit 1
fi

echo "✅ Python encontrado"
echo ""

# Paso 1: Verificar base de datos
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 1: Verificando base de datos..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python check_database.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 2: ¿Deseas resetear la base de datos?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  ADVERTENCIA: Esto eliminará todos los datos existentes"
echo ""
echo "Opciones:"
echo "  1) Sí, resetear base de datos (recomendado si hay errores)"
echo "  2) No, continuar sin resetear"
echo ""
read -p "Selecciona una opción (1 o 2): " opcion

if [ "$opcion" = "1" ]; then
    echo ""
    echo "Reseteando base de datos..."
    python reset_database.py
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 3: Iniciando servidor..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python start.py
