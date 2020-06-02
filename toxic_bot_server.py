import sys
import ssl
import toxic_bot_config_parser as config_parser

from aiohttp import web

config_path = 'app.yml'
if len(sys.argv) > 1:
    config_path = sys.argv[1]

app = web.Application()
try:
    config = config_parser.get_config(config_path)
except FileNotFoundError:
    raise Exception('Не удалось найти конфигурационный файл. Укажите путь в аргуметах командной строки или создайте '
                    'app.yml в директории с основным модулем.')


async def handle(request):
    if not request.match_info.get('token') == config.get_property('token'):
        return web.Response(status=403)

    # TODO
    json = await request.json()
    return web.Response()


app.router.add_post('/{token}/', handle)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
cert_path = config.get_property('certificate.path')
private_key_path = config.get_property('private.key.path')
# ssl_context.load_cert_chain(cert_path, private_key_path)

if __name__ == '__main__':
    web.run_app(
        app=app,
        host=config.get_property('server.host'),
        port=config.get_int('server.port'),
        ssl_context=None
    )
