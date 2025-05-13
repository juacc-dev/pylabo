from . visa import Instrument, channel_list
from enum import Enum
from pylabo import logging

logger = logging.init("pylabo.visa")

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


class FunctionGenerator(Instrument):
    def __init__(self, address, **kwargs):
        super().__init__(self, address, **kwargs)

    def output(
        self,
        ch=0,
        state=None
    ):
        ch_list = channel_list(ch)

        for ch in ch_list:
            if state is not None:
                self.write(f"OUTPut{ch}:STATe {state}")


    def config(
        self,
        ch=0,
        voltage=None,
        freq=None,
        shape=None,
        impedance=None,
    ):
        ch_list = channel_list(ch)

        settings = {}

        for ch in ch_list:
            if voltage is not None:
                self.write(f"SOURce{ch}:VOLTage {voltage}")

            if freq is not None:
                self.write(f"SOURce{ch}:FREQuency {freq}")

            if shape is not None:
                shape = shape.value if type(shape) is Funs else shape

                self.write(f"SOURce{ch}:FUNCtion:SHAPe {shape}")

            if impedance is not None:
                self.write(f"OUTPut{ch}:IMPedance {impedance}")


            settings[ch] = self.query(
                f"SOUR{ch}:VOLT;FREQ;FUNC:SHAP;:SOUR:IMP",
                ascii=True,
                separator=';'
            )


        logger.info(f"Fungen settings: {settings}")
        return settings
    # def voltage(self, voltage=None, ch=1):

    #     return self.query(f"SOURce{ch}:VOLTage?")


    # def freq(self, frequency=None, ch=1):

    #     return self.query(f"SOURce{ch}:FREQuency?")


    # def function(self, shape: Funs|str = None, ch=1):

    #     return self.query(f"SOURce{ch}:FUNCtion:SHAPe?")



    # def impedance(self, value=None, ch=1):

    #     return self.query(f"OUTPut{ch}:IMPedance?")
