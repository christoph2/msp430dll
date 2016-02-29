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

from collections import namedtuple
from ctypes import addressof, byref, create_string_buffer, cast, c_char, c_char_p, c_int32, POINTER, Structure, Union
from ctypes.wintypes import BYTE, BOOL, WORD, DWORD, LONG, ULONG, WINFUNCTYPE

import enum
from msp430dll.api import API, STATUS_T
from msp430dll.errors import ErrorType

class _DeviceStructure(Structure):
        # actually 108 Bytes.
        _pack_ = 1
        _fields_ = [
            ("endian", WORD),                   #: The value 0xaa55.
            ("id", WORD),                       #: Identification number.
            ("string", BYTE * 32),              #: Identification string.
            ("mainStart", WORD),                #: MAIN MEMORY starting address.
            ("infoStart", WORD),                #: INFORMATION MEMORY starting address.
            ("ramEnd", WORD),                   #: RAM ending address.
            ("nBreakpoints", WORD),             #: Number of breakpoints.
            ("emulation", WORD),                #: Emulation level.
            ("clockControl", WORD),             #: Clock control level.
            ("lcdStart", WORD),                 #: LCD starting address.
            ("lcdEnd", WORD),                   #: LCD ending address.
            ("vccMinOp", WORD),                 #: Vcc minimum during operation [mVolts].
            ("vccMaxOp", WORD),                 #: Vcc maximum during operation [mVolts].
            ("hasTestVpp", WORD),               #: Device has TEST/VPP.
            ("ramStart", WORD),                 #: RAM starting address.
            ("ram2Start", WORD),                #: RAM2 starting address.
            ("ram2End", WORD),                  #: RAM2 ending address.
            ("infoEnd", WORD),                  #: INFO ending address.
            ("mainEnd", ULONG),                 #: MAIN ending address.
            ("bslStart", WORD),                 #: BSL starting  address.
            ("bslEnd", WORD),                   #: BSL ending address.
            ("nRegTrigger", WORD),              #: Number of CPU Register Trigger.
            ("nCombinations", WORD),            #: Number of EEM Trigger Combinations.
            ("cpuArch", BYTE),                  #: The MSP430 architecture (non-X, X or Xv2).
            ("jtagId", BYTE),                   #: The JTAG ID - value returned on an instruction shift.
            ("coreIpId", WORD),                 #: The CoreIP ID.
            ("deviceIdPtr", ULONG),             #: The Device-ID Pointer.
            ("eemVersion", WORD),               #: The EEM Version Number.
            ("nBreakpointsOptions", WORD),      #: Breakpoint Modes.
            ("nBreakpointsReadWrite", WORD),
            ("nBreakpointsDma", WORD),
            ("nTrigerMask", WORD),              #: Trigger Mask for Breakpoint.
            ("nRegTriggerOperations", WORD),    #: Register Trigger modes.
            ("nStateStorage", WORD),            #: MSP430 has Stage Storage.
            ("nCycleCounter", WORD),            #: Number of cycle counters of MSP430.
            ("nCycleCounterOperations", WORD),  #: Cycle couter modes.
            ("nSequencer", WORD),               #: Msp430 has Sequencer.
            ("hasFramMemory", WORD),            #:  Msp430 has FRAM Memory.
        ]


def instanceiateNamedtuple(ntType, struc):
    result = []
    for field in ntType._fields:
        value = getattr(struc, field)
        if 'c_byte_Array' in str(type(value)):
            value = cast(value, c_char_p).value
        result.append(value)
    return ntType(*result)


def makeNamedtupleFromStructure(name, struct):
    # namedtuples are more convenient then these ctypes stuff.
    fields = []
    for field in struct._fields_:
        fields.append(field[0])

    return namedtuple(name, ' '.join(fields))

DeviceStructureNT = makeNamedtupleFromStructure("DeviceStructureNT", _DeviceStructure)

class Device(Union):
    _pack_ = 1
    _fields_ = [("buffer", c_char * 112), ("s", _DeviceStructure)]


DEVICE_UNKNOWN  = 0 #: Device id for unknown device.

class ArchType(enum.IntEnum):
    CPU_ARCH_ORIGINAL   = 0
    CPU_ARCH_X          = 1
    CPU_ARCH_XV2        = 2


class ReadWriteType(enum.IntEnum):
    WRITE = 0
    READ = 1


class EnableDisableType(enum.IntEnum):  # TODO: xxxType!!!
    DISABLE = 0
    ENABLE = 1


class ResetMethodType(enum.IntEnum):
    PUC_RESET   = (1 << 0)  #: Power up clear (i.e., a "soft") reset.
    RST_RESET   = (1 << 1)  #: RST/NMI (i.e., "hard").
    VCC_RESET   = (1 << 2)  #: Cycle Vcc (i.e., a "power on") reset.
    FORCE_RESET = (1 << 3)

    #: combines all possible reset methods enumerated in enum RESET_METHOD.
    ALL_RESETS = (PUC_RESET | RST_RESET | VCC_RESET)
    #: forces a Power up clear reset.
    FORCE_PUC_RESET = (FORCE_RESET | PUC_RESET)
    #: forces a RST/NMI clear reset.
    #: Non-Xv2 devices will be running and executing code after the reset.
    FORCE_RST_RESET = (FORCE_RESET | RST_RESET)
    #: forces a Vcc clear reset.
    #: Non-Xv2 devices will be running and executing code after the reset.
    FORCE_VCC_RESET = (FORCE_RESET | VCC_RESET)


class EraseType(enum.IntEnum):
    ERASE_SEGMENT = 0   #: Erase a segment.
    ERASE_MAIN = 1      #: Erase all MAIN memory.
    ERASE_ALL = 2       #: Erase all MAIN and INFORMATION memory not including IP protected area.
    ERASE_TOTAL = 3     #: Erase all MAIN and INFORMATION memory including IP protected area.


class ConfigModeType(enum.IntEnum):
    VERIFICATION_MODE = 0       #: Verify data downloaded to FLASH memories.
    EMULATION_MODE = 1          #: 4xx emulation mode.
    LOCKED_FLASH_ACCESS = 5     #: Allows Locked Info Mem Segment A access (if set to '1').
    EDT_TRACE_MODE = 7          #: Trace mode in EDT file format.
    INTERFACE_MODE = 8          #: Configure interface protocol: JTAG or Spy-bi-Wire (see enum INTERFACE_TYPE).
    # Configure a value that will be placed on the devices' MemoryDataBus
    # right before the device gets released from JTAG.
    # Used for Software Breakpoints.
    SET_MDB_BEFORE_RUN = 9
    # Configure whether RAM content should be preserved/restored
    # in MSP430_Erase() and MSP430_Memory() or not.
    # RAM_PRESERVE_MODE is set to ENABLE by default.
    # Usage Example for initial flash programming:
    # (1) MSP430_Configure(RAM_PRESERVE_MODE, DISABLE);
    # (2) MSP430_Erase(ERASE_ALL,..,..);
    # (3) MSP430_Memory(..., ..., ..., WRITE );
    # (4) MSP430_Memory(..., ..., ..., READ );
    # ..... Flash Programming/Download finished
    # (n) MSP430_Configure(RAM_PRESERVE_MODE, ENABLE);
    RAM_PRESERVE_MODE = 10
    # Configure the DLL to allow read/write/erase access to the 5xx
    # Bootstrap Loader (BSL) memory segments.
    UNLOCK_BSL_MODE =11
    # just used internal for the device code of L092 and C092
    DEVICE_CODE = 12
    # set true to write the external SPI image of the L092
    WRITE_EXTERNAL_MEMORY = 13
    # set DEBUG_LPM_X true to start debugging of LPMx.5
    # this will start polling for LPMX.5 events if a system notify callback was
    # previously set using MSP430_SET_SYSTEM_NOTIFY_CALLBACK()
    DEBUG_LPM_X = 14
    # Configure JTAG speed
    JTAG_SPEED = 15
    # total device erase including IP protection
    TOTAL_ERASE_DEVICE = 16


class InterfaceType(enum.IntEnum):
    JTAG_IF = 0             #: 4 Wire JTAG protocol used.
    SPYBIWIRE_IF = 1        #: 2 Wire (Spy-bi-wire) JTAG protocol used.
    SPYBIWIREJTAG_IF = 2    #: 2 Wire Devices accessed by 4wire JTAG protocol.
    AUTOMATIC_IF = 3        #: Protocol will be detected automatically.


class FileType(enum.IntEnum):
    FILETYPE_AUTO = 0       #: Auto detect */
    FILETYPE_TI_TXT = 1     #: TI text */
    FILETYPE_INTEL_HEX = 2  #: Intel hex */


class SystemEventMSPType(enum.IntEnum):
    #: System event FET connection is lost.
    FET_CONNECTION_LOST     = 0
    #: System event device connection is lost.
    DEVICE_CONNECTION_LOST  = 1
    #: System event FET restart needed.
    FET_RESTART_NEEDED      = 2
    #: System event device entered LPMx.5.
    DEVICE_IN_LPM5_MODE     = 3
    #: System event devices wakes up from LPMx.5.
    DEVICE_WAKEUP_LPM5_MODE = 4

# UmsSchedulerProc = WINFUNCTYPE(None, c_int32, POINTER(wintypes.ULONG), wintypes.LPVOID)
## typedef void (* SYSTEM_NOTIFY_CALLBACK) (SYSTEM_EVENT_MSP_t MySystemEvent);
SystemNotifyCallback = WINFUNCTYPE(None, c_int32)



class BaseAPI(API):

    FUNCTIONS = (
        ("MSP430_GetNumberOfUsbIfs", STATUS_T, [POINTER(LONG)]),
        ("MSP430_GetNameOfUsbIf", STATUS_T, [LONG, POINTER(c_char_p), POINTER(LONG)]),
        ("MSP430_SET_SYSTEM_NOTIFY_CALLBACK", STATUS_T, [SystemNotifyCallback]),
        ("MSP430_Initialize", STATUS_T, [c_char_p, POINTER(DWORD)]),
        ("MSP430_Close", STATUS_T, [LONG]),
        ("MSP430_GetJtagID", STATUS_T, [POINTER(LONG)]),
        ("MSP430_GetFoundDevice", STATUS_T, [c_char_p, LONG]),
        ("MSP430_OpenDevice", STATUS_T, [c_char_p, c_char_p, LONG, LONG, LONG]),
        ("MSP430_Identify", STATUS_T, []),
        ("MSP430_Device", STATUS_T, [LONG, c_char_p, LONG]),
        ("MSP430_Configure", STATUS_T, [LONG, LONG]),
        ("MSP430_VCC", STATUS_T, [LONG]),
        ("MSP430_GetCurVCCT", LONG, [POINTER(LONG)]),
        ("MSP430_GetExtVoltage", LONG, [POINTER(LONG), POINTER(LONG)]),
        ("MSP430_Reset", STATUS_T, [LONG, LONG, LONG]), # LONG method, LONG execute, LONG releaseJTAG)
        ("MSP430_Erase", STATUS_T, [LONG, LONG, LONG]), # LONG type, LONG address, LONG length
        ("MSP430_Memory", STATUS_T, [LONG, c_char_p, LONG, LONG]),    # LONG address, CHAR* buffer, LONG count, LONG rw
        ("MSP430_Secure", STATUS_T, []),
        ("MSP430_ReadOutFile", STATUS_T, [LONG, LONG, c_char_p, LONG]),   # LONG wStart, LONG wLength, CHAR* lpszFileName, LONG iFileType
        ("MSP430_ProgramFile", STATUS_T, []),
        ("MSP430_VerifyFile", STATUS_T, []),
        ("MSP430_VerifyMem", STATUS_T, []),
        ("MSP430_EraseCheck", STATUS_T, []),
        ("MSP430_Error_Number", STATUS_T, []),
        ("MSP430_Error_String", POINTER(c_char), [LONG]),   # c_char_p
    )

    def initialize(self, port = "TIUSB"):
        """.. py:method:: initialize(port)

            \brief   Initialize the interface.

            \note    1. This function must be called first.
            \note    2. MSP430_VCC() must be called second (after MSP430_Initialize() is called).
            \note    3. When initializing the MSP-FET430UIF (TI USB FET) parameter 'version' could
                        contain the value -1 or -3. This means that the Dll and the MSP-FET430UIF do not
                        have the same version (-3 means a major internal update is required).
                        MSP430_FET_FwUpdate() should be called.
                        MSP430_FET_FwUpdate() is part of the Maintenance API of the Dll.
                        When -3 was returned and calling MSP430_FET_FwUpdate(), the file CDC.log must exist
                        in the directory of the executed binary and the content must be the string "True"
                        without a newline. This file signals that a CDC driver is installed and prevents
                        the update from making the MSP-FET430UIF unusable.

            \param   port:    Interface port reference (application specific).
                            - To initialize a MSP-FET430PIF LPT Jtag adapter the parameter port should point to
                                a string which respresents the corresponding LPT port
                                (e.g. '1','2',... or 'LPT1','LPT2',...).
                            - To initialize TI's MSP-FET430UIF USB Jtag adapter the parameter
                                port should point to the string 'TIUSB' or just 'USB'.
                            - TI's MSP-FET430UIF USB Jtag adapter create Virtual Com Ports (VCPs)
                                on the PC system (see Device Manager). It is also possible to directly
                                pass the name of a dedicated VCP via this parameter (e.g. 'COM4, COM23,...).
                                This can be used to support multiple MSP-FET430UIF interfaces on one PC.
                                The later generation of USB development tools (eZ430-RF2500) no longer
                                uses the VCP approach. These tools enumerate as Human Interface Devices (HID)
                                on the USB. Since DLL version 2.03.00.000 it is also possible to directly
                                pass the name of a dedicated HID via this parameter.
                                When using a v3 MSP-FET430UIF it is enumerated as Communication Device Class (CDC).
                                Refer to MSP430_GetNumberOfUsbIfs() and MSP430_GetNameOfUsbIf()
                                for more information on VCP, HID and CDC.
            \param   version: The version number of the MSP430 DLL is returned (if version is not NULL).
                            A value of -1 or -3 reports a version conflict between the Dll and USB FET f/w.
                            In that case please refer to MSP430_FET_FwUpdate() on how to update
                            the firmware of the MSP-FET430UIF.

            \return  STATUS_OK:    The interface was initialized.
            \n       STATUS_ERROR: The interface was not initialized.

            \par     Error codes:
                     INITIALIZE_ERR
            \n       USB_FET_NOT_FOUND_ERR
            \n       USB_FET_BUSY_ERR
            \n           COMM_ERR
        """
        version = DWORD()
        self.MSP430_Initialize(port, byref(version))
        self.debug("MSP430_Initialize('{0}') - version returned: {1:#x}".format(port, version.value))
        return version.value

    def getVCC(self):
        voltage = LONG()
        self.MSP430_GetCurVCCT(byref(voltage))
        self.debug("MSP430_GetCurVCCT() returned: {0:d}".format(voltage.value))
        return voltage.value #/ 1000.0

    def setVCC(self, voltage):
        self.debug("MSP430_VCC({0:d})".format(voltage))
        self.MSP430_VCC(voltage)

    def getExternalVoltage(self):
        voltage = LONG()
        state = LONG()
        self.MSP430_GetExtVoltage(byref(voltage), byref(state))
        return (voltage.value, ErrorType(state.value))

    def openDevice(self, device = "DEVICE_UNKNOWN", password = "", deviceCode = 0, setId = 0):
        device = c_char_p(device)
        self.MSP430_OpenDevice(device, c_char_p(password), len(password), LONG(deviceCode), LONG(setId))

    def getJTAGId(self):
        jid = LONG()
        self.MSP430_GetJtagID(byref(jid))
        return jid.value

    def getFoundDevice(self):
        device = create_string_buffer(256)
        self.MSP430_GetFoundDevice(device, LONG(256))
        deviceStructure = cast(device, POINTER(_DeviceStructure))
        content = deviceStructure.contents
        return instanceiateNamedtuple(DeviceStructureNT, content)

    def memory(self, address, buf, byteCount, rw):   # LONG address, CHAR* buffer, LONG count, LONG rw
        # ReadWrite
        buf = create_string_buffer(byteCount)
        self.MSP430_Memory(address, buf, byteCount, rw)
        return buf

    def readMemory(self, address, buffer, byteCount):
        return self.memory(address, buffer, byteCount, ReadWriteType.READ)

    def writeMemory(self, address, buffer, byteCount):
        pass

    def readOutFile(self, start, length, filename, filetype = FileType.FILETYPE_AUTO):
        self.MSP430_ReadOutFile(start, length, filename, filetype.value)

    def getNumberOfIFs(self):
        number = LONG()
        self.MSP430_GetNumberOfUsbIfs(byref(number))
        return number.value

    def getIF(self, number):
        name = create_string_buffer(128)
        pName = c_char_p(addressof(name))
        status = LONG()
        self.MSP430_GetNameOfUsbIf(LONG(number), byref(pName), byref(status))
        return (pName.value, EnableDisableType(status.value), )

    def secure(self):
        self.MSP430_Secure()

    def errorNumber(self):
        err = self.MSP430_Error_Number()
        return err

    def errorString(self, number):
        return cast(self.MSP430_Error_String(number), c_char_p).value

