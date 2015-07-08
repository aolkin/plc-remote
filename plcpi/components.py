
from hardware import *

faders = ADCSet(0x48, 3, True, 36, 3264, 0, 100)

keypad = LEDKeypad(0x70)

display = ManagedDisplay()

__all__ = ["faders", "keypad", "display"]

SUB_FADERS = range(10)
X_FADER = 10
GM_FADER = 11

__all__ += ["SUB_FADERS", "X_FADER", "GM_FADER"]
