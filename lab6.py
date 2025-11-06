import pyvisa
import time
import math
import matplotlib.pyplot as plt
import numpy as np


#rm = pyisa...(**blank**)
rm = pyvisa.ResourceManager('C:\\Windows\\System32\\visa32.dll')
print(rm.list_resources())

#USB0::0x1AB1::0x0644::DG2P263801356::0::INSTR

#oscilloscope
scope = rm.open_resource('USB0::0x1AB1::0x0610::HDO1B26BM00073::INSTR')
print('here')

#function generator
gen = rm.open_resource('USB0::0x1AB1::0x0644::DG2P263801356::INSTR')

print(gen.query("*IDN?"))
print(scope.query("*IDN?"))

START_FREQ = 10
STOP_FREQ = 100000
NUM_POINTS = 30
AMPLITUDE = 1.0
OFFSET = 0.0
DELAY = 1.0   # allow full settling per step
POINTS = 25000

frequencies = np.logspace(np.log10(START_FREQ), np.log10(STOP_FREQ), NUM_POINTS)
gain_db = []
phase_deg = []

# -----------------------------
# Configure instruments
# -----------------------------
gen.write("*RST")
gen.write("SOUR1:FUNC SIN")
gen.write(f"SOUR1:VOLT {AMPLITUDE}")
gen.write(f"SOUR1:VOLT:OFFS {OFFSET}")
gen.write("OUTP1 ON")

# Fixed scope configuration for consistency
scope.write(":STOP")
scope.write(":CHAN1:DISP ON")
scope.write(":CHAN2:DISP ON")
scope.write(":CHAN1:SCAL 0.5")
scope.write(":CHAN2:SCAL 0.5")
scope.write(":TIM:SCAL 0.001")      # adjust to fit multiple cycles
scope.write(f":WAV:POIN {POINTS}")
scope.write(":RUN")
time.sleep(2)

# -----------------------------
# Measurement loop
# -----------------------------
for f in frequencies:
    gen.write(f"SOUR1:FREQ {f}")
    time.sleep(DELAY)

    scope.write(":STOP")
    time.sleep(0.2)

    # Get CH1
    scope.write(":WAV:MODE NORM")
    scope.write(":WAV:FORM BYTE")
    scope.write(":WAV:SOUR CHAN1")
    pre = scope.query(":WAV:PRE?").split(',')
    xinc = float(pre[4])
    yinc = float(pre[7])
    yoff = float(pre[8])
    yorg = float(pre[9])
    data1 = np.array(scope.query_binary_values(":WAV:DATA?", datatype='B'))
    ch1 = (data1 - yoff) * yinc + yorg

    # Get CH2
    scope.write(":WAV:SOUR CHAN2")
    pre = scope.query(":WAV:PRE?").split(',')
    xinc = float(pre[4])
    yinc = float(pre[7])
    yoff = float(pre[8])
    yorg = float(pre[9])
    data2 = np.array(scope.query_binary_values(":WAV:DATA?", datatype='B'))
    ch2 = (data2 - yoff) * yinc + yorg

    # Compute amplitude ratio
    vin = (np.max(ch1) - np.min(ch1)) / 2
    vout = (np.max(ch2) - np.min(ch2)) / 2
    if vin == 0 or np.isnan(vin) or vout == 0:
        gain_db.append(np.nan)
        phase_deg.append(np.nan)
        continue
    gain_db.append(20 * np.log10(vout / vin))

    # Compute phase via FFT
    fft1 = np.fft.rfft(ch1 - np.mean(ch1))
    fft2 = np.fft.rfft(ch2 - np.mean(ch2))
    freqs = np.fft.rfftfreq(len(ch1), d=xinc)
    idx = np.argmin(np.abs(freqs - f))
    phase = np.angle(fft2[idx]) - np.angle(fft1[idx])
    phase = np.degrees(np.unwrap([phase]))[0]
    phase_deg.append(phase)

    print(f"{f:.1f} Hz | Gain: {gain_db[-1]:.2f} dB | Phase: {phase_deg[-1]:.2f}°")

    scope.write(":RUN")

# -----------------------------
# Plot separate diagrams
# -----------------------------
plt.figure()
plt.semilogx(frequencies, gain_db, 'b')
plt.title('Bode Magnitude Plot')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(which='both', axis='both')

plt.figure()
plt.semilogx(frequencies, phase_deg, 'r')
plt.title('Bode Phase Plot')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (°)')
plt.grid(which='both', axis='both')

plt.show()

# -----------------------------
# Cleanup
# -----------------------------
gen.write("OUTP1 OFF")
gen.close()
scope.close()
rm.close()