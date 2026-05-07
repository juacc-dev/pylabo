import time
import numpy as np
import pandas as pd
import logging
from pylabo.visa import VisaInstrument

logger = logging.getLogger("pylabo.visa")


class Agilent_34401A(VisaInstrument):
    def __init__(
        self,
        address,
        **kwargs
    ):
        super().__init__(address, **kwargs)


    def voltage(self, rg=None, kind="DC"):
        return float(self.query(f"MEASURE:VOLTAGE:{kind}?"))


    def current(self, kind="DC"):
        return float(self.query(f"MEASURE:CURRENT:{kind}?"))

    def resistance(self):
        return float(self.query("MEASURE:RESISTANCE?"))

    def config(self):
        pass

    def read(self):
        r = self.query("READ?")
        return float(r)
