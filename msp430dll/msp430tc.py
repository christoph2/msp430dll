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

import binascii
from collections import namedtuple
import ctypes
from ctypes.wintypes import BYTE, BOOL, WORD, DWORD, LONG, ULONG, LPVOID
import enum
from pprint import pprint
import os
import threading

from msp430dll.api import API, StatusCode, STATUS_T
from msp430dll.base import BaseAPI, FileType
from msp430dll.debug import DebugAPI, RUN_MODES
from msp430dll.logger import Logger

MSP430_DLL = "msp430"
MSP_DLL = r"."

"""
#ifdef WIN32
static const char tilib_filename[] = "MSP430.DLL";
#else
static const char tilib_filename[] = "libmsp430.so";
#endif
"""

Instance = namedtuple('Instance', 'klass dll')

class DLL(object):

    _dllInstances = {}

    def __new__(cls, dllPath):  # Alternativ: PATH scannen.
        if dllPath not in DLL._dllInstances:
            klass = super(DLL, cls).__new__(cls)
            dll = DLL._loadDll(dllPath)

            baseApi = BaseAPI(dll)
            baseApi.loadFunctions()
            klass.base = baseApi

            debugApi = DebugAPI(dll)
            debugApi.loadFunctions()
            klass.debug = debugApi

            debugApi.errorNumber = baseApi.errorNumber
            debugApi.errorString = baseApi.errorString

            DLL._dllInstances[dllPath] = Instance(klass, dll)
        inst = DLL._dllInstances[dllPath]
        inst.klass.dll = inst.dll
        return inst.klass

    @classmethod
    def _loadDll(cls, dllPath):
        currentPath = os.getcwd()
        os.chdir(dllPath)
        mspDll = ctypes.windll.LoadLibrary(MSP430_DLL)
        os.chdir(currentPath)
        return mspDll

    @classmethod
    def loadedDlls(cls):
        result = []
        for path, inst in cls._dllInstances.items():
            item = "{0}\\{1}.dll".format(path, inst.dll._name)
            result.append(item)
        return result

    def interfaces(self):
        result = []
        for num in range(self.base.getNumberOfIFs()):
            name, status = dll.base.getIF(num)
            result.append((name, status, ))
        return result


def myCallback(*params):
    print("myCallback called with: {0}".format(params))


dll = DLL(MSP_DLL)
print hex(dll.base.initialize("TIUSB"))

#dll.base.MSP430_Close(False)

dll.base.setVCC(3000)

#result = dll.base.MSP430_SET_SYSTEM_NOTIFY_CALLBACK(SystemNotifyCallback(myCallback)) # This function should be called after MSP430_OpenDevice() function.

print dll.base.getVCC()
print dll.base.getExternalVoltage()
dll.base.openDevice("COM21")
dev =  dll.base.getFoundDevice()
pprint(sorted(dev._asdict().items()))

#mem = dll.base.readMemory(dev.infoStart, None, dev.infoStart + dev.infoEnd + 1)
#dll.base.readOutFile(dev.infoStart, dev.infoStart + dev.infoEnd + 1, "info.hex", FileType.FILETYPE_INTEL_HEX)


# See docs\index.html for further details.

jid  = dll.base.getJTAGId()
print("JTAG-ID: {0:#x}".format(jid))

print(dll.interfaces())

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
#print dll.base.MSP430_Close(0)



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
"""
If you don't know UML statecharts, here an example: ===, its abaout these small black circles...
"""

"""
echo '0e4c 0d40 3d50 0c00' | ./disassembler.py -x -
      0: 0E4C           mov    R12, R14
      1: 0D40           mov    PC, R13
      2: 3D50 0C00      add    #0xc, R13
"""
