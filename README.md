# **UCI EECS 70B LAB 6 "WALKTHROUGH"**
**disclaimer: this setup may not be replicable on every machine. i personally highly advise ta's to reconsider requiring this softwares for labs going forward given the multitude of issues that may appear**

last updated: FA 2025 (11/05/2025)

@author: clement wu (discord: @citru | email @ ciwu@.uci.edu)

## **Step 0: Hardware**
This lab replaces ethernet cables with type A to B USB Ports, so no need for a lan/ethernet port as required in the lab. Only required ports are 2 USB-A ports to read both the oscilloscope and the function generator

## **Step 1: Downloads and Extracts**

1. Download [IO Libraries Suite](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html), scroll down for download. This SHOULD cover prerequisites, so no need to install it. I personally used SIC Expert.
2. Download [Command Expert](https://www.keysight.com/us/en/lib/software-detail/computer-software/command-expert-downloads-2151326.html), scroll down for download
3. Download [NI-VISA](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#575764) **not optional** since it is the python backend required by pyvisa to communicate via usb ports. pip installing "libusb" and "pyusb" for install doesn't seem to work well, so I did not bother. **yes, you need to make an account, the email NEEDS to be verified, will take FIFTEEN minutes to install fully, and will take up significant storage**
4. Download [Python 3.13.0](https://www.python.org/downloads/release/python-3130/) **python is not backwards compatable**, as in 3.14 will NOT work with 3.13. You must install THIS specific python version

took roughly 20 minutes to download everything on lab room wifi


## **Step 2: Commands**
1. Open up Powershell or Command Prompt (this has only been verified with Command Prompt, so translate all commands to Powershell if you choose to use it)
2. type:
```
pip install pyvisa-py 
```
    OR
```
pip install pyvisa 
```
depending on your version. you can check whether it works or not by going to and downloading test.py in this repository
3. type:
'''
py -m pip install matplotlib
'''
if you haven't already from the prelab! thank you to (discord: @maanya)
4. you MAY need to pip install other dependencies depending on errors if they show up in your terminal. doing so is fairly easy: simply look up the errors requiring some "pip install ..." and install said package. I believe I installed 2 more packages, but I have no idea if they are used/needed/work.

## **Step 3: Proceed As Normal! (Using the Lab Handout)**
Follow the Lab Handout and connect all the wires together to the machines. Beware that some wires may be faulty or the connection may be unstable at your ports. I will include some personal notes here:
- I used the most recent version of SIC Expert and it could automatically detect the usb ports when connected. For reference, I currently run an overheating i7-12700H, 16 GB RAM, Windows 11. 
- If your IO Libraries Suite does NOT launch, uninstall and reinstall. It's the fastest way to resolve the issue (yes, the uninstaller will appear to be not working but it does work. it just takes a long time due to the recursive uninstalling of dependency programs). restart your laptop when done (and whenever you follow a step and don't see a fix. nothing broke on my end when i restarted)
- I used a VSCode setup with MATLAB support and did NOT use IDLE. IDLE issues can/should be resolved by asking LLM's for advice.
- **It is in my humble opinion to skip** the "Sending commands to the AFG" section of the report. The methods/functions needed do not translate well to pure python code and doesn't paste properly.

## **Step 4: Updating Given Code**
The given code in the Lab Handout is as follows:
'''
import pyvisa
import time
import math
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
print(rm.list_resources())

scope = rm.open_resource('...')
gen = rm.open_resource('...)

print(gen.query("*IDN?))
print(scope.query("*IDN?))
'''

where i recommend to change (as per standard python convention AND for readability):
rm to resource_manager
scope to oscilloscope
gen to function_generator

if your ResourceManager throws errors of "no modules named ..." and/or "no backend available", you are using pure python backend instead of ni's. tell pyvisa to use it! change:
'''
rm = pyvisa.ResourceManager()
'''
    to:
'''
rm = pyvisa.ResourceManager( insert ni-visa address here )
'''
    in this case, my location was at 'C:\\Windows\\System32\\visa32.dll'. This address may change for different systems. In my case, this becomes:
'''
rm = pyvisa.ResourceManager('C:\\Windows\\System32\\visa32.dll')
'''

find the IP Addresses of the rm.open_resource to respective IP Addresses of function_generator and oscilloscope. if it looks something like "USB0::0x1AB1::0x0610::HDO1B26BM00073::INSTR", you're on the right track! it must match word for word, bar for bar.


## **Step 5: Running Code**
Check the Canvas for code attachments (or download the two 70lb.py files I have included in this repository) and they should work "beautifully".
Alternatively, if you would like to check out my code (or any part of my setup), see lab6.py in this repository. I was the only one ~~dumb enough~~ to code my own solution (that does not work as well as the canvas ones)
~~not noticing these two files took 2 hours away from our lives~~