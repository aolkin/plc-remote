
from hardware import Context
from plc.core.data import DMX_MAX_SLOT_VALUE
from plc.network.messages import *
from .components import *

def val_to_str(val):
    return ("{:02}".format(val) if val < 100 else "FL")

def to_percent(val):
    return round(val / DMX_MAX_SLOT_VALUE * 100)

def justify(val, num, trim=False, zero=False):
    trim = False if type(val) == int else trim
    fmt = "{{:{fill}>{num}{trimnum}}}".format(
        fill="0" if zero else " ", num=num,
        trimnum=("."+str(num) if trim else ""))
    return fmt.format(val)

class PLCContext(Context):
    def __init__(self, app):
        self.__manager_initialized = False
        self.app = app

    def set_manager(self, manager):
        if self.__manager_initialized:
            raise RuntimeError("Manager already set")
        else:
            super().__init__(self.app)
            self.manager = manager
            self.__manager_initialized = True

class BackgroundContext(PLCContext):
    """Uses display, keypad (1-11, 13, 15), sub faders and GM
    App must have faders, keypad, and display attributes."""

    def set_manager(self, manager):
        super().set_manager(manager)
        self.xtra = SubContext(self.app)
        
    def status(self, val):
        self.output(display, 3, 8, "{: >12.12}".format(val))
            
    def enter(self):
        self.status("Loading...")
        self.capture(faders, SUB_FADERS, self.handle_sub)
        self.capture(faders, GM_FADER, self.handle_gm)
        self.output(display, 3, 0, "M")
        self.xtra.enter()
        self.status("Ready")

    def handle_gm(self, *args):
        val = faders.get(11)
        debug("GM:", val)
        self.output(display, 3, 1, val_to_str(val))

    def handle_sub(self, pin):
        val = faders.get(pin)
        self.app.protocol.send_message(
            GroupMessage("level", pin+1, val/100))
        debug("Sub:", pin+1, "at", val)
        
class SubContext(Context):
    """Uses X fader and keypad and display..."""

    def enter(self):
        self.select(0)
        self.capture(faders, X_FADER, self.handle_fade)

    def select(self, num):
        self.output(display, 3, 4, justify(num, 3, True))
        self.group = num

    def handle_fade(*args):
        val = faders.get(X_FADER)
        self.app.protocol.send_message(
            GroupMessage("level", self.group, val/100))
        debug("X:",val)

class DimmerContext(Context):

    def show_dimmers(self, dimmers, source=None):
        ch = " ".join([justify(i+1, 3, True, True) for i, j
                       in sorted(dimmers.items())])
        lvl = " ".join([justify(to_percent(i),
                                3, True, True) for j, i
                        in sorted(dimmers.items())])
        self.output(display, 0, 0, justify(ch,20,True))
        self.output(display, 1, 0, justify(lvl,20,True))
