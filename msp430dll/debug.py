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

from collections import OrderedDict
from ctypes import addressof, byref, create_string_buffer, cast, c_char, c_char_p, c_int32, POINTER, Union
from ctypes.wintypes import BYTE, BOOL, WORD, DWORD, LONG, LPVOID, WINFUNCTYPE

import enum
from msp430dll.api import API, STATUS_T
from msp430dll.base import ReadWriteType

class DEVICE_REGISTERS(enum.IntEnum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = 13
    R14 = 14
    R15 = 15

REGISTER_ALIAS = {
    "PC":   "R0",
    "SP":   "R1",
    "SR":   "R2",
    "CG1":  "R2",
    "CG2":  "R3",
}

def registerAlias(regName):
    return REGISTER_ALIAS.get(regName, regName)


def maskreg(reg):
    return (1 << reg)

ALL_REGS   = 0xffff

class RUN_MODES(enum.IntEnum):
    """Run modes.
    """
    FREE_RUN            = 1 # Run the device. Set breakpoints (if any) are disabled.
    SINGLE_STEP         = 2 # A single device instruction is executed. Interrupt processing is supported.
    RUN_TO_BREAKPOINT   = 3 # Run the device. Set breakpoints (if any) are enabled.


class STATE_MODES(enum.IntEnum):
    """State modes.
    """
    STOPPED                 = 0 # The device is stopped
    RUNNING                 = 1 # The device is running or is being single stepped
    SINGLE_STEP_COMPLETE    = 2 # The device is stopped after the single step operation is complete
    BREAKPOINT_HIT          = 3 # The device is stopped as a result of hitting an enabled breakpoint
    LPMX5_MODE              = 4 # The device is in LPMx.5 low power mode
    LPMX5_WAKEUP            = 5 # The device woke up from LPMx.5 low power mode


class EMEX_MODE(enum.IntEnum):
    """One of the following enumerations is returned in device.emulation.
    """
    EMEX_NONE               = 0 # Device has no Emex module.
    EMEX_LOW                = 1 # Device Emex module has two breakpoints.
    EMEX_MEDIUM             = 2 # Device Emex module has three breakpoints and range comparison.
    EMEX_HIGH               = 3 # Device Emex module has eight breakpoints, range comparison, state storage, and trigger sequencer.
    EMEX_EXTRA_SMALL_5XX    = 4 # Device Emex module has 2 breakpoints and range comparison.
    EMEX_SMALL_5XX          = 5 # Device Emex module has 4 breakpoints and range comparison.
    EMEX_MEDIUM_5XX         = 6 # Device Emex module has 6 breakpoints, range comparison and trigger sequencer.
    EMEX_LARGE_5XX          = 7 # Device Emex module has 8 or 10 breakpoints, range comparison, state storage, and trigger sequencer.


class DEVICE_CLOCK_CONTROL(enum.IntEnum):
    """One of the following enumerations is returned in device.clockControl.
    """
    GCC_NONE        = 0 # Device has no clock control. The system clock continue to function when the device is stopped by JTAG
    GCC_STANDARD    = 1 # Device has General Clock Control register
    GCC_EXTENDED    = 2 # Device has Extended General Clock Control register and Module Clock Control register 0.
    GCC_STANDARD_I  = 3 # Device has General Clock Control register (Note 1793).


# Bits of the EEM General Clock Control register (F41x).
TCE_SMCLK   = (1 << 0) # Clock SMCLK with TCLK. See Note 1.
ST_ACLK     = (1 << 1) # Stop ACLK
ST_SMCLK    = (1 << 2) # Stop SMCLK
TCE_MCLK    = (1 << 3) # Clock functional MCLK with TCLK. See Note 1
JT_FLLO     = (1 << 4) # Switch off FLL
ST_TACLK    = (1 << 5) # Stop TACLK

# Bits of the EEM Extended General Clock Control register (F43x/F44x).
ECLK_SYN    = (1 << 0) # Emulation clock synchronization. See Note 1
ST_MCLK     = (1 << 3) # Stop MCLK
FORCE_SYN   = (1 << 5) # Force JTAG synchronization. See Note 1

# Bits of the EEM General Control register.
# Do not use with MSP430_Configure(EMULATION_MODE, <bits>);
EEM_EN          = (1 << 0)
CLEAR_STOP      = (1 << 1)
EMU_CLK_EN      = (1 << 2)
EMU_FEAT_EN     = (1 << 3)
DEB_TRIG_LATCH  = (1 << 4)


# The actual name of this bit is STOPPED.
# Do not use with MSP430_Configure(EMULATION_MODE, <bits>);
EEM_STOPPED     = (1 << 7)

EMU_MODE_F44X_100   = 0x0000 # (Emulate) F44x 100 pins. This is the normal device mode.
EMU_MODE_F43X_100   = 0x4000 # Emulate F43x 100 pins.
EMU_MODE_F4XX_64    = 0x5000 # Emulate F4xx 64 pins.
EMU_MODE_F4XX_80    = 0x6000 # Emulate F4xx 80 pins.


class DebugAPI(API):

    FUNCTIONS = (
        ("MSP430_Registers", STATUS_T, [POINTER(c_int32), c_int32, c_int32]),
        ("MSP430_ExtRegisters", STATUS_T, [POINTER(c_int32), c_int32, c_int32, c_int32]),
        ("MSP430_Register", STATUS_T, [POINTER(c_int32), c_int32, c_int32]),
        ("MSP430_Run", STATUS_T, [c_int32, c_int32]),
        ("MSP430_State", STATUS_T, [POINTER(c_int32), c_int32, POINTER(c_int32)]), #  STATUS_T MSP430_State(int32_t* state, int32_t stop, int32_t* pCPUCycles);
        ("MSP430_CcGetClockNames", STATUS_T, [c_char_p, POINTER(DWORD)]),
        ("MSP430_CcGetModuleNames", STATUS_T, [c_char_p, POINTER(DWORD)]),
    )

    def run(self, mode, releaseJTAG):
        self.MSP430_Run(mode, releaseJTAG)

    def getState(self, stop):
        state = c_int32()
        cycles = c_int32()
        self.MSP430_State(byref(state), stop, byref(cycles))
        return (STATE_MODES(state.value), cycles.value)

   # def registers(self, regs, mask, rw):
   #     paramRegs = c_int32(regs)
   #     self.MSP430_Registers(byref(paramRegs), mask, rw)
   #     return paramRegs.value

    def readRegister(self, num):
        reg = c_int32()
        self.MSP430_Register(byref(reg), num, ReadWriteType.READ)
        return reg.value

    def writeRegister(self, num, value):
        reg = LONG(value)
        self.MSP430_Register(byref(reg), num, ReadWriteType.WRITE)

    def readRegisters(self):
        treg = c_int32 * 16
        registers = treg()
        regPointer = cast(registers, POINTER(c_int32))
        self.MSP430_Registers(regPointer, ALL_REGS, ReadWriteType.READ)
        return OrderedDict(zip(DEVICE_REGISTERS.__members__, registers))


    def readRegistersExt(self):
        treg = c_int32 * 16
        registers = treg()
        regPointer = cast(registers, POINTER(c_int32))
        self.MSP430_ExtRegisters(regPointer, ALL_REGS, 1, ReadWriteType.READ)
        return OrderedDict(zip(DEVICE_REGISTERS.__members__, registers))

