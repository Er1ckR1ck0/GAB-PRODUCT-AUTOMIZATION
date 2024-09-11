from datetime import datetime
import pytz
from event import Event


class UserRubitime:

    def __init__(self, event: Event):
        self.name = event.DATA.name
        self.

