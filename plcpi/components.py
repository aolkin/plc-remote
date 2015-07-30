
from plc.core.data import DMX_MAX_SLOT_VALUE

from hardware import *

faders = ADCSet(0x48, 3, True, 34, 3272, 0, DMX_MAX_SLOT_VALUE)

keypad = LEDKeypad()

display = ManagedDisplay()

SUB_FADERS = range(10)
X_FADER = 10
GM_FADER = 11

__all__ = ["faders", "keypad", "display"]
