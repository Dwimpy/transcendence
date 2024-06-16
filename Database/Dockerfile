FROM postgres:16-bullseye

COPY init-user-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh
