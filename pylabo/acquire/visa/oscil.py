from . visa import Instrument, channel_list
import time
import numpy as np
from pylabo import logging

logger = logging.init("pylabo.visa")

X_ACCURACY = 50.0 / 10 ** 6  # 50 ppm
Y_ACCURACY = 0.03  # 3% of measurement
Y_DIVISIONS = 8
X_DIVISIONS = 10
SCREEN_HEIGHT = 255
N = 2500

DATA_ENCODING = "RPBinary"  # positive integer, from 0 to 255
DATA_WIDTH = 1  # 8 bits

BAUD_RATE = 19200
LINE_TERMINATOR = ("LF", '\n')

BUSY_DELAY = 0.1  # seconds
BUSY_MAX_TRIES = 10


def tuplify(param) -> tuple:
    if not isinstance(param, tuple):
        return [param, param]

    return param


class Oscilloscope(Instrument):
    def __init__(
        self,
        address,
        backend: str = None,
        **kwargs
    ):
        super().__init__(address, backend=backend, **kwargs)

        self.write(f"RS232:BAUd {BAUD_RATE}")
        self._instrument.baud_rate = BAUD_RATE

        self.write(f"RS232:TRANsmit:TERMinator {LINE_TERMINATOR[0]}")
        self._instrument.read_terminator = LINE_TERMINATOR[1]
        self._instrument.write_terminator = LINE_TERMINATOR[1]


    def wait_busy(
        self,
        delay=BUSY_DELAY,
        max_tries=BUSY_MAX_TRIES
    ):
        n = 0

        while self.query("BUSY?") or n > max_tries:
            time.sleep(delay)

        if n > max_tries:
            logger.error(f"Wait timed out! (>{max_tries * delay * 1000} ms)")


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


    # def y_scale(self, ch, scale=None):
    #     """
    #     Ejemplos de `scale`:
    #         2E-3 5E-3 10E-3 20E-3 50E-3 100E-3 200E-3 500E-3 1E0 2E0 5E0
    #     """
    #     if scale is not None:
    #         self.write(f"CH{ch}:SCAle {scale}")

    #     return self.query(f"CH{ch}:SCAle?")

    # def y0(self, ch, pos=None):
    #     if pos is not None:
    #         self.write(f"CH{ch}:POSition {pos}")

    #     return self.query(f"CH{ch}:POSition?")

    # # Check this two methods
    # def x_scale(self, scale=None):
    #     if scale is not None:
    #         self.write(f"HORizontal:SCAle {scale}")

    #     return self.query("HORizontal:SCAle?")

    # def x0(self, pos=None):
    #     if pos is not None:
    #         self.write(f"HORizontal:POSition {pos}")

    #     return self.query("HORizontal:POSition?")

    # def vertical(
    #     self,
    #     *,
    #     ch=0,
    #     height=None, # In volts
    #     pos=None # ??
    # ):
    #     ch_list = channel_list(ch)

    #     # settings = {}

    #     for ch in ch_list:
    #         if height is not None:
    #             logger.debug(f"Setting scale of channel {ch}")

    #             scale = height / Y_DIVISIONS
    #             self.write(f"CH{ch}:SCAle {scale:.1E}")

    #         if pos is not None:
    #             logger.debug(f"Setting posisition of channel {ch}")

    #             self.write(f"CH{ch}:POSition {pos:.1E}")

    #     #     settings[ch] = self.query(f"CH{ch}:SCAle;POSition?")

    #     # logger.info(f"Osciloscope vertical settings: {settings}")

    #     # return settings

    # def horizontal(
    #     self,
    #     *,
    #     width=None, # In seconds
    #     pos=None
    # ):
    #     if width is not None:
    #         logger.debug("Setting horizontal scale")

    #         scale = width / X_DIVISIONS
    #         self.write(f"HORizontal:SCAle {scale:.1E}")

    #     if pos is not None:
    #         logger.debug("Setting horizontal position")

    #         self.write(f"HORizontal:POSition {pos:.1E}")

    #     # settings = self.query("HORizontal:SCAle;POSition?")

    #     # logger.info(f"Osciloscope horizontal settings: {settings}")

    #     # return settings


    def config(
        self,
        *,
        height: float | tuple[float] = None,  # In volts
        y0: float | tuple[float] = None,  # ??
        width: float = None,
        x0: float = None,
    ) -> None:

        heights = tuplify(height)
        y0s = tuplify(y0)

        channels = [1, 2]

        settings = {
            "height": (0, 0),
            "y0": (0, 0),
            "width": 0,
            "x0": 0
        }

        for h, ch in zip(heights, channels):
            if h is not None:
                scale = h / Y_DIVISIONS
                self.write(f"CH{ch}:SCAle {scale:.1E}")

            settings["height"][ch-1] = self.query(f"CH{ch}:SCALe?") * Y_DIVISIONS


        for pos, ch in zip(y0s, channels):
            if h is not None:
                self.write(f"CH{ch}:POSition {pos:.1E}")

            settings["y0"][ch-1] = self.query(f"CH{ch}:POSition?") * Y_DIVISIONS

        if width is not None:
            scale = width / X_DIVISIONS
            self.write(f"HORizontal:SCAle {scale:.1E}")

        settings["width"] = self.query("HORizontal:SCAle?")

        if x0 is not None:
            self.write(f"HORizontal:POSition {x0:.1E}")

        settings["width"] = self.query("HORizontal:POSition?")

        return settings


    # def query_config(self) -> list:
    #     pass


    def curve(
        self,
        ch,
    ):
        # Set data source, in this case a channel, the binary encoding and
        # the width
        self.write(
            f"DATa:SOURce CH{ch};ENCdg {DATA_ENCODING};WIDth {DATA_WIDTH}"
        )

        self.wait_busy()

        settings = self.query(
            "WFMPre:YZEro;YMUlt;YOFf?",
            ascii=True,
            separator=';'
        )

        sensitivity = self.query(f"CH{ch}:SCAle?") * Y_DIVISIONS / SCREEN_HEIGHT

        logger.info(f"Retrieved settings from channel {ch}: {settings}.")

        y0, vertical_units, vertical_offset = settings

        self.wait_busy()

        # Retrieve curve data
        data = self.query(
            "CURVe?",
            binary=True,
            datatype="B",
            container=np.array
        )

        logger.info(f"Read {len(data)} points from oscilloscope.")

        # data: values from 0 to 255
        # y_0: just what it sounds like
        # vertical_offset: adjust data for converting units.
        # vertical_units: converting factor, something like volts/pixel
        # (technically, in the manual says y_units per digitizer levels)
        y = y0 + (data - vertical_offset) * vertical_units

        # Size of a pixel (minimum unit of measure)

        # Error for each point, from the accuracy of the measurement
        # and the sensitivity of the Instrument
        sigma_y = Y_ACCURACY * (y - y0) + sensitivity

        events = self.query(
            "ALLEv?",
            ascii=True,
            separator=';'
        )

        logger.info(f"Oscilloscope events (channel: {ch}): {events}")

        return y, sigma_y


    def capture(self, ch: int = 0):
        """
        ch=0 means both channels, 1 and 2.
        """
        Y = []
        sigma_y = []

        ch_list = channel_list(ch)

        for ch in ch_list:
            data, sigma = self.curve()

            Y.append(data)
            sigma_y.append(sigma)

        # x0 = self.query("WFMPre:XZEro?")
        # logger.info(f"x_zero is {x0}")

        width = self.query("HORizontal:SCAle?") * X_DIVISIONS

        t = np.linspace(0, width, 2500)

        return t, np.array(Y), np.array(sigma_y)
        pass
