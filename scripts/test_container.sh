#!/bin/bash
set -e

echo "Проверка контейнера..."

if ! docker compose ps | grep -q "Up"; then
    echo "Контейнер не запущен"
    exit 1
fi

echo "Ожидание healthcheck..."
sleep 10

if [ "$(docker compose ps --format json | jq -r '.[] | select(.Service=="suggestion-box") | .Health')" != "healthy" ]; then
    echo "Healthcheck не пройден"
    exit 1
fi

USER_ID=$(docker compose exec -T suggestion-box id -u)
if [ "$USER_ID" != "1000" ]; then
    echo "Контейнер запущен под root"
    exit 1
fi

echo "Все проверки пройдены"
