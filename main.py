import toxic_bot as bot


def handle(request):
    bot.process(request.get_json())
