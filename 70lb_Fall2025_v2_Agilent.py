

import pyvisa
print("pyvisa imported successfully!")
import time
import math
import matplotlib.pyplot as plt


rm = pyvisa.ResourceManager()
print(rm.list_resources())

#scope = rm.open_resource('TCPIP0::169.254.254.254::inst0::INSTR')
scope = rm.open_resource('GPIB3::8::INSTR')
print('here')
gen = rm.open_resource('GPIB3::10::INSTR')
print('here')
# write
# read
# query

# verify
print(gen.query("*IDN?"))
print(scope.query("*IDN?"))

# reset
gen.write(":OUTPut:STATe 0")
gen.write(":OUTPut:LOAD INFinity")
time.sleep(2)

# change output load
gen.write(":OUTPut:LOAD INFinity")
gen.write(":OUTPut:STATe 0")


vpp_in_arr = []
vpp_out_arr = []
gain_arr = []
phase_arr = []

# Note that freq is in Hz not in rad/s. You can convert by multiply with 2pi
# unit is Hz. kHz needs to *1000
freq_arr = list(range(1000, 50000, 3000))

for freq in freq_arr:
    # set freq and v of sin wave.
    gen.write(":APPLy:SINusoid {f},{v}".format(f=freq, v=2.5))
    time.sleep(1)
    # turn on output
    gen.write(":OUTPut:STATe 1")
    # warm up
    time.sleep(1)

    # autoscale scope
    scope.write(":AUToscale CHANNEL1,CHANNEL2")
    time.sleep(3)
    
    # read vpp and phase
    vpp_in = float(scope.query(":MEASure:VAMPlitude? CHANNEL1"))
    vpp_out = float(scope.query(":MEASure:VAMPlitude? CHANNEL2"))
    time.sleep(2)
    phase = float(scope.query(":MEASure:PHASe? CHANNEL2,CHANNEL1"))
    # derive gain
    gain = 20 * math.log(vpp_out/vpp_in, 10)+6
    # phase: angle
    phase = phase 

    print('freq:', freq, 'vpp in: ', vpp_in, 'vpp out: ', vpp_out, 'phase: ', phase)

    # save to list
    vpp_in_arr.append(vpp_in)
    vpp_out_arr.append(vpp_out)
    gain_arr.append(gain)
    phase_arr.append(phase)

    # turn off generator output
    time.sleep(2)
    #gen.write(":OUTPut:STATe 0")
    #time.sleep(1)    

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Bode Plot')

#ax1.set_title('Gain')
ax1.semilogx(freq_arr, gain_arr)
ax1.set_ylabel('Magnitude (dB)')

#ax2.set_title('Phase')
ax2.semilogx(freq_arr, phase_arr)
ax2.set_ylabel('Phase(Degree)')
ax2.set_xlabel('Frequency (Hz)')

plt.show()


plt.semilogx(freq_arr, gain_arr)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.show()

plt.semilogx(freq_arr, phase_arr)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Degree')
plt.ylim(-360, 360)
plt.grid(True)
plt.show()

# close
gen.close()
scope.close()
rm.close()
print('end')

