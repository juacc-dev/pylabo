# Information about SCPI:
# https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments
# SCPI Volume 1: Syntax and style (1999):
# https://www.ivifoundation.org/downloads/SCPI/scpi-99.pdf

# User guide for PyVISA:
# https://pyvisa.readthedocs.io/en/latest/introduction/index.html

# TODO: Check if the instruments actually support *OPC

import pyvisa
import logging
import re
import time

logger = logging.getLogger("pylabo.visa")

# Possible backends are NI-VISA (default) and PyVISA-Py ("@py")
DEFAULT_BACKEND = ""  # NI-VISA
STARTUP_SLEEP = 0.5


def print_devs() -> None:
    rm = pyvisa.ResourceManager()

    ids = rm.list_resources()

    for id in ids:
        if not re.match(r"ASRL.*", id):
            try:
                dev = rm.open_resource(id)
                print(f"{id}  -->  {dev.query('*IDN?')}")
            except Exception:
                continue


class VisaInstrument:
    def __init__(
        self,
        address,
        *,
        backend: str = None,
        **kwargs
    ) -> None:

        self._instrument = pyvisa.ResourceManager(backend).open_resource(
            resource_name=address,
            # read_termination='\n',
            # write_termination='\n',
            **kwargs
        )

        time.sleep(STARTUP_SLEEP)
        self.check()

    def __del__(self):
        self._instrument.close()

    def check(self) -> bool:
        id = self.query("*IDN?")

        if id is None:
            self._instrument.close()
            logger.error("Failed to identify intrument")

            return False

        return True

    def reset(self) -> None:
        self.write("*RST")

    def write(
        self,
        cmd: str,
        **kwargs
    ) -> None:
        """Write a single value to the instrument."""

        return self._instrument.write(cmd, **kwargs)

    def query(
        self,
        cmd: str,
        **kwargs
    ) -> str:
        """Query a single value from the instrument."""

        return self._instrument.query(cmd, **kwargs)

    def write_values(
        self,
        cmd: str,
        *,
        ascii: bool = True,
        **kwargs
    ):
        """Write multiple values to the instrument. By default, the messsage is
        sent in binary form, but passing ascii=True makes it use plain text."""

        if ascii:
            return self._instrument.write_ascii_values(
                cmd,
                **kwargs
            )

        else:
            return self._instrument.write_binary_values(
                cmd,
                **kwargs
            )

    def query_values(
        self,
        cmd: str,
        *,
        ascii: bool = True,
        separator=",",
        **kwargs
    ):
        """Query multiple values from the instrument. By default, the result is
        sent in binary form, but passing ascii=True makes it use plain text."""

        if ascii:
            return self._instrument.query_ascii_values(
                cmd,
                separator=separator,
                **kwargs
            )

        else:
            return self._instrument.query_binary_values(
                cmd,
                **kwargs
            )

    def opc(self) -> bool:
        return self.query("*OPC?") == "1"
