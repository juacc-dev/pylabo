from . visa import Instrument, channel_list
import numpy as np
from pylabo import logging

logger = logging.init("pylabo.visa")

X_ACCURACY = 50.0 / 10 ** 6  # 50 ppm
Y_ACCURACY = 0.03  # 3% of measurement
Y_DIVISIONS = 10
X_DIVISIONS = 15  # Maybe not
SCREEN_HEIGHT = 255

# DATA_ENCODING = ""


def closest(value, options):
    return min(options, key=lambda x: abs(x - value))


class Oscilloscope(Instrument):
    def __init__(self, address, **kwargs):
        super().__init__(self, address, **kwargs)

        self.x0: float = 0
        self.dx: float = 0

        self.y0 = np.zeros(3)
        self.y_scale = np.zeros(3)

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


    def y_scale(self, ch, scale=None):
        """
        Ejemplos de `scale`:
            2E-3 5E-3 10E-3 20E-3 50E-3 100E-3 200E-3 500E-3 1E0 2E0 5E0
        """
        if scale is not None:
            self.write(f"CH{ch}:SCAle {scale}")

        return self.query(f"CH{ch}:SCAle?")

    def y0(self, ch, pos=None):
        if pos is not None:
            self.write(f"CH{ch}:POSition {pos}")

        return self.query(f"CH{ch}:POSition?")

    # Check this two methods
    def x_scale(self, scale=None):
        if scale is not None:
            self.write(f"HORizontal:SCAle {scale}")

        return self.query("HORizontal:SCAle?")

    def x0(self, pos=None):
        if pos is not None:
            self.write(f"HORizontal:POSition {pos}")

        return self.query("HORizontal:POSition?")

    def config(
        self,
        ch=0,
        scale=None, # In volts
        pos=None # ??
    ):
        ch_list = channel_list(ch)

        # settings = {}

        for ch in ch_list:
            if scale is not None:
                logger.debug(f"Setting scale of channel {ch}")

                scale /= Y_DIVISIONS
                self.write(f"CH{ch}:SCAle {scale:.1E}")

            if pos is not None:
                logger.debug(f"Setting posisition of channel {ch}")

                self.write(f"CH{ch}:POSition {pos:.1E}")

        #     settings[ch] = self.query(f"CH{ch}:SCAle;POSition?")

        # logger.info(f"Osciloscope vertical settings: {settings}")

        # return settings

    def horizontal(
        self,
        scale=None, # seconds per division
        pos=None
    ):
        if scale is not None:
            logger.debug("Setting horizontal scale")

            scale /= X_DIVISIONS
            self.write(f"HORizontal:SCAle {scale:.1E}")

        if pos is not None:
            logger.debug("Setting horizontal position")

            self.write(f"HORizontal:POSition {pos:.1E}")

        # settings = self.query("HORizontal:SCAle;POSition?")

        # logger.info(f"Osciloscope horizontal settings: {settings}")

        # return settings


    def curve(
        self,
        ch: int = 0,
    ):
        """
        ch=0 means both channels, 1 and 2.
        """
        Y = []
        sigma_y = []

        ch_list = channel_list(ch)

        for ch in ch_list:
            if not self.is_done():
                logger.error("Oscilloscope is not done (??)")

            # Set data source, in this case a channel
            self.write(f"DATa:SOURce CH{ch}")
            # self.write(f"DATa:DATa ENCdg {DATA_ENCODING}")


            settings = self.query(
                "WFMPre:YZEro;YMUlt;YOFf?",
                ascii=True,
                separator=';'
            )

            logger.info(f"Retrieved settings from channel {ch}: {settings}.")

            y0, vertical_units, vertical_offset = settings

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

            Y.append(y)

            # Size of a pixel (minimum unit of measure)
            sensitivity = self.y_scale(ch) * Y_DIVISIONS / SCREEN_HEIGHT

            # Error for each point, from the accuracy of the measurement
            # and the sensitivity of the Instrument
            sigma_y.append(Y_ACCURACY * (y - y0) + sensitivity)


        x0 = self.query("WFMPre:XZEro?")

        logger.info(f"x_zero is {x0}")

        t = np.arange(x0, x0 + Y[0].size, self.dx)

        return t, np.array(Y), np.array(sigma_y)
