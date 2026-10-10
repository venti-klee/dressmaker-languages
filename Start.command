#!/bin/zsh
set -eu
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export ARGOS_PACKAGES_DIR="$SCRIPT_DIR/models"
export ARGOS_DEVICE_TYPE=cpu
if [[ -x "$SCRIPT_DIR/.venv/bin/python3" ]]; then
  PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_EXEC="$(command -v python3)"
else
  print "Python 3.9 or later is required. Install Python, then reopen the assistant."
  read -r "REPLY?Press Enter to close."
  exit 1
fi
exec "$PYTHON_EXEC" "$SCRIPT_DIR/assistant/server.py" "$@"
