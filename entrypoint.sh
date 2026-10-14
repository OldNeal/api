#!/bin/sh
set -e

# Том монтируется от root — вернём владельца
if [ -d /app/logs ]; then
    chown -R apiuser:apiuser /app/logs
fi

exec gosu apiuser "$@"