#!/usr/bin/env bash
# build.sh para Render con Django y Neon PostgreSQL

set -o errexit

echo "🚀 Iniciando proceso de build..."

# Crear directorios necesarios
mkdir -p logs
mkdir -p staticfiles

echo "📦 Actualizando pip..."
python -m pip install --upgrade pip

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗃️ Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completado exitosamente"
echo "📊 Resumen:"
echo "   - Proyecto: control_escolar_desit_api"
echo "   - Base de datos: PostgreSQL (Neon)"
echo "   - Servidor: Gunicorn"
echo "   - Archivos estáticos: WhiteNoise"
