
set -e

export PGPASSWORD=$POSTGRES_PASSWORD

/cmpdbot/code/wait-for-it.sh -s $POSTGRES_HOST:$POSTGRES_PORT

for s in /cmpdbot/sql/*
do
    psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_DB -f $s
done

echo Migrations maybe applied.
