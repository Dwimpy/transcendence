#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER andrei;
	CREATE DATABASE hello;
	GRANT ALL PRIVILEGES ON DATABASE hello TO andrei;
EOSQL