FROM ubuntu

RUN apt update && apt install -y postgresql-client

COPY extlibs/vishnubob-wait-for-it/wait-for-it.sh /bot/code/

COPY pgmigrations/migrate.sh /bot/code/

COPY pgmigrations/sql /bot/sql/

CMD ["bash", "/bot/code/migrate.sh"]
