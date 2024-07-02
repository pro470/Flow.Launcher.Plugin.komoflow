import json
import logging
import time
import os
import ctypes
import ctypes.wintypes
from pyflowlauncher import Result, string_matcher
from typing import Iterable, Generator, Optional

# Constants
PIPE_ACCESS_DUPLEX = 0x00000003
PIPE_TYPE_MESSAGE = 0x00000004
PIPE_READMODE_MESSAGE = 0x00000002
PIPE_WAIT = 0x00000000
INVALID_HANDLE_VALUE = -1
FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3

# Functions from kernel32.dll
CreateNamedPipe = ctypes.WinDLL('kernel32', use_last_error=True).CreateNamedPipeW
ConnectNamedPipe = ctypes.WinDLL('kernel32', use_last_error=True).ConnectNamedPipe
ReadFile = ctypes.WinDLL('kernel32', use_last_error=True).ReadFile
WriteFile = ctypes.WinDLL('kernel32', use_last_error=True).WriteFile
CloseHandle = ctypes.WinDLL('kernel32', use_last_error=True).CloseHandle
CreateFile = ctypes.WinDLL('kernel32', use_last_error=True).CreateFileW
DisconnectNamedPipe = ctypes.WinDLL('kernel32', use_last_error=True).DisconnectNamedPipe

# Error handling
GetLastError = ctypes.WinDLL('kernel32', use_last_error=True).GetLastError

BUFFER_SIZE = 1024 * 64


def create_named_pipe(pipename):
    pipe = CreateNamedPipe(
        rf'\\.\pipe\{pipename}',
        PIPE_ACCESS_DUPLEX | FILE_FLAG_FIRST_PIPE_INSTANCE,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        1, 65536, 65536, 0, None
    )

    if pipe == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())

    return pipe


def connect_komorebi(wkomorebic, pipename) -> None:
    wkomorebic.subscribe_pipe(pipename)


def exit_komoflow(wkomorebic, pipe, pipename) -> None:
    wkomorebic.unsubscribe_pipe(pipename)
    DisconnectNamedPipe(pipe)
    CloseHandle(pipe)


def state(pipe):
    # read komorebi event
    try:
        while True:

            buffer = ctypes.create_string_buffer(64 * 1024)
            bytes_read = ctypes.wintypes.DWORD()
            success = ReadFile(pipe, buffer, len(buffer), ctypes.byref(bytes_read), None)
            if success or bytes_read.value != 0:
                break
            else:
                time.sleep(0.1)

        message = buffer.value.decode('utf-8')

        event = json.loads(message)
        # event = json.loads(data)
        # print(json.dumps(event, indent=4))

        event_state = event['state']

        return event_state

    except (BaseException, Exception):
        DisconnectNamedPipe(pipe)
        CloseHandle(pipe)


def score_resluts_with_sub(query: str, results: Iterable[Result]) -> Generator[Result, None, None]:
    for result in results:
        match = string_matcher.string_matcher(
            query,
            result.Title,
            query_search_precision=string_matcher.DEFAULT_QUERY_SEARCH_PRECISION
        )
        if match.matched or (True and not query):
            result.TitleHighlightData = match.index_list
            result.Score = match.score
            yield result

        if result.Score == 0:
            text = result.SubTitle
            text.replace('EXE:', '')
            text.replace('HWND:', '')
            text.replace('.exe', '')

            match = string_matcher.string_matcher(
                query,
                text,
                query_search_precision=string_matcher.REGULAR_SEARCH_PRECISION
            )
            if match.matched or (False and not query):
                result.Score = match.score
                yield result


def get_first_word(s: str):
    words = s.split()
    if words:
        return words[0]
    return None
