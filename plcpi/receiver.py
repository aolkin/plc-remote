
from plc.network import Receiver

class Manager(Receiver):
    """Protocol receiver, handles messages with appropriate contexts."""
    def __init__(self, bg):
        self.bg = bg
        self.bg.set_manager(self)
