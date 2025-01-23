#!/bin/bash
set -e

# Ждем, пока InfluxDB будет доступен
until curl -s http://localhost:8086/ping; do
    echo "Waiting for InfluxDB to be available..."
    sleep 5
done

# Создаем базу данных
influx -execute "CREATE DATABASE nt_test_db"
