#!/bin/bash

set -e

echo "🧪 Configurando contexto Replicate..."
source config/replicate-context.sh

echo "📥 Extrayendo dashboard de Replicate..."
grr pull -d dashboards/replicate

echo "🔄 Ejecutando sincronización de panel modificado..."
python3 sync_manual_panel.py

echo "📤 Aplicando cambios en dashboard de Replicate..."
grr apply dashboards/replicate

echo "✅ Sincronización completada con éxito."