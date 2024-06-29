import json
import logging
import time
import win32file
import win32pipe

BUFFER_SIZE = 1024 * 64


def create_named_pipe(pipename):
    pipe = win32pipe.CreateNamedPipe(f'\\\\.\\pipe\\{pipename}',
                                     win32pipe.PIPE_ACCESS_DUPLEX,
                                     win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                                     1,
                                     BUFFER_SIZE,
                                     BUFFER_SIZE,
                                     50,
                                     None)

    logging.info(f'Created named pipe ${pipename}')

    return pipe


def connect_komorebi(wkomorebic, pipename) -> None:
    wkomorebic.subscribe_pipe(pipename)
    logging.info("connect successfully")


def exit_komoflow(pipe) -> None:
    win32pipe.DisconnectNamedPipe(pipe)
    win32file.CloseHandle(pipe)


def state(pipe):
    # read komorebi event
    try:
        while True:
            buffer, bytes_to_read, status = win32pipe.PeekNamedPipe(pipe, 1)
            if not bytes_to_read:
                time.sleep(0.1)
            else:
                break

        result, data = win32file.ReadFile(pipe, bytes_to_read)
        if not data.strip():
            return
        event = json.loads(data.decode("utf-8"))
        # event = json.loads(data)
        # print(json.dumps(event, indent=4))

        event_state = event['state']

        return event_state

    except (BaseException, Exception):
        win32pipe.DisconnectNamedPipe(pipe)
        win32file.CloseHandle(pipe)
        print("There are exceptions")
