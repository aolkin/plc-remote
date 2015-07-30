#!/usr/bin/env python3.4

import os
from plcpi import PLCRemote
from plc.core.settings import Configuration

remote = PLCRemote()
conf = Configuration()
conf.load(os.environ.get("PLC_SETTINGS","clientsettings.json"))

if __name__ == "__main__":
    remote.run(conf)
