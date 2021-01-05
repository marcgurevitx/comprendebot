from sanic.response import html

from adminsite.config import config


async def index(request):
    template = config.jinja_environment.get_template("index.html")
    text = template.render()
    return html(text)
