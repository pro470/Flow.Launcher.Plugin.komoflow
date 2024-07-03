from typing import Optional, Iterable, Any

from pyflowlauncher import Method, ResultResponse, Result, shared, JsonRPCAction, string_matcher, utils, icons, api
from plugin.komorebic_client import WKomorebic
from utils import state, score_resluts_with_sub, get_first_word, exit_komoflow


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
        start_list = []

        first_word = get_first_word(query)

        r = Result(Title='start',
                   SubTitle='Start komorebi.exe as a background process')

        if first_word == "start":

            new_query = query.replace('start', '')
            ffm: bool = False
            config: Optional[Iterable[Any]] = None
            await_configuration: bool = False
            tcp: Optional[Iterable[Any]] = None
            whkd: bool = False
            ahk: bool = False
            result_ffm = Result(Title='ffm',
                                SubTitle="Allow the use of komorebi's custom focus-follows-mouse implementation",
                                AutoCompleteText="ffm",
                                JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "ffm"],
                                                            dontHideAfterAction=True))

            if 'ffm' in query:
                ffm = True
                new_query = new_query.replace(" ffm", "")
            else:
                start_list.append(result_ffm)

            result_await_configuration = Result(Title='await-configuration',
                                                SubTitle="Wait for 'komorebic complete-configuration' to be sent before processing events",
                                                AutoCompleteText="await-configuration",
                                                JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "await-configuration"],
                                                                            dontHideAfterAction=True))

            if 'await-configuration' in query:
                await_configuration = True
                new_query = new_query.replace(" await-configuration", "")
            else:
                start_list.append(result_await_configuration)

            rr = utils.score_results(new_query, start_list, match_on_empty_query=True)

            r.JsonRPCAction = JsonRPCAction(method="start",
                                            parameters=[ffm, config, await_configuration, tcp, whkd, ahk])
        else:
            r.JsonRPCAction = JsonRPCAction(method="start", parameters=[])
            start_list.append(r)
            rr = utils.score_results(query, start_list, match_on_empty_query=True)

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


def append_if_matches(input_string, word_to_check):
    words = input_string.split()
    if not words:
        return input_string  # If input_string is empty or only whitespace, return as is

    last_word = words[-1]
    if word_to_check.startswith(last_word):
        # Find the part of word_to_check that is not in last_word
        remaining_part = word_to_check[len(last_word):]
        # Append the remaining part to the input string
        return input_string + remaining_part
    else:
        if input_string.endswith(" "):
            return input_string + word_to_check
        else:
            return input_string + " " + word_to_check


class Change(Method):

    def __init__(self, settings):
        self.settings = settings

    def __call__(self, query, word_to_check) -> JsonRPCAction:
        query = "kc " + query

        return api.change_query(query=append_if_matches(query, word_to_check))


class App_focus(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self, exe: str, hwnd: int):
        self.komorebic.focus_exe(exe=[exe], hwnd=[str(hwnd)])
        exit_komoflow(self.komorebic, self.pipe, self.pipename)


class Quickstart(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self):
        self.komorebic.quickstart()
        exit_komoflow(self.komorebic, self.pipe, self.pipename)


class Start(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self._logger = shared.logger(self)
        self._results: list[Result] = []

    def __call__(self, ffm: bool = False, config: Optional[Iterable[Any]] = None, await_configuration: bool = False,
                 tcp_port: Optional[Iterable[Any]] = None, whkd: bool = False, ahk: bool = False):
        self.komorebic.start(ffm=ffm, config=config, await_configuration=await_configuration, tcp_port=tcp_port,
                             whkd=whkd, ahk=ahk)
        exit_komoflow(self.komorebic, self.pipe, self.pipename)
