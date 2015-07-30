
from hardware import HWApp
from .components import *

from .contexts import *
from .receiver import Manager

class PLCRemote(HWApp):
    def __init__(self):
        super().__init__()
        # ALL THE MAGIC NUMBERS ARE BELONG TO ME
        self.add_hw(faders, keypad, display)

        self.bg = BackgroundContext(self)
        self.manager = Manager(self.bg)

        print(conf["server"])
        coro = self.loop.create_connection(lambda: ClientProtocol(
            conf["user"], conf["password"], self.manager),
            conf["server"]["address"], conf["server"]["port"])
        log("Connecting to {}:{} as '{}'...".format(conf["server"]["address"],
                                                    conf["server"]["port"],
                                                    conf["user"]))
        self.socket, self.protocol = self.loop.run_until_complete(coro)
        log("Connected.")

        self.loop.call_soon(bg.enter)
        self.mainloop()

