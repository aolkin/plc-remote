
from plc.network.receiver import Receiver

class Manager(Receiver):
    """Protocol receiver, handles messages with appropriate contexts."""
    def __init__(self, bg):
        self.bg = bg
        self.bg.set_manager(self)

    def dimmer(self, *args, **kwargs):
        pass

    def registry(self, *args, **kwargs):
        pass
