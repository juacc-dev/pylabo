# Information about SCPI:
# https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments
# SCPI Volume 1: Syntax and style (1999):
# https://www.ivifoundation.org/downloads/SCPI/scpi-99.pdf

# User guide for PyVISA:
# https://pyvisa.readthedocs.io/en/latest/introduction/index.html

# TODO: Check if the instruments actually support *OPC

import pyvisa as pyvisa
from pylabo import logging

logger = logging.init("pylabo.visa")

backends = {
    "NI-VISA": "",
    "PyVISA-Py": "@py",
}

DEFAULT_BACKEND = backends["PyVISA-Py"]

def find_instruments():
    rm = pyvisa.ResourceManager()

    print(rm.list_resources())


def channel_list(ch: int) -> list[int]:
    ch_list = [1, 2]

    match ch:
        case 0:
            pass
        case 1:
            ch_list = [1]
        case 2:
            ch_list = [2]
        case _:
            logger.error(f"Invalid channel {ch}")

    return ch_list


class Instrument:
    def __init__(
        self,
        address,
        *,
        backend: str = None,
        **kwargs
    ) -> None:

        if backend is None:
            backend = DEFAULT_BACKEND

        logger.info(f"Using backend {backend}.")

        self._instrument = pyvisa.ResourceManager(backend).open_resource(
            resource_name=address,
            # read_termination='\n',
            # write_termination='\n',
            **kwargs
        )

        self.check()


    def __del__(self):
        self._instrument.close()


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


    def write(
        self,
        cmd: str,
        *,
        binary: bool = False
    ) -> None:
        if binary is True:
            self._instrument.write_binary_values()
            return

        self._instrument.write(cmd)

    def query(
        self,
        cmd: str,
        *,
        binary: bool = False,
        ascii: bool = False,
        **kwargs
    ) -> str:
        if ascii is True:
            return self._instrument.query_ascii_values(
                cmd,
                **kwargs
            )

        if binary is True:
            return self._instrument.query_binary_values(
                cmd,
                **kwargs
            )

        return self._instrument.query(cmd)


    def is_done(self) -> bool:
        """
        This function should block
        """
        return self.query("*OPC?") == "1"
