from . import visa
from enum import Enum


class Funs(Enum):
    SINE = "SINusoid"
    SQUARE = "SQUare"
    PULSE = "PULSe"
    RAMP = "RAMP"
    NOISE = "PRNoise"
    DC = "DC"
    SINC = "SINC"
    GAUSSIAN = "GAUSsian"
    LORENTZ = "LORentz"
    USER1 = "USER1"
    USER2 = "USER2"
    USER3 = "USER3"
    USER4 = "USER4"


class FunctionGenerator(visa.Instrument):
    def __init__(self, address, **kwargs):
        super().__init__(self, address, **kwargs)

    def voltage(self, voltage=None, ch=1):
        if voltage is not None:
            self.write(f"SOURce{ch}:VOLTage {voltage}")

        return self.query(f"SOURce{ch}:VOLTage?")


    def freq(self, frequency=None, ch=1):
        if frequency is not None:
            self.write(f"SOURce{ch}:FREQuency {frequency}")

        return self.query(f"SOURce{ch}:FREQuency?")


    def function(self, shape: Funs|str = None, ch=1):
        if shape is not None:
            shape = shape.value if type(shape) is Funs else shape

            self.write(f"SOURce{ch}:FUNCtion:SHAPe {shape}")

        return self.query(f"SOURce{ch}:FUNCtion:SHAPe?")


    def output(self, state=None, ch=1):
        if state is not None:
            self.write(f"OUTPut{ch}:STATe {state}")

        return self.query(f"OUTPut{ch}:STATe?")


    def impedance(self, value=None, ch=1):
        if value is not None:
            self.write(f"OUTPut{ch}:IMPedance {value}")

        return self.query(f"OUTPut{ch}:IMPedance?")
