import pyvisa, time, math, matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
print(rm.list_resources())

scope = rm.open_resource('USB0::0x1AB1::0x0610::HDO1B274M00032::INSTR')
gen   = rm.open_resource('USB0::0x1AB1::0x0644::DG2P263801366::INSTR')

# VISA quality-of-life
for inst in (scope, gen):
    inst.timeout = 10000           # 10 s
    inst.read_termination = '\n'
    inst.write_termination = '\n'

print(gen.query("*IDN?"))
print(scope.query("*IDN?"))

# Generator setup
gen.write(":OUTP:STAT 0")
gen.write(":OUTP:LOAD INF")
time.sleep(0.5)

freq_arr = list(range(1000, 30000, 2000))
vpp_in_arr, vpp_out_arr, gain_arr, phase_arr = [], [], [], []

for f in freq_arr:
    # DG2000/DG900 syntax: APPLy:SIN <freq>,<ampl>,<offset>
    gen.write(f":APPLy:SIN {f},2.5,0")
    gen.write(":OUTP:STAT 1")
    time.sleep(0.8)

    # Let scope find a good view
    scope.write(":AUToset")  # or ":AUToset:OPENch CHANnel1,CHANnel2"
    time.sleep(1.5)

    # Single-source measurements (use VPP or VAMP)
    vpp_in  = float(scope.query(":MEASure:ITEM? VPP,CHANnel1"))
    vpp_out = float(scope.query(":MEASure:ITEM? VPP,CHANnel2"))

    # Two-source phase: RRPHase/FRPHase/RFPHase/FFPHase
    phase   = float(scope.query(":MEASure:ITEM? RRPHase,CHANnel2,CHANnel1"))

    # Guard against divide-by-zero
    gain = -999.0 if vpp_in == 0 else 20*math.log10(vpp_out/vpp_in)

    print(f"freq: {f}  Vin_pp: {vpp_in:.3g}  Vout_pp: {vpp_out:.3g}  phase: {phase:.3g}")

    vpp_in_arr.append(vpp_in); vpp_out_arr.append(vpp_out)
    gain_arr.append(gain);     phase_arr.append(phase)

gen.write(":OUTP:STAT 0")

# Plots (unchanged)
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Bode Plot')
ax1.semilogx(freq_arr, gain_arr);  ax1.set_ylabel('Magnitude (dB)')
ax2.semilogx(freq_arr, phase_arr); ax2.set_ylabel('Phase (deg)'); ax2.set_xlabel('Frequency (Hz)')
plt.show()
