import os
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic import Sanic

from adminsite.config import config
from adminsite.handlers import index

if config.PGMIGRATIONS_SYNC:
    os.system("$CMPDBOT_DIR/extlibs/vishnubob-wait-for-it/wait-for-it.sh -s $PGMIGRATIONS_HOST:$PGMIGRATIONS_PORT")

config.jinja_environment = Environment(
    loader=FileSystemLoader(pathlib.Path(config.CMPDBOT_DIR, "templates/adminsite")),
    autoescape=select_autoescape(["html", "xml"]),
)

app = Sanic("adminsite")
app.add_route(index, "/")

app.run(host=config.ADMINSITE_BIND, port=config.ADMINSITE_PORT)
