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

import ctypes
from ctypes.wintypes import BYTE, BOOL, WORD, DWORD, LONG, ULONG, LPVOID
from collections import namedtuple
import os

from msp430dll.api import API, StatusCode, STATUS_T
from msp430dll.base import BaseAPI, FileType
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

    def __new__(cls, dllPath = MSP_DLL):
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

##
##    def interfaces(self):
##        result = []
##        for num in range(self.base.getNumberOfIFs()):
##            name, status = dll.base.getIF(num)
##            result.append((name, status, ))
##        return result
##


