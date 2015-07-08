
from plc.core.logging import *
from plc.core.settings import conf
from plc.network.protocols import ClientProtocol

from hardware import HardwareApp
from .components import *

from .contexts import *
from .receiver import Manager

class PLCRemote(HardwareApp):
    def __init__(self):
        super().__init__()
        # ALL THE MAGIC NUMBERS ARE BELONG TO ME
        self.add_hw(faders, keypad, display)

        self.bg = BackgroundContext(self)
        self.dimmers = DimmerContext(self)
        self.manager = Manager(self.bg, self.dimmers)

    def run(self, conf=conf):
        coro = self.loop.create_connection(lambda: ClientProtocol(
            conf["user"], conf["password"], self.manager),
            conf["server"]["address"], conf["server"]["port"])
        log("Connecting to {}:{} as '{}'...".format(conf["server"]["address"],
                                                    conf["server"]["port"],
                                                    conf["user"]))
        self.socket, self.protocol = self.loop.run_until_complete(coro)
        log("Connected.")

        self.loop.call_soon(self.bg.enter)
        self.mainloop()

