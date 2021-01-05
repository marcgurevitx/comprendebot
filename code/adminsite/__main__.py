import os

from sanic import Sanic

from adminsite.config import config
from adminsite.handlers import index

if config.PGMIGRATIONS_SYNC:
    os.system("$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $PGMIGRATIONS_HOST:$PGMIGRATIONS_PORT")

app = Sanic("adminsite")
app.add_route(index, "/")

app.run(host=config.ADMINSITE_BIND, port=config.ADMINSITE_PORT)
