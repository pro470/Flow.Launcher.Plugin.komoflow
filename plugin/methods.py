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
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and not attr_name.startswith('__') and not attr_name.endswith('__'):
                if attr_name != 'application_focus' and attr_name != 'add_function' and 'add_function' != attr_name and 'run_function' != attr_name and 'call_methods' != attr_name and 'add_result' != attr_name and 'return_results' != attr_name:
                    self.functions_dict[attr_name.replace('_', '-')] = attr

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
            if callable(attr) and not attr_name.startswith('__') and not attr_name.endswith('__'):
                if attr_name != 'add_function' and 'add_function' != attr_name and 'run_function' != attr_name and 'call_methods' != attr_name and 'add_result' != attr_name and 'return_results' != attr_name:
                    attr(query, state_j)  # Call the method

    def add_function(self, key, function):
        """Adds a function to the dictionary with the given key."""
        self.functions_dict[key] = function

    def run_function(self, key, query, state_j):
        """Runs the function corresponding to the given key if it exists."""
        if key in self.functions_dict:
            self.functions_dict[key](query, state_j)

    def application_focus(self, query, state_j):
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

    def quickstart(self, query: str, state_j):
        r = Result(Title='quickstart',
                   SubTitle='Gather example configurations for a new-user quickstart',
                   JsonRPCAction=JsonRPCAction(method="quickstart",
                                               parameters=[]))
        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)


    def start(self, query: str, state_j):

        first_word = get_first_word(query)

        r = Result(Title='start',
                   SubTitle='Start komorebi.exe as a background process')

        if first_word == "start":
            para_dict = {}
            para_dict['ffm'] = True
            r.JsonRPCAction = JsonRPCAction(method="start", parameters=para_dict)
        else:
            r.JsonRPCAction = JsonRPCAction(method="start", parameters=[])

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)




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

class Quickstart(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self):
        self.komorebic.quickstart()