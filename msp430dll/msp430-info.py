#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"
__description__ = "MSP430DLL (Python wrapper for msp430.dll)."
__copyright__ = """
  MSP430DLL (Python wrapper for msp430.dll).

  (C) 2016 by Christoph Schueler <https://github.com/christoph2,
                                       cpu12.gems@googlemail.com>

  All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from optparse import OptionParser
from pprint import pprint
import re
import sys

from msp430dll import DLL
from msp430dll.base import SystemNotifyCallback, ArchType
from msp430dll.debug import DebugAPI, RUN_MODES
from msp430dll.utils import cygpathToWin

def myCallback(*params):
    print("myCallback called with: {0}".format(params))


def displayMemoryInfo(name, start, stop):
    if not start and not stop:
        rangeDescription = "[Not implemented]"
    else:
        rangeDescription = "from 0x{0:04x} to 0x{1:04x} ({2:>6d} bytes)".format(start, stop, stop - start + 1)
    return "{0:<10}: {1}".format(name, rangeDescription)

def yesNo(value):
    if value == 1:
        return "yes"
    elif value == 0:
        return "no"
    else:
        return "<unknown>"

def beautifyEnumerator(value):
    """
    """
    return re.sub(r"([^.]*\.)(.*)", r"\2", str(value))

def displayInfo(pathToDll, dllName, port = 'TIUSB'):
    """[
 ('clockControl', 1),
 ('coreIpId', 0),
 ('deviceIdPtr', 0L),
 ('eemVersion', 0),
 ('emulation', 1),
 ('endian', 43605),
 ('id', 52),
 ('jtagId', 0),
 ('nBreakpointsDma', 0),
 ('nBreakpointsOptions', 0),
 ('nBreakpointsReadWrite', 0),
 ('nCombinations', 2),
 ('nCycleCounter', 0),
 ('nCycleCounterOperations', 0),
 ('nRegTrigger', 0),
 ('nRegTriggerOperations', 0),
 ('nSequencer', 0),
 ('nStateStorage', 0),
 ('nTrigerMask', 0),
]
    """
    dll = DLL(pathToDll, dllName)
    dll.logger.setLevel("debug")
    ver = dll.base.initialize(port)
    major = ver / 10000000
    minor = ver / 100000
    patch = ver / 1000
    print("Dll-Version : {0}.{1}.{2:04d}".format(major, minor, patch))

    """uint32_t VersionInfo::get () const
{
        /* a.bb.cc.ddd */
        return (this->imajor * 10000000) + (this->iminor * 100000) + (this->patch * 1000) + this->flavor;
}
    """

    dll.base.setVCC(3000)

    dll.base.openDevice()

    result = dll.base.MSP430_SET_SYSTEM_NOTIFY_CALLBACK(SystemNotifyCallback(myCallback))
    device =  dll.base.getFoundDevice()
    print("Controller: {0}".format(device.string))
    print("Arch.     : {0}".format(beautifyEnumerator(ArchType(device.cpuArch))))
    print("\n")
    print("Memory")
    print("-"*60)
    print(displayMemoryInfo('RAM',device.ramStart ,device.ramEnd))
    print(displayMemoryInfo('RAM2',device.ram2Start ,device.ram2End))
    print(displayMemoryInfo('FLASH',device.mainStart ,device.mainEnd))
    print(displayMemoryInfo('INFO',device.infoStart ,device.infoEnd))
    print(displayMemoryInfo('BSL',device.bslStart ,device.bslEnd))
    print(displayMemoryInfo('LCD',device.lcdStart ,device.lcdEnd))
    print("FRAM      : {0}".format(yesNo(device.hasFramMemory)))
    print("\n")
    print("Voltages")
    print("-"*60)
    print("VCC       : {0:2.2f} V".format(dll.base.getVCC() / 1000.0))
    #print("ext. VCC  : {0:2.2f} V".format(dll.base.getExternalVoltage() / 1000.0))
    print("Min. VCC  : {0:2.2f} V".format(device.vccMinOp / 1000.0))
    print("Max. VCC  : {0:2.2f} V".format(device.vccMaxOp / 1000.0))
    print("Test VCC  : {0}".format(yesNo(device.hasTestVpp)))
    print("\n")
    print("Debugging")
    print("-"*60)
    print("Brk.-Pts. : {0}".format(device.nBreakpoints))
    print("\n")
    print("Registers")
    print("-"*60)

    #mem = dll.base.readMemory(dev.infoStart, None, dev.infoStart + dev.infoEnd + 1)
    #dll.base.readOutFile(dev.infoStart, dev.infoStart + dev.infoEnd + 1, "info.hex", FileType.FILETYPE_INTEL_HEX)

    jid  = dll.base.getJTAGId()
    print("JTAG-ID: {0:#x}".format(jid))

    #print(dll.interfaces())

    result = dll.debug.readRegisters()
    print(result)

    dll.debug.writeRegister(5, 4711)

    result = dll.debug.readRegister(5)
    print(result)

    #result = dll.debug.readRegistersExt()
    #print(result)

    #print(DLL.loadedDlls())

    print("STATE: {0}".format(dll.debug.getState(1)))

    dll.debug.run(RUN_MODES.FREE_RUN, 1)
    print dll.base.MSP430_Close(0)



"""
1. The interface is initialized: MSP430_Initialize()
2. The device Vcc is set: MSP430_GetExtVoltage()††, MSP430_VCC() MSP430_GetCurVCCT()
3. Configuring the JTAG protocol (Spy-bi-Wire 2-Wire JTAG, 4-wire JTAG) is optional. By default the protocol is selected automatic: MSP430_Configure()
4. The device is identified: MSP430_OpenDevice()
5. Return the identified device: MSP430_GetFoundDevice
6. The mode for verification is optionally configured: MSP430_Configure(). The device memory is manipulated using:
    erase [MSP430_Erase()]
    read/write [MSP430_Memory(), MSP430_ReadOutFile(), MSP430_ProgramFile()]
    verify [MSP430_VerifyFile(), MSP430_VerifyMem(), MSP430_EraseCheck()]
8. The device function is manipulated by:
    blowing the security fuse [MSP430_Secure()]
    reset [MSP430_Reset()]
9. The device interface is closed: MSP430_Close()
10. Errors are handled: MSP430_Error_Number(), MSP430_Error_String()
"""

# MSP43.h   - General application and device handling
"""

"""

# MSP430_Debug.h - debugging, controlling device program execution
"""

"""

# MSP430_EEM.h - enhanced debugging functions.
"""
"""

# MSP430_FET.h - MSP-FET430UIF maintenance functions.

def main():
    usage = "Usage: {0} [options] path-to-msp430.dll".format(sys.argv[0])

    options=[]
    args=[]

    op = OptionParser(usage = usage,version = "%prog " + __version__, description = "Display informations about connected MSP430 controllers.")
    op.add_option('-n', '--dll-name', help = "Name of DLL", dest = "dllName", type = str, default = "msp430")

    (options, args) = op.parse_args()
    if len(args) >= 1:
        pathToDll = args[0]
    else:
        pathToDll = "."
    displayInfo(cygpathToWin(pathToDll), options.dllName)

if __name__ == '__main__':
    main()

