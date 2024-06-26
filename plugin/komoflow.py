import flowlauncher.FlowLauncherAPI
from flowlauncher import FlowLauncher
import logging
import win32pipe, win32file
import json
import time
from plugin.komorebic_client import WKomorebic


BUFFER_SIZE = 1024 * 64

class Komoflow(FlowLauncher):

    def __init__(self):
        self.komorebic = WKomorebic()
        self.pipe = None
        self.pipename = 'komoflow'
        self.create_named_pipe()
        self.connect_komorebi()

    def create_named_pipe(self) -> None:
        self.pipe = win32pipe.CreateNamedPipe(f'\\\\.\\pipe\\{self.pipename}',
                                              win32pipe.PIPE_ACCESS_DUPLEX,
                                              win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                                              1,
                                              BUFFER_SIZE,
                                              BUFFER_SIZE,
                                              50,
                                              None)
        logging.info(f'Created named pipe ${self.pipename}')

    def connect_komorebi(self) -> None:
        self.komorebic.subscribe_pipe(self.pipename)
        logging.info("connect successfully")


    def exit_komoflow(self) -> None:
        win32pipe.DisconnectNamedPipe(self.pipe)
        win32file.CloseHandle(self.pipe)

    def state(self):


        # read komorebi event
        try:
            buffer, bytes_to_read, status = win32pipe.PeekNamedPipe(self.pipe, 1);
            while True:
                if not bytes_to_read:
                    time.sleep(0.1)
                else:
                    break

            result, data = win32file.ReadFile(self.pipe, bytes_to_read)
            if not data.strip():
                return
            event = json.loads(data.decode("utf-8"))
            # event = json.loads(data)
            # print(json.dumps(event, indent=4))

            event_state = event['state']

            return event_state

        except (BaseException, Exception):
            win32pipe.DisconnectNamedPipe(self.pipe)
            win32file.CloseHandle(self.pipe)
            print("There are exceptions")
    def query(self, param: str = '') -> list:


        return


    def context_menu(self, data) -> list:



        return



