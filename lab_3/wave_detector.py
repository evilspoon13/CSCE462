import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import numpy as np
from scipy.fft import rfft, rfftfreq

# Initialize SPI
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D22)

mcp = MCP.MCP3008(spi, cs)

chan0 = AnalogIn(mcp, MCP.P0)

def sample_adc(chan, sample_rate, duration):

    #    Returns numpy array of voltages and actual sample_rate.
    
    N = int(sample_rate * duration)
    samples = np.empty(N, dtype=np.float32)
    period = 1.0 / sample_rate
    t0 = time.perf_counter()
    next_time = t0
    for i in range(N):
        # read value in volts directly
        samples[i] = chan.voltage
        next_time += period
        while time.perf_counter() < next_time:
            pass
    t1 = time.perf_counter()
    actual_rate = N / (t1 - t0)
    return samples, actual_rate

def frequency_from_fft(samples, fs):
    x = samples - np.mean(samples)
    yf = np.abs(rfft(x))
    xf = rfftfreq(len(x), 1/fs)
    if len(yf) < 2:
        return 0, yf, xf, 0
    peak_idx = np.argmax(yf[1:]) + 1
    return xf[peak_idx], yf, xf, peak_idx

def get_amplitude(samples):
    vpp = np.max(samples) - np.min(samples)
    return vpp

def classify_waveform(samples, fs, fundamental_idx, yf):

    vpp = get_amplitude(samples)

    fund_amp = yf[fundamental_idx]
    if fund_amp <= 0:
        return "unknown"

    harmonics = []
    for k in [3,5,7]:
        idx = fundamental_idx * k
        if idx < len(yf):
            harmonics.append(yf[idx]/fund_amp)
        else:
            harmonics.append(0)

    print(fund_amp)

    for (i, h) in enumerate(harmonics):
        print(i, h)


    else:
        return ["idk bro", vpp]

if __name__ == "__main__":
   
    try:
        
        samples, fs = sample_adc(chan0, 8000, 1)

        freq, yf, xf, fundamental_idx = frequency_from_fft(samples, fs)

        output = classify_waveform(samples, fs, fundamental_idx, yf)

        print(output)
    except KeyboardInterrupt:
        print("\nStopping...")