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
from ctypes import addressof, byref, create_string_buffer, cast, c_char, c_char_p, c_int
from ctypes import Array, c_int32, c_uint32, c_uint16, c_uint64, Structure, POINTER, Union
from ctypes.wintypes import BYTE, BOOL, WORD, DWORD, LONG, LPVOID
from ctypes import WINFUNCTYPE

import enum
from msp430dll.api import API, STATUS_T
from msp430dll.base import ReadWriteType
from msp430dll.utils import StructureWithEnums


MAXHANDLE       = 20  #: The definition of MAXHANDLE is twice of the number of Memory-Bus and Register-Write triggers. More handles are impossible.
MAXTRIGGER      = 8  #: The definition of MAXTRIGGER is the number of Memory-Bus triggers.
N_TRACE_POS     = 8  #: The definition of N_TRACE_POS is the number of positions in the trace buffer.
MAX_SEQ_TRIGGER = 4  #: The definition of MAX_SEQ_TRIGGER is the number of available triggers used by the sequencer.
MAX_SEQ_STATE   = 4  #: The definition of MAX_SEQ_STATE is the number of available states of the sequencer.


class MessageIdType(StructureWithEnums):
    """Event message identification structure:
    This structure contains the message identifications for the
    different event messages sent by the DLL. Events are sent by the
    DLL to inform the caller of a change of state (e.g. breakpoint hit)
    or to provide data to the caller.
    """
    _pack_ = 1
    _fields_ = [
        ("uiMsgIdSingleStep", DWORD), #: Message identification for "Single step complete" event.
        ("uiMsgIdBreakpoint", DWORD), #: Message identification for "Breakpoint hit" event.
        ("uiMsgIdStorage", DWORD),    #: Message identification for "Storage on trace buffer" event.
        ("uiMsgIdState", DWORD),      # Message identification for "Change in new state of the sequencer" event.
        ("uiMsgIdWarning", DWORD),    #: Message identification for "Warning" event.
        ("uiMsgIdCPUStopped", DWORD), #: Message identification for "Device CPU stopped" event.
    ]


class MessageType(enum.IntEnum):
   WMX_SINGLESTEP   = 0x0400
   WMX_BREKAPOINT   = 0x0401
   WMX_STORAGE      = 0x0402
   WMX_STATE        = 0x0403
   WMX_WARNING      = 0x0404
   WMX_STOPPED      = 0x0405


class WarningCodes(enum.IntEnum):
    """WarCode contains the warning codes that are sent as an event."""
    WAR_CLR_COMBINE = 0        #: Combination removed.
    WAR_CLR_BP_COMBINE = 1     #: Breakpoint removed from combination.
    WAR_MOD_COMBINE = 2        #: Properties of combination changed.
    WAR_RESET = 3              #: Reset device
    WAR_DIS_TR_TRIGGER = 4     #: Trace trigger action is disabled and stored.
    WAR_EN_TR_TRIGGER = 5      #: Stored trace trigger action is enabled.
    WAR_EEM_THREAD_ACTIVE = 6  #: Polling thread is active - function call not allowed at the moment.
    WAR_EEM_CONFLICT = 7       #: forbidden old API call.


class BpMode(enum.IntEnum):
    """BpMode gives the supported modes for a breakpoint."""
    BP_CLEAR = 0    #: Clear breakpoint.
    BP_CODE = 1     #: Set code breakpoint.
    BP_RANGE = 2    #: Set range breakpoint.
    BP_COMPLEX = 3  #: Set complex breakpoint.
    BP_SOFTWARE = 4 #: Set software breakpoint.


class BpType(enum.IntEnum):
    """BpType gives the supported types for a breakpoint."""
    BP_MAB = 0      #: Set MAB breakpoint.
    BP_MDB = 1      #: Set MDB breakpoint.
    BP_REGISTER = 2 #: Set register breakpoint.


class BpAccess(enum.IntEnum):
    """BpAccess gives the supported access modes for a breakpoint."""
    BP_FETCH = 0                  #: Instuction fetch.
    BP_FETCH_HOLD = 1             #: Instruction fetch & hold trigger.
    BP_NO_FETCH = 2               #: No instruction fetch.
    BP_DONT_CARE = 3              #: Don't care.
    BP_NO_FETCH_READ = 4          #:No intruction fetch & read.
    BP_NO_FETCH_WRITE = 5         #:No instruction fetch & write.
    BP_READ = 6                   #:Read.
    BP_WRITE = 7                  #:Write.
    BP_NO_FETCH_NO_DMA = 8        #:No intruction fetch & no DMA access.
    BP_DMA = 9                    #:DMA access (read or write).
    BP_NO_DMA = 10                #:No DMA access.
    BP_WRITE_NO_DMA = 11          #:Write & no DMA access.
    BP_NO_FETCH_READ_NO_DMA = 12  #:No instruction fetch & read & no DMA access.
    BP_READ_NO_DMA = 13           #:Read & no DMA access.
    BP_READ_DMA = 14              #:Read & DMA access.
    BP_WRITE_DMA = 15             #:Write & DMA access.


class BpAction(enum.IntEnum):
    """BpAction gives the supported actions for a breakpoint."""
    BP_NONE = 0      #: No action on trigger (necessary for sequencer mechanism).
    BP_BRK = 1       #: Break on trigger.
    BP_STO = 2       #: Trigger state storage (trace mechnism) on trigger.
    BP_BRK_STO = 3   #: Break and trigger state storage on trigger.
    BP_CC = 4        #: Cycle counter.


class BpOperat(enum.IntEnum):
    """BpOperat gives the supported comparison operators for a breakpoint."""
    BP_EQUAL = 0    #: Address/value equal MAB/MDB.
    BP_GREATER = 1  #: Address/value greater MAB/MDB.
    BP_LOWER = 2    #: Address/value lower MAB/MDB.
    BP_UNEQUAL = 3  #: Address/value unequal MAB/MDB.


class BpRangeAction(enum.IntEnum):
    """BpRangeAction gives the supported range control for a range breakpoint."""
    BP_INSIDE = 0   #: Inside range.
    BP_OUTSIDE = 1  #: Outside range.


class BpCondition(enum.IntEnum):
    """BpCondition gives the exist condition for a complex breakpoint."""
    BP_NO_COND = 0  #: No condition available.
    BP_COND = 1     #: Condition available.


class BpParameter(StructureWithEnums):
    """The breakpoint structure contains the settings which are required to set, modify or clear a breakpoint."""
    _pack_ = 1
    _fields_ = [
        ("bpMode", c_int),          #: Breakpoint modes.
        ("lAddrVal", c_int32),      #: Breakpoint address/value (ignored for clear breakpoint).
        ("bpType", c_int),          #: Breakpoint type (used for range and complex breakpoints).
        ("lReg", c_int32),          #: Breakpoint register (used for complex breakpoints with register-write trigger).
        ("bpAccess", c_int),        #: Breakpoint access (used only for range and complex breakpoints).
        ("bpAction", c_int),        #: Breakpoint action (break/storage) (used for range and complex breakpoints).
        ("bpOperat", c_int),        #: Breakpoint operator (used for complex breakpoints).
        ("lMask", c_int32),         #: Breakpoint mask (used for complex breakpoints).
        ("lRangeEndAdVa", c_int32), #: Range breakpoint end address (used for range breakpoints).
        ("bpRangeAction", c_int),   #: Range breakpoint action (inside/outside) (used for range breakpoints).
        ("bpCondition", c_int),     #: Complex breakpoint: Condition available.
        ("lCondMdbVal", c_uint32),  #: Complex breakpoint: MDB value (used for complex breakpoints).
        ("bpCondAccess", c_int),    #: Complex breakpoint: Access (used for complex breakpoints).
        ("lCondMask", c_int32),     #: Complex breakpoint: Mask Value(used for complex breakpoints).
        ("bpCondOperat", c_int),    #: Complex breakpoint: Operator (used for complex breakpoints).
        ("wExtCombine", c_uint16),  #: Combine breakpoint: Reference of a combination handle.
    ]
    _map = {
        "bpMode": BpMode, "bpType": BpType, "bpAccess": BpAccess, "bpAction": BpAction, "bpOperat": BpOperat,
        "bpRangeAction": BpRangeAction, "bpCondition": BpCondition, "bpCondAccess": BpAccess, "bpCondOperat": BpOperat
    }


class CbControl(enum.IntEnum):
    """CbControl gives the supported control options for a combined breakpoint. Used in MSP430_EEM_SetCombineBreakpoint()"""
    CB_SET = 0      #: Combines two or several available breakpoints.
    CB_CLEAR = 1    #: Clears existing combination of two or several breakpoints.


class TrControl(enum.IntEnum):
    """Trace: Control."""
    TR_ENABLE = 0   #: Enable state storage.
    TR_DISABLE = 1  #: Disable state storage.
    TR_RESET = 2    #: Reset state storage.


class TrMode(enum.IntEnum):
    """Trace: Mode."""
    TR_HISTORY = 0   #: Trigger stops the Trace.
    TR_FUTURE = 1    #: Trigger starts the Trace - stops if buffer is full.
    TR_SHOT = 2      #: Start immediately - stops if buffer is full.
    TR_COLLECT = 3   #: Collect data only at trigger event - stops if buffer is full.


class TrAction(enum.IntEnum):
    """Trace: Action (ignored for collect data mode)."""
    TR_FETCH = 0     #: Trace information only at instruction Fetch.
    TR_ALL_CYCLE = 1 #: Trace information on all MCLK clocks.


class TrParameter(StructureWithEnums):
    """Trace parameter structure:
       The data structure contains the configuration settings of the EEM trace function.
    """
    _pack_ = 1
    _fields_ = [
        ("trControl", c_int),   #: Enable/disable/reset trace buffer (see enumerations of TR_Control).
        ("trMode", c_int),      #: Stores history, future, one snap shot or collect data on trigger (see enumerations of TR_Mode) (only if trControl = ST_ENABLE, else ignored).
        ("trAction", c_int),  #: Store on instruction fetch or on all cycles (see enumerations of TR_Action) (only trControl = ST_ENABLE and trMode != TR_COLLECT, else ignored).
    ]
    _map = {
        "trControl": TrControl, "trMode": TrMode, "trAction": TrAction
    }

#param = TrParameter(2,2,1)
#print(param.trControl, param.trMode, param.trAction)


class TraceBuffer(StructureWithEnums):
    """Trace buffer readout structure:
    The data structure is a copy of one position of the hardware trace buffer.
    They consist of data in a 40 bit buffer. The 40 bits are divided in 16 bit MAB,
    16 bit MDB and 8 bit control signals.
    """
    _pack_ = 1
    _fields_ = [
        ("lTrBufMAB", c_int32),     #: Trace buffer MAB.
        ("lTrBufMDB", c_int32),     #: Trace buffer MDB.
        ("wTrBufCNTRL", c_uint16),  #: Trace buffer control signals.
    ]


class VwEnable(enum.IntEnum):
    """Variable watch: Enable.
    """
    VW_ENABLE = 0   #: Enable the variable watch function.
    VW_DISABLE = 1  #: Disable the variable watch function.


class VwControl(enum.IntEnum):
    """Variable watch: Control.
    """
    VW_SET = 0      #: Set a variable to watch.
    VW_CLEAR = 1    #: Clear a watched variable.


class VwDataType(enum.IntEnum):
    """Variable watch: Data type of the variable (ignored for VW_CLEAR).
    """
    VW_8 = 0    #: Byte.
    VW_16 = 1   #: Word.
    VW_32 = 2   #: Long.


class VwParameter(StructureWithEnums):
    """Variable watch parameter structure:
    The data structure contains the settings of one variable.
    """
    _pack_ = 1
    _fields_ = [
        ("vwControl", c_int),   #: Set/clear variable.
        ("lAddr", c_uint32),    #: Address of the watched variable (ignored for VW_CLEAR).
        ("vwDataType", c_int),  #: Data type of the variable (ignored for VW_CLEAR).
    ]
    _map = {
        "vwControl": VwControl, "lAddr": c_uint32, "vwDataType": VwDataType
    }


class VwResources(StructureWithEnums):
    """Variable watch resource structure:
    The data structure contains the resources of one variable trigger.
    """
    _pack_ = 1
    _fields_ = [
        ("vwHandle", c_uint16), #: Handle of the variable trigger.
        ("lAddr", c_uint32),    #: Address of the watched variable.
        ("vwDataType", c_int),  #: Data type of the variable.
    ]
    _map = {
        "vwDataType": VwDataType
    }


class CcControl(enum.IntEnum):
    """Clock control: Extended emulation.
    """
    CC_DISABLE = 0  #: Disable.
    CC_ENABLE = 1   #: Enable.


class CcModule(enum.IntEnum):
    """Clock control: Clock for selected modules switch off (logic AND operation) (only for extended clock control, else ignored).
    """
    CC_ALLRUN           = 0         #: All module clocks are running on emualtion halt.
    CC_WDT              = (1 << 1)  #: Stop clock for Watch Dog Timer on emualtion halt.
    CC_TIMER_A          = (1 << 2)  #: Stop clock for TimerA on emualtion halt
    CC_TIMER_B          = (1 << 3)  #: Stop clock for TimerB on emualtion halt
    CC_BASIC_TIMER      = (1 << 4)  #: Stop clock for Basic Timer on emualtion halt.
    CC_LCD_FREQ         = (1 << 5)  #: Stop clock for LCD frequency on emualtion halt.
    CC_TIMER_COUNTER    = (1 << 6)  #: Stop clock for 8 bit Timer/Counter on emualtion halt.
    CC_TIMER_PORT       = (1 << 7)  #: Stop clock for Timer Port on emualtion halt.
    CC_USART0           = (1 << 8)  #: Stop clock for USART0 on emualtion halt.
    CC_USART1           = (1 << 9)  #: Stop clock for USART1 on emualtion halt.
    CC_FLASH_CNTRL      = (1 << 10) #: Stop clock for Flash Control on emualtion halt
    CC_ADC              = (1 << 11) #: Stop clock for ADC on emualtion halt.
    CC_ACLK             = (1 << 12) #: Stop ACLK on extern pin on emualtion halt.
    CC_SMCLK            = (1 << 13) #: Stop SMCLK on extern pin on emualtion halt.
    CC_MCLK             = (1 << 14) #: Stop MCLK on extern pin on emualtion halt.


class CcGeneralCLK(enum.IntEnum):
    """Clock control: Switch general clock off (logic AND operation)

    This function does influence the module clock control.
    If the general clock is not stop it could not be stopped at the module
    """
    CC_STP_NONE     = 0         #: All general clocks running on emulation halt.
    CC_STP_ACLK     = (1 << 1)  #: Stop ACLK on emulation halt.
    CC_STP_SMCLK    = (1 << 2)  #: Stop SMCLK on emulation halt.
    CC_STP_MCLK     = (1 << 3)  #: Stop MCLK on emulation halt (not for extended clock control).
    CC_STP_TACLK    = (1 << 5)  #: Stop TACLK on emulation halt (only for standard clock control).


class CcParameter(StructureWithEnums):
    """Clock control parameter structure:
    The data structure contains the settings of the clock control features.
    """
    _pack_ = 1
    _fields_ = [
        ("ccControl", c_int),   #: Extended emulation clock control (enable/disable clock control).
        ("ccModule", c_uint16),     #: Switch clock for modules off (1 bit per clock module, 1: stop clock module while CPU halted).
        ("ccGeneralCLK", c_uint16), #: Switch general clock off (1 bit per clock, 1: stop clock while CPU halted).
    ]
    _map = {
        "ccControl": CcControl
    }


class SeqControl(enum.IntEnum):
    """Sequencer: Control.
    """
    SEQ_DISABLE = 0 #: Disable sequencer state machine.
    SEQ_ENABLE = 1  #: Enable sequencer state machine.


class SeqState(enum.IntEnum):
    """Sequencer: Select next state when selected trigger occurs.
    """
    SEQ_STATE0 = 0  #: Switch in state 0.
    SEQ_STATE1 = 1  #: Switch in state 1.
    SEQ_STATE2 = 2  #: Switch in state 2.
    SEQ_STATE3 = 3  #: Switch in state 3.


class SeqParameter(StructureWithEnums):
    """Sequencer parameter structure:
    The data structure contains the configuration settings of the sequencer.
    To select no trigger provide zero as handle.
    """
    _pack_ = 1
    _fields_ = [
        ("seqControl", c_int),                          #: Trigger sequencer Control (enable/disable).
        ("wHandleRstTrig", c_uint16),                   #: Select breakpoint as a reset trigger to set start state 0 (0 = off).
        ("bpAction", c_int),                            #: Select action on entering final state.
        ("seqNextStateX", c_int * MAX_SEQ_STATE),       #: Select next state x that followed of state X.
        ("wHandleStateX", c_uint16 * MAX_SEQ_STATE),    #: Select breakpoint as a trigger for switching from state x into next state: x path.
        ("seqNextStateY", c_int * MAX_SEQ_STATE),       #: Select next state y that followed of state X.
        ("wHandleStateY", c_uint16 * MAX_SEQ_STATE),    #: Select breakpoint as a trigger for switching from state x into next state: y path.
    ]
    _map = {
        "seqControl": SeqControl, "bpAction": BpAction, "seqNextStateX": SeqState, "seqNextStateY": SeqState
    }


class CycleCounterMode(enum.IntEnum):
    """Cycle counter operation mode.
    """
    CYC_MODE_BASIC = 0x0    #: Basic mode (default): counter 0 is reserved for legacy behavior.
    CYC_MODE_ADVANCED = 0x1 #: Advanced mode: counter 0 is available for manual configuration.


class CycleCounterCountMode(enum.IntEnum):
    """Cycle counter count mode.
    """
    CYC_COUNT_STOPPED = 0x0     #: Counter is stopped.
    CYC_COUNT_ON_REACTION = 0x1 #: Count on cycle counter trigger reaction (only counter 1).
    CYC_COUNT_ON_IFCLK = 0x2    #: Count on all IFCLKs (used and unused by CPU or DMA).
    CYC_COUNT_ON_FETCH = 0x4    #: Count on instruction fetch.
    CYC_COUNT_ON_ALL_BUS = 0x5  #: Count on all bus cycles (CPU or DMA).
    CYC_COUNT_ON_CPU_BUS = 0x6  #: Count on CPU bus cycles.
    CYC_COUNT_ON_DMA_BUS = 0x7  #: Count on DMA bus cycles.


class CycleCounterCountMode(enum.IntEnum):
    """Cycle counter count mode.
    """
    CYC_COUNT_STOPPED = 0x0     #: Counter is stopped.
    CYC_COUNT_ON_REACTION = 0x1 #: Count on cycle counter trigger reaction (only counter 1).
    CYC_COUNT_ON_IFCLK = 0x2    #: Count on all IFCLKs (used and unused by CPU or DMA).
    CYC_COUNT_ON_FETCH = 0x4    #: Count on instruction fetch.
    CYC_COUNT_ON_ALL_BUS = 0x5  #: Count on all bus cycles (CPU or DMA).
    CYC_COUNT_ON_CPU_BUS = 0x6  #: Count on CPU bus cycles
    CYC_COUNT_ON_DMA_BUS = 0x7  #: Count on DMA bus cycles.


class CycleCounterStartMode(enum.IntEnum):
    """Cycle counter start mode.
    """
    CYC_START_ON_RELEASE = 0x0  #: Start counter when released from debug halt.
    CYC_START_ON_REACTION = 0x1 #: Start counter on counter trigger reaction (only counter 1).
    CYC_START_ON_COUNTER = 0x2  #: Start when other counter starts (only targets with 2 counters).
    CYC_START_IMMEDIATELY = 0x3 #: Start counter immediately.


class CycleCounterStopMode(enum.IntEnum):
    """Cycle counter stop mode.
    """
    CYC_STOP_ON_DBG_HALT = 0x0  #: Stop counter on debug halt.
    CYC_STOP_ON_REACTION = 0x1  #: Stop counter on counter trigger reaction (only counter 1).
    CYC_STOP_ON_COUNTER = 0x2   #: Stop counter when other counter stops (only targets with 2 counters).
    CYC_STOP_NO_EVENT = 0x3     #: Never stop counter.


class CycleCounterClearMode(enum.IntEnum):
    """Cycler counter clear mode.
    """
    CYC_CLEAR_NO_EVENT = 0x0    #: Never automatically reset counter.
    CYC_CLEAR_ON_REACTION = 0x1 #: Reset counter on counter trigger reaction (only counter 1).
    CYC_CLEAR_ON_COUNTER = 0x2  #: Reset counter when other counter automatically resets (only targets with 2 counters).


class CycleCounterConfig(StructureWithEnums):
    """Cycle counter parameter structure:
    The data structure contains the configuration settings for a cycle counter.
    """
    _pack_ = 1
    _fields_ = [
        ("countMode", c_int),   # : Condition to increase counter.
        ("startMode", c_int),   #: Condition to start counter.
        ("stopMode", c_int),    #: Condition to stop counter.
        ("clearMode", c_int),   #: Condition to clear/reset counter.
    ]
    _map = {
        "countMode": CycleCounterCountMode, "startMode": CycleCounterStartMode,
        "stopMode": CycleCounterStopMode, "clearMode": CycleCounterClearMode
    }


"""/**
\brief   Type definition for a callback function which must be available
         in the application which calls the MSP430.dll. The callback function
                 handles notify events which are sent from the DLL to the calling application.
                 A handle to the callback function is passed to the DLL by calling
                 MSP430_EEM_Init().
*/
typedef void (* MSP430_EVENTNOTIFY_FUNC) (uint32_t MsgId, uint32_t wParam, int32_t lParam, int32_t clientHandle);
"""
Msp430EventnotifyFunc = WINFUNCTYPE(None, c_uint32, c_uint32, c_int32, c_int32)


class EMMAPI(API):

    FUNCTIONS = (
        ("MSP430_EEM_Init", STATUS_T, [Msp430EventnotifyFunc, c_int32, POINTER(MessageIdType)]),
        ("MSP430_EEM_SetBreakpoint", STATUS_T, [POINTER(c_uint16), POINTER(BpParameter)]),
        ("MSP430_EEM_GetBreakpoint", STATUS_T, [c_uint16, POINTER(BpParameter)]),
        ("MSP430_EEM_SetCombineBreakpoint", STATUS_T, [c_int, c_uint16, POINTER(c_uint16), POINTER(c_uint16)]),
        ("MSP430_EEM_GetCombineBreakpoint", STATUS_T, [c_uint16, POINTER(c_uint16), POINTER(c_uint16)]),
        ("MSP430_EEM_SetTrace", STATUS_T, [POINTER(TrParameter)]),
        ("MSP430_EEM_GetTrace", STATUS_T, [POINTER(TrParameter)]),
        ("MSP430_EEM_ReadTraceBuffer", STATUS_T, [POINTER(TraceBuffer)]),
        ("MSP430_EEM_ReadTraceData", STATUS_T, [POINTER(TraceBuffer), POINTER(c_uint32)]),
        ("MSP430_EEM_RefreshTraceBuffer", STATUS_T, []),
        ("MSP430_EEM_SetVariableWatch", STATUS_T, [c_int]),
        ("MSP430_EEM_SetVariable", STATUS_T, [POINTER(c_uint16), POINTER(VwParameter)]),
        ("MSP430_EEM_GetVariableWatch", STATUS_T, [POINTER(c_int), POINTER(VwResources)]),
        ("MSP430_EEM_SetClockControl", STATUS_T, [POINTER(CcParameter)]),
        ("MSP430_EEM_GetClockControl", STATUS_T, [POINTER(CcParameter)]),
        ("MSP430_EEM_SetSequencer", STATUS_T, [POINTER(SeqParameter)]),
        ("MSP430_EEM_GetSequencer", STATUS_T, [POINTER(SeqParameter)]),
        ("MSP430_EEM_ReadSequencerState", STATUS_T, [POINTER(c_int)]),
        ("MSP430_EEM_SetCycleCounterMode", STATUS_T, [c_int]),
        ("MSP430_EEM_ConfigureCycleCounter", STATUS_T, [c_uint32, CycleCounterConfig]),
        ("MSP430_EEM_ReadCycleCounterValue", STATUS_T, [c_uint32, POINTER(c_uint64)]),
        ("MSP430_EEM_WriteCycleCounterValue", STATUS_T, [c_uint32, c_uint64]),
        ("MSP430_EEM_ResetCycleCounter", STATUS_T, [c_uint32]),
    )

    def init(self, callback, clientHandle, parameters):
        pref = byref(parameters)
        self.MSP430_EEM_Init(Msp430EventnotifyFunc(callback), clientHandle, pref)

    def setBreakpoint(self, parameter):
        pref = byref(parameter)
        handle = c_uint16()
        self.MSP430_EEM_SetBreakpoint(byref(handle), pref)
        return handle.value

    def getBreakpoint(self, handle):
        param = BpParameter()
        self.MSP430_EEM_GetBreakpoint(handle, byref(param))
        return param

    def setCombineBreakpoint(self, control, count, combinationHandles):
        handle = c_uint16()
        self.MSP430_EEM_SetCombineBreakpoint(control, count, byref(handle), byref(combinationHandles))
        return handle

    def getCombineBreakpoint(self, handle):
        count = c_uint16()
        bpHandles = c_uint16()
        self.MSP430_EEM_GetCombineBreakpoint(handle, byref(count), byref(bpHandles))
        return (count, bpHandles)

    def setTrace(self, parameter):
        self.MSP430_EEM_SetTrace(byref(parameter))

    def getTrace(self):
        destBuff = TrParameter()
        self.MSP430_EEM_GetTrace(byref(destBuff))
        return destBuff

    def readTraceBuffer(self):
        buffer = TraceBuffer()
        self.MSP430_EEM_ReadTraceBuffer(byref(buffer))
        return buffer

    def readTraceData(self):
        buffer = TraceBuffer()
        pulCount = c_uint32(1)
        self.MSP430_EEM_ReadTraceData(byref(buffer), byref(pulCount))
        return (buffer, pulCount)

    def refreshTraceBuffer(self):
        self.MSP430_EEM_RefreshTraceBuffer()

    def setVariableWatch(self, ena):
        self.MSP430_EEM_SetVariableWatch(ena)

    def setVariable(self, handle, buffer):
        self.MSP430_EEM_SetVariable(byref(handle), byref(buffer))

    def getVariableWatch(self):
        ena = VwEnable()
        resource = VwResources()
        self.MSP430_EEM_GetVariableWatch(byref(ena), byref(resource))
        return (ena, resource)

    def setClockControl(self, parameter):
        self.MSP430_EEM_SetClockControl(byref(parameter))

    def getClockControl(self):
        parameter = CcParameter()
        self.MSP430_EEM_SetClockControl(byref(parameter))
        return parameter

    def setSequencer(self, parameter):
        self.MSP430_EEM_SetSequencer(byref(parameter))

    def getSequencer(self):
        parameter = SeqParameter()
        self.MSP430_EEM_GetSequencer(byref(parameter))
        return paramter

    def readSequencerState(self):
        state = c_int()
        self.MSP430_EEM_ReadSequencerState(byref(state))
        return SeqState(state)

    def setCycleCounterMode(self, mode):
        self.MSP430_EEM_SetCycleCounterMode(mode)

    def configureCycleCounter(self, counter, config):
        self.MSP430_EEM_ConfigureCycleCounter(counter, config)

    def readCycleCounterValue(self, counter):
        value = c_uint64
        self.MSP430_EEM_ReadCycleCounterValue(counter, byref(value))
        return value

    def writeCycleCounterValue(self, counter, value):
        self.MSP430_EEM_WriteCycleCounterValue(counter, value)

    def resetCycleCounter(self, counter):
        self.MSP430_EEM_ResetCycleCounter(counter)

