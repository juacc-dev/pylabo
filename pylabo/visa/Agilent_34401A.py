import time
import numpy as np
import pandas as pd
import logging
from pylabo.visa.visa import VisaInstrument

logger = logging.getLogger("pylabo.visa")


class Agilent_34401A(VisaInstrument):
    def __init__(
        self,
        address,
        backend: str = None,
        **kwargs
    ):
        super().__init__(address, backend=backend, **kwargs)
        

    def voltage(self, range=None ,type="DC"):
        return float(self.query(f"MEASURE:VOLTAGE:{type}?"))
    
        
    def current(self, type="DC"):
        return float(self.query(f"MEASURE:CURRENT:{type}?"))
        
    def resistance(self):
        return float(self.query(f"MEASURE:RESISTANCE?"))

    def config(self):
        pass
    
    def read(self):
        r = self.query("READ?")
        return float(r)