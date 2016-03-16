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

from ctypes.wintypes import LONG
import enum

from msp430dll.errors import MSPError
from msp430dll.logger import Logger

STATUS_T = LONG

class StatusCode(enum.IntEnum):
    STATUS_ERROR = -1
    STATUS_OK = 0


class API(object):

    def __init__(self, parent, dll):
        self.dll = dll
        self.parent = parent
        self.unsupported = []
        self.logger = Logger()

    def isImplemented(self, funcName):
        return funcName not in self.unsupported
        # As of now, only 'MSP430_Identify' is affected.

    def returnValue(self, value):
        if value == -1:
            errno = self.parent.base.errorNumber()
            errstr = self.parent.base.errorString(errno)
            raise MSPError("{0} -- {1}.".format(errno, errstr), errno = errno)
        elif value != 0:
            self.warn("Unexpected return value: {0}".format(value))
        return StatusCode(value)

    def functionFactory(self, library, functionName, resultType, argTypes, errorChecker = None):
        #if not errorChecker:
        #    errorChecker = defaultChecker
        func = getattr(library, functionName)
        # These functions do not return 'STATUS_T'.
        if functionName not in ('MSP430_Error_Number', 'MSP430_Error_String', 'MSP430_GetCurVCCT', 'MSP430_GetExtVoltage'):
            func.restype = self.returnValue
        func.argtypes = argTypes
        return func

    def loadFunctions(self):
        for fun in self.FUNCTIONS:
            addFunction = True
            if len(fun) == 3:
                functionName, resultType, argTypes = fun
                if argTypes == []:
                    argTypes = None
                try:
                    function = self.functionFactory(self.dll, functionName, resultType, argTypes)
                except AttributeError as e:
                    self.info(str(e))
                    self.unsupported.append(functionName)
                    addFunction = False
            elif len(fun) == 4:
                functionName, resultType, argTypes, checker = fun
                if argTypes == []:
                    argTypes = None
                try:
                    function = self.functionFactory(self.dll, functionName, resultType, argTypes, checker)
                except AttributeError:
                    self.unsupported.append(functionName)
                    addFunction = False
            else:
                raise AttributeError("wrong length of function definition '{0}'.".format(fun))
            if addFunction:
                setattr(self, functionName, function)

    def info(self, *args):
        self.logger.info(*args)

    def debug(self, *args):
        self.logger.debug(*args)

    def error(self, *args):
        self.logger.error(*args)

    def warn(self, *args):
        self.logger.warn(*args)

