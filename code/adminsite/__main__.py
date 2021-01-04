from sanic import Sanic

from adminsite.config import config
from adminsite.handlers import index

app = Sanic("adminsite")
app.add_route(index, "/")

app.run(host=config.ADMINSITE_BIND, port=config.ADMINSITE_PORT)
