from . import visa
import numpy as np

X_ACCURACY = 50.0 / 10 ** 6
Y_ACCURACY = 0.03
DIVISIONS = 10
SCREEN_HEIGHT = 255

class Osciloscopio(visa.Instrument):
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


    def curve(
        self,
        chs: int = 0,
    ):
        """
        ch=0 means both channels, 1 and 2.
        """
        ys = []
        sigma_y = []

        channels = [1, 2] if chs == 0 else [1] if chs == 1 else [2]

        for ch in channels:
            # Set data source, in this case a channel
            self.write(f"DATa:SOURce CH{chs}")

            y0, y_units, vertical_offset = self.query(
                "WFMPre:YZEro;YMUlt;YOFf?"
                # ascii=True,
                # separator=';'
            )

            # Retrieve curve data
            data = self.query(
                "CURVe?",
                binary=True,
                datatype="B",
                container=np.array
            )

            # data: values from 0 to 255
            # y_0: just what it suonds like
            # vertical_offset: adjust data for converting units.
            # y_units: converting factor, something like volts/pixel
            # (technically, in the manual says y_units per digitizer levels)
            y = y0 + (data - vertical_offset) * y_units

            ys.append(y)

            sensitivity = self.y_scale(ch) * DIVISIONS / SCREEN_HEIGHT

            sigma_y.append(Y_ACCURACY * (y - y0) + sensitivity)


        x0 = self.query("WFMPre:XZEro?")

        t = np.arange(x0, x0 + ys[0].size, self.dx)

        return t, np.array(ys), np.array(sigma_y)
