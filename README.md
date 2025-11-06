# **UCI EECS 70B LAB 6 "WALKTHROUGH"**
disclaimer: this setup may not be replicable on every machine. 
**i personally highly advise ta's to reconsider requiring this softwares for labs going forward given the multitude of issues that may appear**

last updated: FA 2025 (11/05/2025)

@author: clement wu (discord: @citru | email @ ciwu@.uci.edu)

## **Step 0: Hardware**
This lab replaces ethernet cables with type A to B USB Ports, so no need for a lan/ethernet port.
Only required ports are 2 USB-A ports to read both the oscilloscope and the function generator

## **Step 1: Downloads and Extracts**

1. Download [IO Libraries Suite](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html), scroll down for download. This SHOULD cover prerequisites, so no need to install it
2. Download [Command Expert](https://www.keysight.com/us/en/lib/software-detail/computer-software/command-expert-downloads-2151326.html), scroll down for download
3. Download [NI-VISA](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html#575764) **not optional** since it is the python backend required by pyvisa to communicate via usb ports. "libusb" and "pyusb" for install doesn't seem to work well, so I did not bother.
4. Download [Python 3.13.0](https://www.python.org/downloads/release/python-3130/) **python is not backwards compatable**, as in 3.14 will NOT work with 3.13. \
You must install THIS specific python version


## **STEP 2: Commands**
1. Open up Powershell or Command Prompt (this has only been verified with Command Prompt, so translate all commands to Powershell if you choose to use it)
2. type > pip install pyvisa-py OR > pip install pyvisa depending on your version