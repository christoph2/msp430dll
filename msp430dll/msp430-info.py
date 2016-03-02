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
import sys

from msp430dll import DLL
from msp430dll.base import SystemNotifyCallback
from msp430dll.debug import DebugAPI, RUN_MODES

def myCallback(*params):
    print("myCallback called with: {0}".format(params))

def displayInfo(pathToDll, port = 'TIUSB'):
    dll = DLL(pathToDll)
    print hex(dll.base.initialize("port))

    dll.base.setVCC(3000)

    print dll.base.getVCC()
    print dll.base.getExternalVoltage()
    dll.base.openDevice()

    result = dll.base.MSP430_SET_SYSTEM_NOTIFY_CALLBACK(SystemNotifyCallback(myCallback))
    device =  dll.base.getFoundDevice()
    pprint(sorted(device._asdict().items()))

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
    op.add_option('-f', '--dump-flash', help = "dump content of flash memory", dest = "dumpFlash", action = 
    "store_true", default = False)

    (options, args) = op.parse_args()
    if len(args) >= 1:
        pathToDll = args[0]
    else:
        filename = "."
    displayInfo(pathToDll)

if __name__ == '__main__':
    main()

