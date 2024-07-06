import json
import logging
import subprocess
import time
import os
import ctypes
import ctypes.wintypes
from pyflowlauncher import Result, string_matcher
from typing import Iterable, Generator, Optional
from komorebic_client import WKomorebic

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
            bytes_read = ctypes.wintypes.DWORD()
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
