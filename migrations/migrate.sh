
set -e

export PGPASSWORD=$POSTGRES_PASSWORD

$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $POSTGRES_HOST:$POSTGRES_PORT

cat $CMPDBOT_DIR/migrations/sql/* | psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_DB -f -

echo Migrations maybe applied.

if [[ 1 -eq $MIGRATIONS_SYNC ]] ; then
    nc -lk $MIGRATIONS_PORT
fi
