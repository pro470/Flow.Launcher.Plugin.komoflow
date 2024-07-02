from pyflowlauncher import Method, ResultResponse, Result, shared, JsonRPCAction, string_matcher, utils, icons
from plugin.komorebic_client import WKomorebic
from utils import state, score_resluts_with_sub


class Query(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self, query: str) -> ResultResponse:
        state_json = state(self.pipe)
        if not state_json['is_paused']:
            self.application_focus(state_json, query)
        return self.return_results()

    def application_focus(self, state, query):
        application_list = []

        for monitor in state['monitors']['elements']:
            for workspace in monitor['workspaces']['elements']:
                for container in workspace['containers']['elements']:
                    for window in container['windows']['elements']:
                        r = Result(
                            Title=str(window['title']),
                            SubTitle=f"EXE: {str(window['exe'])}, HWND: {str(window['hwnd'])}",
                            JsonRPCAction=JsonRPCAction(method="app_focus",
                                                        parameters=[str(window['exe']), int(window['hwnd'])]),

                        )
                        application_list.append(r)

        scored_results = score_resluts_with_sub(query, application_list)

        for scored_result in scored_results:

            self.add_result(scored_result)


class Context_menu(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self, data) -> ResultResponse:
        return self.return_results()


class App_focus(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self, exe: str, hwnd: int):
        self.komorebic.focus_exe(exe=[exe], hwnd=[str(hwnd)])
