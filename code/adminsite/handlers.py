from sanic.response import html


async def index(request):
    return html("<h1>Bonk.</h1>")
