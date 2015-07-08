
from plc.network.receiver import Receiver

class Manager(Receiver):
    """Protocol receiver, handles messages with appropriate contexts."""
    def __init__(self, bg, dimmers):
        self.bg = bg
        self.dimmerc = dimmers
        self.dimmers = {}
        self.protocol = None
        self.bg.set_manager(self)

    def fatal(self, *args):
        self.bg.app.quit()
        
    def dimmer(self, dimmers, source=None):
        self.dimmers.update(dimmers)
        self.dimmerc.show_dimmers(dimmers, source)

    def registry(self, type_, reg):
        setattr(self, type_, reg)

    def get_list(self, l):
        return getattr(self, l)

    def group(self, *args):
        pass

    def cue(self, *args):
        pass

    def result(self, of, *args, **kwargs):
        log(of, args, kwargs)
        
