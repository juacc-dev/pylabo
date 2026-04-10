import numpy as np
import scipy.signal
# import pandas as pd
import logging

logger = logging.getLogger("pylabo.proc.signal")

def fourier_transform(x, y, skip_first=0):

    sampling_freq = x.size / x.iat[-1]
    cut = y.size // 2

    fft = np.fft.fft(y)
    yfft = 2.0/len(y) * np.abs(fft)

    cut = y.size // 2

    xf = np.arange(0, sampling_freq, 1 / (x.iat[-1] - x.iat[0]))
    yf = 2.0 / y.size * np.abs(yfft[:cut])
    xf = xf[:cut]

    return xf[skip_first:], yf[skip_first:]


def find_highest_peaks(x, y, n, separation=0):
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
