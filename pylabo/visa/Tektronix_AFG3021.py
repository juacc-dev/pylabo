from enum import Enum
import logging
from visa import VisaInstrument

logger = logging.getLogger("visa")


class Tektronix_AFG3021B(VisaInstrument):
    """Tektronix AFG3021 function generator."""

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

    def __init__(
        self,
        address,
        backend: str = None,
        **kwargs
    ):
        super().__init__(address, backend=backend, **kwargs)

    def output(
        self,
        state,
        ch=1,
    ):
        """Turn output state on or off. Possible arguments are "ON" (or 1) and
        "OFF" (or 0)."""

        if state is not None:
            self.write(f"OUTPut{ch}:STATe {state}")

    def set(
        self,
        ch=1,
        voltage=None,
        freq=None,
        shape: Funs | str = None,
        impedance=None
    ):
        """Set configuarion for the function generator."""

        if voltage is not None:
            self.write(f"SOURce{ch}:VOLTage {voltage}")

        if freq is not None:
            self.write(f"SOURce{ch}:FREQuency {freq}")

        if shape is not None:
            shape = shape.value if type(shape) is Tektronix_AFG3021B.Funs else shape

            self.write(f"SOURce{ch}:FUNCtion:SHAPe {shape}")

        if impedance is not None:
            self.write(f"OUTPut{ch}:IMPedance {impedance}")

    def get_voltage(self):
        return float(self.query("SOURce1:VOLTage?"))

    def get_freq(self):
        return float(self.query("SOURce1:FREQuency?"))

    def get_shape(self):
        return self.query("SOURce1:FUNCtion:SHAPe?")

    def get_impedance(self):
        return self.query("OUTPut1:IMPedance?")
