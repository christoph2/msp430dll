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

import enum

class MSPError(Exception):
    """
    """

    def __init__(self, *args, **kws):
        if 'errno' in kws:
            self.errno = kws.get('errno')
        super(Exception, self).__init__(*args)


class ErrorType(enum.IntEnum):
    NO_ERR                          = 0
    INITIALIZE_ERR                  = 1
    CLOSE_ERR                       = 2
    PARAMETER_ERR                   = 3
    NO_DEVICE_ERR                   = 4
    DEVICE_UNKNOWN_ERR              = 5
    READ_MEMORY_ERR                 = 6
    WRITE_MEMORY_ERR                = 7
    READ_FUSES_ERR                  = 8
    CONFIGURATION_ERR               = 9
    VCC_ERR                         = 10
    RESET_ERR                       = 11
    PRESERVE_RESTORE_ERR            = 12
    FREQUENCY_ERR                   = 13
    ERASE_ERR                       = 14
    BREAKPOINT_ERR                  = 15
    STEP_ERR                        = 16
    RUN_ERR                         = 17
    STATE_ERR                       = 18
    EEM_OPEN_ERR                    = 19
    EEM_READ_ERR                    = 20
    EEM_WRITE_ERR                   = 21
    EEM_CLOSE_ERR                   = 22
    FILE_OPEN_ERR                   = 23
    FILE_DETECT_ERR                 = 24
    FILE_END_ERR                    = 25
    FILE_IO_ERR                     = 26
    FILE_DATA_ERR                   = 27
    VERIFY_ERR                      = 28
    BLOW_FUSE_ERR                   = 29
    FUSE_BLOWN_ERR                  = 30
    INTEL_HEX_CODE_ERR              = 31
    WRITE_REGISTER_ERR              = 32
    READ_REGISTER_ERR               = 33
    INTERFACE_SUPPORT_ERR           = 34
    COMM_ERR                        = 35
    NO_EX_POWER                     = 36
    LOW_EX_POWER                    = 37
    EX_POWER_OK                     = 38
    HIGH_EX_POWER                   = 39
    SELFTEST_ERR                    = 40
    FLASH_TIMEOUT_ERR               = 41
    THREAD_ERR                      = 42
    EEM_INIT_ERR                    = 43
    RESOURCE_ERR                    = 44
    CLK_CTRL_ERR                    = 45
    STATE_STOR_ERR                  = 46
    READ_TRACE_ERR                  = 47
    VAR_WATCH_EN_ERR                = 48
    SEQUENCER_ERR                   = 49
    SEQ_ENABLE_ERR                  = 50
    CLR_SEQ_TRIGGER                 = 51
    SET_SEQ_TRIGGER                 = 52
    SPMA_ACTIVE_ERR                 = 53
    SPMA_INVALID_KEY_ERR            = 54
    SPMA_MAX_TRIALS                 = 55
    USB_FET_BSL_ACTIVE_ERR          = 56
    USB_FET_NOT_FOUND_ERR           = 57
    USB_FET_BUSY_ERR                = 58
    THREAD_ACTIVE_ERR               = 59
    THREAD_TERMINATE_ERR            = 60
    UNLOCK_BSL_ERR                  = 61
    BSL_MEMORY_LOCKED_ERR           = 62
    FOUND_OTHER_DEVICE              = 63
    WRONG_PASSWORD                  = 64
    UPDATE_MULTIPLE_UIF_ERR         = 65
    CDC_UIF_ERR                     = 66
    UIF_MANUAL_POWERCYCLE_NEEDED    = 67
    INTERNAL_ERR                    = 68
    INVALID_ERR                     = 69


ERROR_MAP = {
    ErrorType.NO_ERR: "No error",
    ErrorType.INITIALIZE_ERR: "Could not initialize device interface",
    ErrorType.CLOSE_ERR: "Could not close device interface",
    ErrorType.PARAMETER_ERR: "Invalid parameter(s)",
    ErrorType.NO_DEVICE_ERR: "Could not find device (or device not supported)",
    ErrorType.DEVICE_UNKNOWN_ERR: "Unknown device",
    ErrorType.READ_MEMORY_ERR: "Could not read device memory",
    ErrorType.WRITE_MEMORY_ERR: "Could not write device memory",
    ErrorType.READ_FUSES_ERR: "Could not read device configuration fuses",
    ErrorType.CONFIGURATION_ERR: "Incorrectly configured device; device derivative not supported",
    ErrorType.VCC_ERR: "Could not set device Vcc",
    ErrorType.RESET_ERR: "Could not reset device",
    ErrorType.PRESERVE_RESTORE_ERR: "Could not preserve/restore device memory",
    ErrorType.FREQUENCY_ERR: "Could not set device operating frequency",
    ErrorType.ERASE_ERR: "Could not erase device memory",
    ErrorType.BREAKPOINT_ERR: "Could not set device breakpoint",
    ErrorType.STEP_ERR: "Could not single step device",
    ErrorType.RUN_ERR: "Could not run device (to breakpoint)",
    ErrorType.STATE_ERR: "Could not determine device state",
    ErrorType.EEM_OPEN_ERR: "Could not open Enhanced Emulation Module",
    ErrorType.EEM_READ_ERR: "Could not read Enhanced Emulation Module register",
    ErrorType.EEM_WRITE_ERR: "Could not write Enhanced Emulation Module register",
    ErrorType.EEM_CLOSE_ERR: "Could not close Enhanced Emulation Module",
    ErrorType.FILE_OPEN_ERR: "File open error",
    ErrorType.FILE_DETECT_ERR: "File type could not be identified",
    ErrorType.FILE_END_ERR: "File end error",
    ErrorType.FILE_IO_ERR: "File input/output error",
    ErrorType.FILE_DATA_ERR: "File data error",
    ErrorType.VERIFY_ERR: "Verification error",
    ErrorType.BLOW_FUSE_ERR: "Could not blow device security fuse",
    ErrorType.FUSE_BLOWN_ERR: "Security Fuse has been blown",
    ErrorType.INTEL_HEX_CODE_ERR: "Error within Intel Hex file",
    ErrorType.WRITE_REGISTER_ERR: "Could not write device Register",
    ErrorType.READ_REGISTER_ERR: "Could not read device Register",
    ErrorType.INTERFACE_SUPPORT_ERR: "Not supported by selected Interface or Interface is not initialized",
    ErrorType.COMM_ERR: "Interface Communication error",
    ErrorType.NO_EX_POWER: "No external power supply detected",
    ErrorType.LOW_EX_POWER: "External power too low",
    ErrorType.EX_POWER_OK: "External power detected",
    ErrorType.HIGH_EX_POWER: "External power too high",
    ErrorType.SELFTEST_ERR: "Hardware Self Test Error",
    ErrorType.FLASH_TIMEOUT_ERR: "Fast Flash Routine experienced a timeout",
    ErrorType.THREAD_ERR: "Could not create thread for polling",
    ErrorType.EEM_INIT_ERR: "Could not initialize Enhanced Emulation Module",
    ErrorType.RESOURCE_ERR: "Insufficent resources",
    ErrorType.CLK_CTRL_ERR: "No clock control emulation on connected device",
    ErrorType.STATE_STOR_ERR: "No state storage buffer implemented on connected device",
    ErrorType.READ_TRACE_ERR: "Could not read trace buffer",
    ErrorType.VAR_WATCH_EN_ERR: "Enable the variable watch function",
    ErrorType.SEQUENCER_ERR: "No trigger sequencer implemented on connected device",
    ErrorType.SEQ_ENABLE_ERR: "Could not read sequencer state - Sequencer is disabled",
    ErrorType.CLR_SEQ_TRIGGER: "Could not remove trigger - Used in sequencer",
    ErrorType.SET_SEQ_TRIGGER: "Could not set combination - Trigger is used in sequencer",
    ErrorType.SPMA_ACTIVE_ERR: "System Protection Module A is enabled - Device locked",
    ErrorType.SPMA_INVALID_KEY_ERR: "Invalid SPMA key was passed to the target device - Device locked",
    ErrorType.SPMA_MAX_TRIALS: "Device does not accept any further SPMA keys - Device locked",
    ErrorType.USB_FET_BSL_ACTIVE_ERR: "MSP-FET430UIF Firmware erased - Bootloader active",
    ErrorType.USB_FET_NOT_FOUND_ERR: "Could not find MSP-FET430UIF on specified COM port",
    ErrorType.USB_FET_BUSY_ERR: "MSP-FET430UIF is already in use",
    ErrorType.THREAD_ACTIVE_ERR: "EEM polling thread is already active",
    ErrorType.THREAD_TERMINATE_ERR: "Could not terminate EEM polling thread",
    ErrorType.UNLOCK_BSL_ERR: "Could not unlock BSL memory segments",
    ErrorType.BSL_MEMORY_LOCKED_ERR: "Could not perform access, BSL memory segments are protected",
    ErrorType.FOUND_OTHER_DEVICE: "Another device as selected was found",
    ErrorType.WRONG_PASSWORD: "Could not enable JTAG wrong password",
    ErrorType.UPDATE_MULTIPLE_UIF_ERR: "Only one UIF must be connected during update to v3",
    ErrorType.CDC_UIF_ERR: "CDC-USB-FET-Driver was not installed. Please install the driver",
    ErrorType.UIF_MANUAL_POWERCYCLE_NEEDED: "Manual reboot of USB-FET needed ! PLEASE unplug and reconnect your USB-FET!!",
    ErrorType.INTERNAL_ERR: "Internal error",
    ErrorType.INVALID_ERR: "Invalid error number",
}

import unittest

class TestErrorCodes(unittest.TestCase):

    def testErrorCodeInEnum(self):
        self.assertEquals(ErrorType['PRESERVE_RESTORE_ERR'], 12)

    def testErrorCodeInNotEnum(self):
        with self.assertRaises(KeyError):
            value = ErrorType['FooBar']

    def testErrorCodeInErrorMap(self):
        self.assertEquals(ERROR_MAP[ErrorType.USB_FET_NOT_FOUND_ERR], 'Could not find MSP-FET430UIF on specified COM port')

    def testErrorCodeInNotErrorMap(self):
        with self.assertRaises(KeyError):
            value = ERROR_MAP['FooBar']


if __name__ == '__main__':
    unittest.main()
