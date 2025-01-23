#!/bin/bash
set -e

# Путь к pg_hba.conf
PG_HBA_FILE="/var/lib/postgresql/data/pg_hba.conf"

# Заменяем строку для IPv4
#sed -i "s/^host\s\+all\s\+all\s\+127\.0\.0\.1\/32\s\+trust/host all all 0.0.0.0\/0 md5/" $PG_HBA_FILE
echo "host    all             all             0.0.0.0/0               md5" >> $PG_HBA_FILE

# Перезагружаем конфигурацию PostgreSQL
pg_ctl reload -D /var/lib/postgresql/data