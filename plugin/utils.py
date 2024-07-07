import json
import logging
import subprocess
import struct
import time
import os
import ctypes
from ctypes import wintypes
from pyflowlauncher import Result, string_matcher
from typing import Iterable, Generator, Optional
from komorebic_client import WKomorebic
from ctypes import Array, byref, c_char, memset, sizeof
from ctypes import c_int, c_void_p, POINTER
from ctypes.wintypes import *
from enum import Enum
import struct
import zlib

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
user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
shell32 = ctypes.WinDLL("shell32", use_last_error=True)

# Error handling
GetLastError = ctypes.WinDLL('kernel32', use_last_error=True).GetLastError

BUFFER_SIZE = 1024 * 64


# Define necessary Windows structures and constants
class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", wintypes.HBITMAP),
        ("hbmColor", wintypes.HBITMAP),
    ]


class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", wintypes.LONG),
        ("bmWidth", wintypes.LONG),
        ("bmHeight", wintypes.LONG),
        ("bmWidthBytes", wintypes.LONG),
        ("bmPlanes", wintypes.WORD),
        ("bmBitsPixel", wintypes.WORD),
        ("bmBits", ctypes.c_void_p),
    ]


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


def connect_komorebi(wkomorebic: WKomorebic, pipename) -> None:
    wkomorebic.subscribe_pipe(pipename)


def exit_komoflow(wkomorebic: WKomorebic, pipe, pipename) -> None:
    wkomorebic.unsubscribe_pipe(pipename)
    DisconnectNamedPipe(pipe)
    CloseHandle(pipe)


def state(pipe):
    # read komorebi event
    try:
        tries = 0
        buffer = None
        while True:
            if tries == 5:
                break

            tries = tries + 1
            buffer = ctypes.create_string_buffer(64 * 1024)
            bytes_read = wintypes.DWORD()
            success = ReadFile(pipe, buffer, len(buffer), ctypes.byref(bytes_read), None)
            if success or bytes_read.value != 0:
                break
            else:
                time.sleep(0.1)

        if buffer:
            message = buffer.value.decode('utf-8')

            event = json.loads(message)
            # event = json.loads(data)
            # print(json.dumps(event, indent=4))

            event_state = event['state']
        else:
            return None

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
            text.replace(', HWND:', '')
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


def check_process_running(process_name):
    """
    Check if a process with the given name is running on Windows.
    """
    try:
        # Use tasklist to list all running processes without opening a shell window
        result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output = result.stdout.strip()

        # Check if the process_name is in the tasklist output
        if process_name.lower() in output.lower():
            return True
        else:
            return False
    except Exception:
        return False


def find_files_in_user_directory(filename="komorebi.json"):
    """
    Searches for all instances of the specified file in the current user's home directory and its subdirectories.

    Args:
    - filename (str): The name of the file to search for. Default is "komorebi.json".

    Returns:
    - list of str: A list of full paths to each found file.
    """
    matches = []
    user_home_dir = os.path.expanduser("~")

    def scan_directory(directory):
        try:
            with os.scandir(directory) as it:
                for entry in it:
                    if entry.is_file() and entry.name == filename:
                        matches.append(entry.path)
                    elif entry.is_dir():
                        scan_directory(entry.path)
        except PermissionError:
            # Skip directories that cannot be accessed
            pass

    scan_directory(user_home_dir)
    return matches


def word_before_last_bracket(text):
    # Find the last occurrence of '['
    last_bracket_index = text.rfind('[')

    # If no '[' found, return None or an appropriate message
    if last_bracket_index == -1:
        return None

    # Extract the substring after the last '['
    substring_after_bracket = text[last_bracket_index + 1:]

    # Check if the substring contains ']'
    if ']' in substring_after_bracket:
        return None

    # Extract the substring before the last '['
    substring_before_bracket = text[:last_bracket_index]

    # Split the substring into words
    words = substring_before_bracket.split()

    # Return the last word in the split list
    return words[-1] if words else None


def append_if_matches(input_string: str, word_to_check: str, stop_words: [str]) -> str:
    words = input_string.split()
    if not words:
        return input_string  # If input_string is empty or only whitespace, return as is

    last_word = words[-1]
    it = iter(word_to_check)
    if all(char in it for char in last_word.lower()):
        # Remove the last word from the input string
        new_string = None

        # Traverse the words from the end
        for i in range(len(words) - 1, -1, -1):
            word = words[i]

            # Check if the current word is in the stop words list or contains a closing square bracket
            for stop_word in stop_words:
                if stop_word == word or ']' in word:
                    # Join the remaining words to form the substring from this point onwards
                    new_string = ' '.join(words[:i + 1])

                    return f"{new_string.strip()} {word_to_check}".strip()
        # Append word_to_check to the new string
        if new_string is None:
            # Remove the last word from the input string
            new_string = ' '.join(words[:-1])
            # Append word_to_check to the new string
            return f"{new_string} {word_to_check}".strip()
    elif word_to_check.startswith(last_word):
        # Find the part of word_to_check that is not in last_word
        remaining_part = word_to_check[len(last_word):]
        # Append the remaining part to the input string
        return input_string + remaining_part
    else:
        if input_string.endswith(" "):
            return input_string + word_to_check
        else:
            return input_string + " " + word_to_check


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * 260)
    ]


TH32CS_SNAPPROCESS = 0x00000002
INVALID_HANDLE_VALUE1 = ctypes.c_void_p(-1).value

BI_RGB = 0
DIB_RGB_COLORS = 0


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ("fIcon", BOOL),
        ("xHotspot", DWORD),
        ("yHotspot", DWORD),
        ("hbmMask", HBITMAP),
        ("hbmColor", HBITMAP)
    ]


class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ("rgbBlue", BYTE),
        ("rgbGreen", BYTE),
        ("rgbRed", BYTE),
        ("rgbReserved", BYTE),
    ]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD)
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1),
    ]


gdi32.CreateCompatibleDC.argtypes = [HDC]
gdi32.CreateCompatibleDC.restype = HDC
gdi32.GetDIBits.argtypes = [
    HDC, HBITMAP, UINT, UINT, LPVOID, c_void_p, UINT
]
gdi32.GetDIBits.restype = c_int
gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DeleteObject.restype = BOOL
shell32.ExtractIconExW.argtypes = [
    LPCWSTR, c_int, POINTER(HICON), POINTER(HICON), UINT
]
shell32.ExtractIconExW.restype = UINT
user32.GetIconInfo.argtypes = [HICON, POINTER(ICONINFO)]
user32.GetIconInfo.restype = BOOL
user32.DestroyIcon.argtypes = [HICON]
user32.DestroyIcon.restype = BOOL


class IconSize(Enum):
    SMALL = 1
    LARGE = 2

    @staticmethod
    def to_wh(size: "IconSize") -> tuple[int, int]:
        """
        Return the actual (width, height) values for the specified icon size.
        """
        size_table = {
            IconSize.SMALL: (16, 16),
            IconSize.LARGE: (32, 32)
        }
        return size_table[size]


def extract_icon(filename: str, size: IconSize) -> Array[c_char]:
    """
    Extract the icon from the specified `filename`, which might be
    either an executable or an `.ico` file.
    """
    dc: HDC = gdi32.CreateCompatibleDC(0)
    if dc == 0:
        raise ctypes.WinError()

    hicon: HICON = HICON()
    extracted_icons: UINT = shell32.ExtractIconExW(
        filename,
        0,
        byref(hicon) if size == IconSize.LARGE else None,
        byref(hicon) if size == IconSize.SMALL else None,
        1
    )
    if extracted_icons != 1:
        raise ctypes.WinError()

    def cleanup() -> None:
        if icon_info.hbmColor != 0:
            gdi32.DeleteObject(icon_info.hbmColor)
        if icon_info.hbmMask != 0:
            gdi32.DeleteObject(icon_info.hbmMask)
        user32.DestroyIcon(hicon)

    icon_info: ICONINFO = ICONINFO(0, 0, 0, 0, 0)
    if not user32.GetIconInfo(hicon, byref(icon_info)):
        cleanup()
        raise ctypes.WinError()

    w, h = IconSize.to_wh(size)
    bmi: BITMAPINFO = BITMAPINFO()
    memset(byref(bmi), 0, sizeof(bmi))
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bmi.bmiHeader.biSizeImage = w * h * 4
    bits = ctypes.create_string_buffer(bmi.bmiHeader.biSizeImage)
    copied_lines = gdi32.GetDIBits(
        dc, icon_info.hbmColor, 0, h, bits, byref(bmi), DIB_RGB_COLORS
    )
    if copied_lines == 0:
        cleanup()
        raise ctypes.WinError()

    cleanup()
    return bits


def enumerate_processes():
    process_list = []
    hProcessSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if hProcessSnap == INVALID_HANDLE_VALUE1:
        raise ctypes.WinError()

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

    if not kernel32.Process32First(hProcessSnap, ctypes.byref(pe32)):
        kernel32.CloseHandle(hProcessSnap)
        raise ctypes.WinError()

    while True:
        process_list.append((pe32.th32ProcessID, pe32.szExeFile.decode('utf-8')))
        if not kernel32.Process32Next(hProcessSnap, ctypes.byref(pe32)):
            break

    kernel32.CloseHandle(hProcessSnap)
    return process_list


def get_exe_path_from_pid(pid):
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    hProcess = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not hProcess:
        return None

    exe_path = (ctypes.c_wchar * 260)()
    size = DWORD(260)
    if kernel32.QueryFullProcessImageNameW(hProcess, 0, exe_path, ctypes.byref(size)):
        kernel32.CloseHandle(hProcess)
        return exe_path.value
    else:
        kernel32.CloseHandle(hProcess)
        return None


def extract_icon_from_running_process(process_name):
    for pid, exe in enumerate_processes():
        if exe.lower() == process_name.lower():
            exe_path = get_exe_path_from_pid(pid)
            if exe_path:
                try:
                    return extract_icon(exe_path, IconSize.LARGE)
                except FileNotFoundError:
                    try:
                        return extract_icon(exe_path, IconSize.SMALL)
                    except FileNotFoundError:
                        return None

    #raise ValueError(f"Process {process_name} not found.")


def save_icon_as_ico(icon_bytes, icon_path, width, height):
    with open(icon_path, 'wb') as f:
        # ICO header
        f.write(struct.pack('<3H', 0, 1, 1))
        # ICO directory entry
        f.write(struct.pack('<BBHHHI', width, height, 0, 0, 1, 32))
        # Offset to the image data
        f.write(struct.pack('<I', 22))
        # BITMAPINFOHEADER
        f.write(struct.pack('<IiiHHIIIIII',
                            40, width, height * 2, 1, 32, BI_RGB, len(icon_bytes), 0, 0, 0, 0))
        # Bitmap data
        f.write(icon_bytes)


def save_icon_as_png(icon_bytes, icon_path, width, height):
    def png_chunk(chunk_type, data):
        chunk_len = len(data)
        chunk = struct.pack('>I', chunk_len) + chunk_type + data
        crc = zlib.crc32(chunk_type + data) & 0xffffffff
        chunk += struct.pack('>I', crc)
        return chunk

    # Convert BGRA to RGBA
    rgba_bytes = bytearray()
    for i in range(0, len(icon_bytes), 4):
        b, g, r, a = icon_bytes[i:i + 4]
        rgba_bytes.extend([r, g, b, a])

    with open(icon_path, 'wb') as f:
        # PNG file signature
        f.write(b'\x89PNG\r\n\x1a\n')

        # IHDR chunk
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
        f.write(png_chunk(b'IHDR', ihdr_data))

        # IDAT chunk
        row_data = b''
        for y in range(height):
            row_data += b'\x00'  # Filter type 0 (None)
            row_data += rgba_bytes[y * width * 4:(y + 1) * width * 4]

        compressed_data = zlib.compress(row_data)
        f.write(png_chunk(b'IDAT', compressed_data))

        # IEND chunk
        f.write(png_chunk(b'IEND', b''))

