import sys
import ssl
import toxic_bot_config_parser as config_parser

from aiohttp import web

if len(sys.argv) < 2:
    raise Exception('Не указан путь до кофигурационного файла')

app = web.Application()
config = config_parser.get_config(sys.argv[1])


async def handle(request):
    if not request.match_info.get('token') == config.get_property('token', 1):
        return web.Response(status=403)

    # TODO
    json = await request.json()
    return web.Response()


app.router.add_post('/{token}/', handle)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
cert_path = config.get_property('certificate.path', 1)
private_key_path = config.get_property('private.key.path', 1)
# ssl_context.load_cert_chain(cert_path, private_key_path)

web.run_app(
    app=app,
    host=config.get_property('server.host'),
    port=config.get_int('server.port'),
    ssl_context=ssl_context
)
