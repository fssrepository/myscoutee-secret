#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOKEN_FILE="$ROOT/.local/sandbox/root-token"
PROJECT=myscoutee-secret-sandbox

compose() {
  docker compose --project-directory "$ROOT" -f "$ROOT/compose.yaml" -p "$PROJECT" "$@"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

case "${1:-}" in
  start)
    require_command docker
    require_command python3
    require_command curl
    umask 077
    mkdir -p "$(dirname "$TOKEN_FILE")"
    if [[ ! -s "$TOKEN_FILE" ]]; then
      python3 -c 'import secrets; print(secrets.token_hex(24))' > "$TOKEN_FILE"
    fi
    chmod 600 "$TOKEN_FILE"
    BAO_DEV_ROOT_TOKEN_ID="$(cat "$TOKEN_FILE")" compose up -d
    for _ in {1..30}; do
      if curl --silent --fail --output /dev/null http://127.0.0.1:8200/v1/sys/health; then
        echo "OpenBao sandbox is ready: http://127.0.0.1:8200/ui/"
        echo "Show the sandbox login token with: ./scripts/lab.sh token"
        exit 0
      fi
      sleep 1
    done
    echo "Sandbox did not become healthy; inspect: ./scripts/lab.sh status" >&2
    exit 1
    ;;
  smoke)
    require_command docker
    require_command python3
    [[ -s "$TOKEN_FILE" ]] || { echo "Start the sandbox first." >&2; exit 1; }
    if [[ "$(BAO_DEV_ROOT_TOKEN_ID="$(cat "$TOKEN_FILE")" compose ps --status running --services)" != "openbao" ]]; then
      echo "The owned OpenBao sandbox is not running." >&2
      exit 1
    fi
    python3 "$ROOT/scripts/smoke.py" "$TOKEN_FILE"
    ;;
  status)
    require_command docker
    [[ -s "$TOKEN_FILE" ]] || { echo "Sandbox has not been started."; exit 0; }
    BAO_DEV_ROOT_TOKEN_ID="$(cat "$TOKEN_FILE")" compose ps
    ;;
  token)
    [[ -s "$TOKEN_FILE" ]] || { echo "Start the sandbox first." >&2; exit 1; }
    cat "$TOKEN_FILE"
    ;;
  stop)
    require_command docker
    [[ -s "$TOKEN_FILE" ]] || { echo "Sandbox has not been started."; exit 0; }
    BAO_DEV_ROOT_TOKEN_ID="$(cat "$TOKEN_FILE")" compose down
    echo "Sandbox stopped. In-memory sample data was discarded."
    ;;
  *)
    echo "Usage: ./scripts/lab.sh {start|smoke|status|token|stop}" >&2
    exit 2
    ;;
esac
