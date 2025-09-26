import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
from scipy.fft import rfft, rfftfreq
from collections import deque

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0)

SAMPLE_RATE = 2000
WINDOW_SIZE = 1000
DENOISE_WIN = 5

samples = deque(maxlen=WINDOW_SIZE)
timestamps = deque(maxlen=WINDOW_SIZE)

def moving_average(x, window_size=DENOISE_WIN):

    if window_size <= 1:
        return x
    return np.convolve(x, np.ones(window_size)/window_size, mode='same')


def estimate_frequency(y, t):

    mean = np.mean(y)
    centered = y - mean
    zero_crossings = np.where(np.diff(np.sign(centered)))[0]
    if len(zero_crossings) < 2:
        return 0.0
    crossing_times = t[zero_crossings]
    periods = np.diff(crossing_times)
    if len(periods) == 0:
        return 0.0
    return 1.0 / np.mean(periods)

def estimate_amplitude(y):
    #Half of peak-to-peak
    return (np.max(y) - np.min(y)) / 2

def classify_waveform(y, amp):
    """Classify using first derivative statistics"""
    # Normalize
    y_norm = (y - np.mean(y)) / np.ptp(y)
    dy = np.diff(y_norm)

    abs_avg = np.mean(np.abs(y)) / amp     # large for square
    slope_var = np.std(np.abs(dy)) / amp             # small for triangle
    curvature = np.std(np.diff(dy)) / amp    # large for sine


    if abs_avg > .9:
        return "Square"
    elif abs_avg > .6:
        return "Sin"
    else:
        return "Triangle"

if __name__ == "__main__":
    print("analyizngg")
    start = time.perf_counter()

    while True:

        voltage = chan.voltage
        now = time.perf_counter() - start
        samples.append(voltage)
        timestamps.append(now)

        if len(samples) == WINDOW_SIZE:
            y = np.array(samples)
            t = np.array(timestamps)

            freq = estimate_frequency(y, t)
            amp = estimate_amplitude(y)
            wtype = classify_waveform(y, amp)

            print(f"Waveform: {wtype}, "
                  f"Freq: {(freq/2):.2f} Hz, "
                  f"Amplitude: {(amp*2):.2f} V")

        time.sleep(1.0 / SAMPLE_RATE)