
from hardware import Context, TYPE
from plc.core.data import DMX_MAX_SLOT_VALUE
from .components import *

def val_to_str(val):
    return ("{:02}".format(round(val/DMX_MAX_SLOT_VALUE)) if
            val < DMX_MAX_SLOT_VALUE else "FL")

def justify(val, num, trim=False, zero=False):
    fmt = "{{:{fill}{num}{trimnum}}}".format(
        fill="0" if zero else " ", num=num,
        trimnum=("."+str(num) if trim else ""))
    return fmt.format(val)

class PLCContext(Context):
    def __init__(self, app, manager):
        super().__init__(app)
        self.manager = manager

class BackgroundContext(PLCContext):
    """Uses display, keypad (1-11, 13, 15), sub faders and GM
    App must have faders, keypad, and display attributes."""
    def __init__(self, app, display, faders, keypad):
        self.app = app
        self.__manager_initialized = False

    def set_manager(self, manager):
        if self.__manager_initialized:
            raise RuntimeError("Manager already set")
        else:
            super().__init__(self.app, manager)
            self.__manager_initialized = True
            self.xtra = SubContext(self.app, self.manager)

    def status(self, val):
        self.output(display, 71, "{: >12.12}".format(val))
            
    def enter(self):
        self.capture(faders, SUB_FADERS, self.handle_sub)
        self.capture(faders, GM_FADER, self.handle_gm)
        self.output(display, 60, "M:")
        self.status("Loading...")
        self.xtra.enter()
        self.handle_gm()

    def handle_gm(self, *args):
        val = faders.get(11)
        self.output(display, 62, val_to_str(val))

    def handle_sub(self, pin):
        val = faders.get(pin)
        print("Sub:", pin, "at", val)
        
class SubContext(PLCContext):
    """Uses X fader and keypad and display..."""

    def enter(self, val):
        self.select(0)
        self.capture(faders, X_FADER, self.handle_fade)

    def select(self, num):
        self.output(display, 64, justify(num, 3, True))
        self.group = num

    def handle_fade(*args):
        val = faders.get(X_FADER)
        print("X:",val)
