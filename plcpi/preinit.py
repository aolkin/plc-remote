
from plc.network.auto import AutoClient

from wifi import Cell, Scheme

import asyncio
import subprocess

def get_current_wifi():
    try:
        return subprocess.check_output("iwgetid").decode().split('"')[1]
    except subprocess.CalledProcessError:
        return None

def autoconf(conf):
    loop = asyncio.get_event_loop()
    auto = AutoClient()
    conf["server"] = loop.run_until_complete(auto.get_server)
    conf.save()

def _name(i):
    return i.address.replace(":","-")
    
def wifi(display, conf):
    if conf.get("wifi") and not get_current_wifi():
        cells = Cell.all(conf["wifi"]["interface"])
        for i in cells:
            scheme = Scheme.find(conf["wifi"]["interface"],_name(i))
            if not scheme:
                if i.ssid in conf["wifi"]["networks"]:
                    display.animateRow(0,"Preparing " + i.ssid)
                    scheme = Scheme.for_cell(
                        conf["wifi"]["interface"], _name(i),
                        i, conf["wifi"]["networks"][i.ssid])
                    scheme.save()
            if scheme:
                display.animateRow(0,"Trying " + scheme.options["wpa-ssid"])
                scheme.activate()
                return True
        return False
                
        
