FROM ubuntu

RUN apt update && apt install -y postgresql-client

WORKDIR /cmpdbot

COPY extlibs/vishnubob-wait-for-it/wait-for-it.sh code/

COPY pgmigrations/migrate.sh code/

COPY pgmigrations/sql sql/

CMD ["bash", "code/migrate.sh"]
