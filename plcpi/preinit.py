
from plc.network.auto import AutoClient

import asyncio


def autoconf(conf):
    loop = asyncio.get_event_loop()
    auto = AutoClient()
    conf["server"] = loop.run_until_complete(auto.get_server)
    conf.save()

def wifi():
    pass
