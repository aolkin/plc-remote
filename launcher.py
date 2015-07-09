#!/usr/bin/env python3.4

if __name__ == "__main__":
    from hardware.display import AnimatedDisplay
    display = AnimatedDisplay()
    display.init()
    display.displayLoadingAnimation()
    display.animateRow(2, "Step 1 of 5")

import os, sys
from plcpi import PLCRemote
from plc.core.settings import Configuration

remote = PLCRemote()
conf = Configuration()
conf.load(os.environ.get("PLC_SETTINGS","settings.json"))

if __name__ == "__main__":
    if "--search" in sys.argv or "-s" in sys.argv:
        conf["server"]["address"] = None
    remote.run(display, conf)
