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
  print "此助手需要 Python 3.9 或更新版本。请先安装 Python，再重新打开。"
  read -r "REPLY?按回车关闭。"
  exit 1
fi
exec "$PYTHON_EXEC" "$SCRIPT_DIR/assistant/server.py" "$@"
