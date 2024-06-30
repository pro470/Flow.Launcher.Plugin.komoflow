from pyflowlauncher import Method, ResultResponse, Result
from plugin.komorebic_client import WKomorebic
from plugin.utils import *


class Query(Method):

    def __init__(self, komorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, query: str) -> ResultResponse:
        state_json = state(self.pipe)
        if not state_json['is_paused']:
            self.application_focus(state_json)

        return self.return_results()

    def application_focus(self, state):

        application_list = []

        for monitor in state['monitors']['elements']:
            for workspace in monitor['workspaces']['elements']:
                for container in workspace['containers']['elements']:
                    for window in container['windows']['elements']:
                        application_list.append([window['exe'], window['hwnd'], window['title']])
                        r = Result(
                            Title=window['title'],
                            SubTitle=f'''Exe: {window['exe']}, HWND: {window['hwnd']}'''
                        )

                        self.add_result(r)


class Context_menu(Method):

    def __init__(self, komorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, data) -> ResultResponse:
        return self.return_results()


class App_focus(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, hwnd, exe):
        self.komorebic.focus_exe()
