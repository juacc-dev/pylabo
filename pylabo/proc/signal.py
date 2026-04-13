import numpy as np
import scipy.signal
import pandas as pd
import logging
from pylabo.proc.dataframe import pair_or_df, unpack

logger = logging.getLogger("pylabo.proc.signal")

def fft(x, y, *, skip_first=0):
    x_first = x.iat[0] if isinstance(x, pd.Series) else x[0]
    x_last = x.iat[-1] if isinstance(x, pd.Series) else x[-1]

    sampling_freq = x.size / x_last
    cut = y.size // 2

    fft = np.fft.fft(y)
    yfft = 2.0/len(y) * np.abs(fft)

    cut = y.size // 2

    xf = np.arange(0, sampling_freq, 1 / (x_last - x_first))
    yf = 2.0 / y.size * np.abs(yfft[:cut])
    xf = xf[:cut]

    return xf[skip_first:], yf[skip_first:]


def fourier_transform(
    df: pd.DataFrame,
    *,
    skip_first=0,
    low_pass=None
) -> pd.DataFrame:
    """
    Fourier transform of a dataframe.
    There should be only 4 columns in the dataframe
    """

    if len(df.columns) != 4:
        logger.error("Invalid dataframe shape. Expected 4 columns")
        return None

    x, err_x, y, err_y = unpack(df)

    xf, yf = fft(x, y, skip_first=skip_first)

    err_xf = 1 / (xf[1] - xf[0])

    if low_pass:
        xf, yf = low_pass_filter(xf, yf, low_pass)

    fft_df = pd.DataFrame({
        "Frecuencia": xf,
        "Error Frecuencia": err_xf,
        "Amplitud": yf,
        "Error Amplitud": 0,
    })

    return fft_df


def low_pass_filter(xf, yf, freq):
    cut = np.where(xf < freq)

    return xf[cut], yf[cut]


def find_highest_peaks(
    x_or_df,
    y=None,  # Must be set if x is not a DataFrame
    /,
    *,
    n=5,
    separation=0,
):
    x, y = pair_or_df(x_or_df, y)

    distance = separation / (x[1] - x[0])

    peaks, properties = scipy.signal.find_peaks(
        y,
        distance=distance
    )

    if peaks.size <= n:
        order = np.argsort(-y[peaks])
        return peaks[order]

    heights = y[peaks]

    top_n = np.argpartition(-heights, n - 1)[:n]
    top_n_sorted = top_n[np.argsort(-heights[top_n])]

    highest_peaks = peaks[top_n_sorted]

    return highest_peaks
