# Multiplexor Agilent 34870A
# Usado en labo 4 para leer termocuplas

# from enum import Enum
import logging
from visa import VisaInstrument
import numpy as np
from datetime import datetime

logger = logging.getLogger("pylabo.visa")


class Agilent_34970A(VisaInstrument):
    """Agilent 34970A multiplexor.
    Agilent's former Test and Measurement business has become Keysight
    Technologies."""

    def __init__(
        self,
        address,
        backend: str = None,
        **kwargs
    ):
        super().__init__(address, backend=backend, **kwargs)

        self.write("FORMAT:READING:CHANNEL ON")
        self.write("FORMAT:READING:TIME ON")
        self.write("FORMAT:READING:UNIT OFF")
        # self.write("FORMAT:READING:ALARM OFF")

        self._mux.write("FORMAT:READING:TIME:TYPE ABSOLUTE")

    def config(
        self,
        *,
        clear=False,
        channels: list[int] = None,
        delay: float = None,
        scan_interval: float = None,
        n_sweep: int = 1,
    ):
        if clear:
            self.write("*CLS")

        if channels is not None:
            self.write(f"ROUTE:SCAN (@{str(channels)[1:-1]})")
            self.channels = channels

        if scan_interval is not None:
            self.write(f"ROUTE:CHANNEL:DELAY {delay}")

        if scan_interval is not None:
            self.write(f"TRIGGER:TIMER {scan_interval}")
            self.write(f"TRIGGER:COUNT {n_sweep}")

    def get_time(self):
        hour, min, sec = self.query_values("SYSTEM:TIME?")

        return 3600 * float(hour) + 60 * float(min) + float(sec)

    def one_scan(self):
        data_raw = self.query_values("READ?", container=np.array)
        data = np.transpose(np.reshape(data_raw, (len(self.channels), 8)))

        temp = data[0]
        tiempo = data[1:7]
        tiempo = [
            datetime(
                int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int((x[5] % 1)*1000000)
            ).timestamp()
            for x in tiempo.T
        ]
        canal = data[7]

        return data, temp, tiempo, canal
