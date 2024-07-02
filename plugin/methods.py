from pyflowlauncher import Method, ResultResponse, Result, shared, JsonRPCAction, string_matcher, utils, icons
from plugin.komorebic_client import WKomorebic
from utils import state, score_resluts_with_sub, get_first_word


class Query(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []
        self.functions_dict = {}

    def __call__(self, query: str) -> ResultResponse:
        state_json = state(self.pipe)
        if not state_json['is_paused']:
            if get_first_word(query) in self.functions_dict:
                self.functions_dict[get_first_word(query)](query, state_json)
            else:
                self.call_methods(query, state_json)
        return self.return_results()

    def call_methods(self, query: str, state_j):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and (not attr_name.startswith('__') and not attr_name.endswith('__')) and (
                    not 'add_function' in attr_name
                    or not 'add_function' in attr_name
                    or not 'run_function' in attr_name
                    or not 'call_methods' in attr_name
                    or not 'add_result' in attr_name
                    or not 'call' in attr_name
                    or not 'init' in attr_name
                    or not 'return_results'):
                attr(query, state_j)  # Call the method

    def add_function(self, key, function):
        """Adds a function to the dictionary with the given key."""
        self.functions_dict[key] = function

    def run_function(self, key, query, state_j):
        """Runs the function corresponding to the given key if it exists."""
        if key in self.functions_dict:
            self.functions_dict[key](query, state_j)

    def application_focus(self, state_j, query):
        application_list = []

        for monitor in state_j['monitors']['elements']:
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
