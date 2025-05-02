# Information about SCPI:
# https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments

# User guide for PyVISA:
# https://pyvisa.readthedocs.io/en/latest/introduction/index.html

import pyvisa as pyvisa
from enum import Enum
import numpy as np

def find_instruments():
    rm = pyvisa.ResourceManager()

    print(rm.list_resources())


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



class Instrument:
    def __init__(
        self,
        address,
        **kwargs
    ) -> None:

        self._instrument = pyvisa.ResourceManager().open_resource(
            resource_name=address,
            # read_termination='\n',
            # write_termination='\n',
            **kwargs
        )

        self.check()


    def check(self) -> bool:
        idn = self.query("*IDN?")
        if idn:
            self.idn = idn
            print(f"Conectado a {idn}.")

            return True

        else:
            self.close()
            print("No se pudo identificar el instrumento :(")

            return False


    def close(self) -> None:
        self._instrument.close()


    def reset(self) -> None:
        self.write("*CLS")

    def write(self, cmd: str) -> None:
        self._instrument.write(cmd)


    def query(self, cmd: str) -> str:
        return self._instrument.query(cmd)


    def is_done(self) -> bool:
        """
        This function should block
        """
        return self.query("*OPC?") == "1"


class FunctionGenerator(Instrument):
    def volt(self, voltage=None, ch=1):
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



class Osciloscopio(Instrument):
    def acquire(
        self,
        *,
        on: bool = None,
        avg: int = None # Only supports 4, 16, 64 and 128
    ) -> None:
        if avg is not None:
            self.write(f"ACQuire:MODe AVErage {avg}")

        if on is not None:
            state = 1 if on is True else 0
            self.write(f"ACQuire:STATE {state}")

        return self.query("ACQuire?")

    # def autorange(
    #     self,
    #     *,
    #     on: bool = None
    # ):
    #     if on is not None:
    #         state = 1 if on is True else 0
    #         self.write(f"AUTORange:STATE {state}")

    #     # There is no query form for autorange
    #     # Programmer manual pg. 2-44 (62)
    #     return self.query("AUTORange")

    def autoset(self):
        return


    def vert(
        self,
        scale=None,
        pos=None,
        ch=1
    ):
        """
        Ejemplos de `scale` y `pos`:
            2E-3
            5E-3
            10E-3
            20E-3
            50E-3
            100E-3
            200E-3
            500E-3
            1E0
            2E0
            5E0
        """
        if scale is not None:
            self.write(f"CH{ch}:SCAle {scale}")

        if pos is not None:
            self.write(f"CH{ch}:POSition {pos}")

        if scale is None and pos is None:
            return self.query(f"CH{ch}?")


    def horiz(
        self,
        scale=None,
        pos=None,
    ):
        if scale is not None:
            self.write(f"HORizontal:SCAle {scale}")

        if pos is not None:
            self.write(f"HORizontal:POSition {pos}")

        if scale is None and pos is None:
            return self.query("HORizontal?")


    def curve(
        self,
        ch: int = 1,
        *,
        bar: bool = False
    ):
        # Set data source, in this case a channel
        self.write(f"DATa:SOURce CH{ch}")

        if bar is False:
            data = self._instrument.query_binary_values(
                "CURVe?",
                datatype="B",
                container=np.array
            )

        else:
            data = self._curve_bar()


    def _curve_bar(self):
        from tqdm import tqdm

        # Calculate the total number of bytes to download
        total_bytes = pyvisa.util.message_length(
            num_points=1000,
            datatype="f",
            header_format="ieee"
        )

        # Create a download monitor and use it when downloading data
        with tqdm(
            desc="Retrieving",
            unit="B",
            total=total_bytes
        ) as progress_bar:
            self.write("CURV?")

            data = self._instrument.read_binary_values(
                monitoring_interface=progress_bar
            )

        return data
