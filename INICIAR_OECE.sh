#!/usr/bin/env bash
# Inicia OECE Assistant en Ubuntu/Linux. Sin rutas fijas ni PowerShell.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ -n "${OECE_PYTHON:-}" ]]; then
    PYTHON="${OECE_PYTHON}"
elif [[ -x ".venv/bin/python" ]]; then
    PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
else
    echo "Se requiere Python >= 3.12." >&2
    exit 1
fi
"${PYTHON}" -c 'import sys; assert sys.version_info >= (3,12), "Se requiere Python >= 3.12"'
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1
exec "${PYTHON}" -m oece panel --host "${OECE_HOST:-127.0.0.1}" --port "${OECE_PORT:-8765}" "$@"
