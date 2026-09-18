import ctypes
import threading
from collections import deque
from collections.abc import Callable, Iterator

from mido import Message

from midi.interface import MidiDeviceProvider, MidiInput, MidiOutput

UINT = ctypes.c_uint
DWORD = ctypes.c_uint32
WORD = ctypes.c_uint16
DWORD_PTR = ctypes.c_size_t
MMRESULT = UINT
HMIDIIN = ctypes.c_void_p
HMIDIOUT = ctypes.c_void_p

CALLBACK_FUNCTION = 0x00030000
MIM_DATA = 0x3C3
MIM_LONGDATA = 0x3C4
MMSYSERR_NOERROR = 0

class MIDIINCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", WORD),
        ("wPid", WORD),
        ("vDriverVersion", DWORD),
        ("szPname", ctypes.c_wchar * 32),
        ("dwSupport", DWORD),
    ]

class MIDIOUTCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", WORD),
        ("wPid", WORD),
        ("vDriverVersion", DWORD),
        ("szPname", ctypes.c_wchar * 32),
        ("wTechnology", WORD),
        ("wVoices", WORD),
        ("wNotes", WORD),
        ("wChannelMask", WORD),
        ("dwSupport", DWORD),
    ]

MIDI_CALLBACK = ctypes.WINFUNCTYPE(
    None,
    HMIDIIN,
    UINT,
    DWORD_PTR,
    DWORD_PTR,
    DWORD_PTR,
)

winmm = ctypes.WinDLL("winmm")

winmm.midiInGetNumDevs.argtypes = []
winmm.midiInGetNumDevs.restype = UINT

winmm.midiOutGetNumDevs.argtypes = []
winmm.midiOutGetNumDevs.restype = UINT

winmm.midiInGetDevCapsW.argtypes = [
    UINT,
    ctypes.POINTER(MIDIINCAPSW),
    UINT,
]
winmm.midiInGetDevCapsW.restype = MMRESULT

winmm.midiOutGetDevCapsW.argtypes = [
    UINT,
    ctypes.POINTER(MIDIOUTCAPSW),
    UINT,
]
winmm.midiOutGetDevCapsW.restype = MMRESULT

winmm.midiInOpen.argtypes = [
    ctypes.POINTER(HMIDIIN),
    UINT,
    DWORD_PTR,
    DWORD_PTR,
    DWORD,
]
winmm.midiInOpen.restype = MMRESULT

winmm.midiInStart.argtypes = [
    HMIDIIN,
]
winmm.midiInStart.restype = MMRESULT

winmm.midiInStop.argtypes = [
    HMIDIIN,
]
winmm.midiInStop.restype = MMRESULT

winmm.midiInReset.argtypes = [
    HMIDIIN,
]
winmm.midiInReset.restype = MMRESULT

winmm.midiInClose.argtypes = [
    HMIDIIN,
]
winmm.midiInClose.restype = MMRESULT

winmm.midiOutOpen.argtypes = [
    ctypes.POINTER(HMIDIOUT),
    UINT,
    DWORD_PTR,
    DWORD,
    DWORD,
]
winmm.midiOutOpen.restype = MMRESULT

winmm.midiOutShortMsg.argtypes = [
    HMIDIOUT,
    DWORD,
]
winmm.midiOutShortMsg.restype = MMRESULT

winmm.midiOutClose.argtypes = [
    HMIDIOUT,
]
winmm.midiOutClose.restype = MMRESULT


class WindowsMidiInput(MidiInput):
    def __init__(
        self,
        device_id: int,
        callback: Callable[[Message], None] | None = None,
    ) -> None:
        self._device_id = device_id
        self._callback = callback
        self._handle = HMIDIIN()
        self._messages: deque[Message] = deque()
        self._condition = threading.Condition()
        self._callback_ref = MIDI_CALLBACK(self.__midi_callback)
        self._opened = False

    def open(self) -> None:
        if self._opened:
            return

        callback_address = ctypes.cast(
            self._callback_ref,
            ctypes.c_void_p,
        ).value

        result = winmm.midiInOpen(
            ctypes.byref(self._handle),
            self._device_id,
            callback_address,
            0,
            CALLBACK_FUNCTION,
        )

        self._check_result(
            result,
            "midiInOpen",
        )

        result = winmm.midiInStart(
            self._handle,
        )

        if result != MMSYSERR_NOERROR:
            winmm.midiInClose(
                self._handle,
            )

            self._handle = HMIDIIN()

            self._check_result(
                result,
                "midiInStart",
            )

        self._opened = True

    def close(self) -> None:
        if not self._opened:
            return

        winmm.midiInStop(
            self._handle,
        )

        winmm.midiInReset(
            self._handle,
        )

        winmm.midiInClose(
            self._handle,
        )

        self._handle = HMIDIIN()
        self._opened = False

        with self._condition:
            self._condition.notify_all()

    def messages(self) -> Iterator[Message]:
        while self._opened:
            with self._condition:
                while not self._messages and self._opened:
                    self._condition.wait(
                        timeout=0.1,
                    )

                while self._messages:
                    yield self._messages.popleft()

    def is_open(self) -> bool:
        return self._opened

    def __midi_callback(
        self,
        handle: HMIDIIN,
        message: UINT,
        instance: DWORD_PTR,
        param1: DWORD_PTR,
        param2: DWORD_PTR,
    ) -> None:
        message_code = int(message)
        parameter_1 = int(param1)

        if message_code == MIM_DATA:
            midi_message = self.__decode_short_message(
                parameter_1,
            )

            if midi_message is not None:
                self.__dispatch_message(
                    midi_message,
                )

            return

        if message_code == MIM_LONGDATA:
            return

    def __dispatch_message(
        self,
        message: Message,
    ) -> None:
        if self._callback is not None:
            self._callback(message)

        with self._condition:
            self._messages.append(message)
            self._condition.notify()

    @staticmethod
    def __decode_short_message(
        packed_message: int,
    ) -> Message | None:
        status = packed_message & 0xFF
        data1 = (packed_message >> 8) & 0xFF
        data2 = (packed_message >> 16) & 0xFF

        if status >= 0xF8:
            system_messages = {
                0xF8: "clock",
                0xFA: "start",
                0xFB: "continue",
                0xFC: "stop",
                0xFE: "active_sensing",
                0xFF: "reset",
            }

            message_type = system_messages.get(status)

            if message_type is None:
                return None

            return Message(
                message_type,
            )

        status_type = status & 0xF0
        channel = status & 0x0F

        if status_type == 0x80:
            return Message(
                "note_off",
                channel=channel,
                note=data1,
                velocity=data2,
            )

        if status_type == 0x90:
            return Message(
                "note_on",
                channel=channel,
                note=data1,
                velocity=data2,
            )

        if status_type == 0xA0:
            return Message(
                "polytouch",
                channel=channel,
                note=data1,
                value=data2,
            )

        if status_type == 0xB0:
            return Message(
                "control_change",
                channel=channel,
                control=data1,
                value=data2,
            )

        if status_type == 0xC0:
            return Message(
                "program_change",
                channel=channel,
                program=data1,
            )

        if status_type == 0xD0:
            return Message(
                "aftertouch",
                channel=channel,
                value=data1,
            )

        if status_type == 0xE0:
            pitch = data1 | (data2 << 7)
            pitch -= 8192

            return Message(
                "pitchwheel",
                channel=channel,
                pitch=pitch,
            )

        return None

    @staticmethod
    def _check_result(
        result: MMRESULT,
        operation: str,
    ) -> None:
        if result != MMSYSERR_NOERROR:
            raise RuntimeError(
                f"{operation} failed with error code {result}"
            )


class WindowsMidiOutput(MidiOutput):
    def __init__(
        self,
        device_id: int,
    ) -> None:
        self._device_id = device_id
        self._handle = HMIDIOUT()
        self._opened = False

    def open(self) -> None:
        if self._opened:
            return

        result = winmm.midiOutOpen(
            ctypes.byref(self._handle),
            self._device_id,
            0,
            0,
            0,
        )

        if result != MMSYSERR_NOERROR:
            raise RuntimeError(
                f"midiOutOpen failed with error code {result}"
            )

        self._opened = True

    def close(self) -> None:
        if not self._opened:
            return

        winmm.midiOutClose(
            self._handle,
        )

        self._handle = HMIDIOUT()
        self._opened = False

    def send(
        self,
        message: Message,
    ) -> None:
        if not self._opened:
            raise RuntimeError(
                "MIDI output is not open."
            )

        if message.type == "sysex":
            raise NotImplementedError(
                "SysEx output is not implemented yet."
            )

        data = message.bytes()

        packed_message = 0

        for index, value in enumerate(data):
            packed_message |= value << (index * 8)

        result = winmm.midiOutShortMsg(
            self._handle,
            packed_message,
        )

        if result != MMSYSERR_NOERROR:
            raise RuntimeError(
                f"midiOutShortMsg failed with error code {result}"
            )

    def is_open(self) -> bool:
        return self._opened


class WindowsMidiDeviceProvider(MidiDeviceProvider):
    def input_ports(self) -> list[str]:
        count = winmm.midiInGetNumDevs()

        ports = []

        for device_id in range(count):
            caps = MIDIINCAPSW()

            result = winmm.midiInGetDevCapsW(
                device_id,
                ctypes.byref(caps),
                ctypes.sizeof(caps),
            )

            if result == MMSYSERR_NOERROR:
                ports.append(caps.szPname)

        return ports

    def output_ports(self) -> list[str]:
        count = winmm.midiOutGetNumDevs()

        ports = []

        for device_id in range(count):
            caps = MIDIOUTCAPSW()

            result = winmm.midiOutGetDevCapsW(
                device_id,
                ctypes.byref(caps),
                ctypes.sizeof(caps),
            )

            if result == MMSYSERR_NOERROR:
                ports.append(caps.szPname)

        return ports

    def create_input(
        self,
        port_name: str,
        callback: Callable[[Message], None] | None = None,
    ) -> MidiInput:
        device_id = self._find_input_device(
            port_name,
        )

        return WindowsMidiInput(
            device_id,
            callback,
        )

    def create_output(
        self,
        port_name: str,
    ) -> MidiOutput:
        device_id = self._find_output_device(
            port_name,
        )

        return WindowsMidiOutput(
            device_id,
        )

    def _find_input_device(
        self,
        port_name: str,
    ) -> int:
        count = winmm.midiInGetNumDevs()

        for device_id in range(count):
            caps = MIDIINCAPSW()

            result = winmm.midiInGetDevCapsW(
                device_id,
                ctypes.byref(caps),
                ctypes.sizeof(caps),
            )

            if (
                result == MMSYSERR_NOERROR
                and caps.szPname == port_name
            ):
                return device_id

        raise ValueError(
            f"MIDI input not found: {port_name}"
        )

    def _find_output_device(
        self,
        port_name: str,
    ) -> int:
        count = winmm.midiOutGetNumDevs()

        for device_id in range(count):
            caps = MIDIOUTCAPSW()

            result = winmm.midiOutGetDevCapsW(
                device_id,
                ctypes.byref(caps),
                ctypes.sizeof(caps),
            )

            if (
                result == MMSYSERR_NOERROR
                and caps.szPname == port_name
            ):
                return device_id

        raise ValueError(
            f"MIDI output not found: {port_name}"
        )