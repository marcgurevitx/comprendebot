
set -e

export PGPASSWORD=$POSTGRES_PASSWORD

$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $POSTGRES_HOST:$POSTGRES_PORT

for s in $CMPDBOT_DIR/pgmigrations/sql/*
do
    psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_DB -f $s
done

echo Migrations maybe applied.
