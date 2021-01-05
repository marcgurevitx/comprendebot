FROM ubuntu

RUN apt update && apt install -y \
    netcat-openbsd \
    postgresql-client

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY extlibs/vishnubob-wait-for-it extlibs/vishnubob-wait-for-it
COPY pgmigrations pgmigrations

CMD ["bash", "pgmigrations/migrate.sh"]
