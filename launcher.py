#!/usr/bin/env python3.4

if __name__ == "__main__":
    from hardware.display import AnimatedDisplay
    display = AnimatedDisplay()
    display.init()
    display.displayLoadingAnimation()

import os
from plcpi import PLCRemote
from plc.core.settings import Configuration

remote = PLCRemote()
conf = Configuration()
conf.load(os.environ.get("PLC_SETTINGS","settings.json"))

if __name__ == "__main__":
    display.stopLoadingAnimation()
    display.cleanup()
    remote.run(conf)
