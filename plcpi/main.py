
from plc.core.logging import *
from plc.core.settings import conf
from plc.network.protocols import ClientProtocol

from hardware.app import HardwareApp
from hardware.display import AnimatedDisplay
from .components import *

from .preinit import *

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
        self.predisp = AnimatedDisplay()

    def make_connection(self, conf):
        log("Connecting to {}:{} as '{}'...".format(conf["server"].get("address"),
                                                    conf["server"].get("port"),
                                                    conf["user"]))
        coro = self.loop.create_connection(lambda: ClientProtocol(
            conf["user"], conf["password"], self.manager),
            conf["server"].get("address"), conf["server"].get("port"))
        self.socket, self.protocol = self.loop.run_until_complete(coro)
        log("Connected.")
        
    def run(self, predisp, conf=conf):
        predisp.animateRow(2, "Step 2 of 5")
        predisp.animateRow(3, "Connecting to wifi...")
        wifi()
        predisp.animateRow(2, "Step 3 of 5")
        predisp.animateRow(3, "Trying server...")
        try:
            self.make_connection(conf)
        except (ValueError, OSError) as err:
            predisp.animateRow(2, "Step 4 of 5")
            predisp.animateRow(3, "Finding server...")
            autoconf(conf)
            predisp.animateRow(2, "Step 5 of 5")
            predisp.animateRow(3, "Connecting...")
            self.make_connection(conf)

        predisp.cleanup()
        self.loop.call_soon(self.bg.enter)
        self.mainloop()

