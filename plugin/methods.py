from typing import Optional, Iterable, Any
import re, os, fnmatch
from pyflowlauncher import Method, ResultResponse, Result, shared, JsonRPCAction, string_matcher, utils, icons, api
from plugin.komorebic_client import WKomorebic
from utils import state, score_resluts_with_sub, get_first_word, append_if_matches, word_before_last_bracket, \
    find_files_in_user_directory


class Query(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self.functions_dict = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and not attr_name.startswith('__') and not attr_name.endswith('__'):
                if attr_name != 'application_focus' and attr_name != 'add_function' and 'add_function' != attr_name and 'run_function' != attr_name and 'call_methods' != attr_name and 'add_result' != attr_name and 'return_results' != attr_name:
                    self.functions_dict[attr_name.replace('_', '-')] = attr

    def __call__(self, query: str) -> ResultResponse:
        state_json = state(self.pipe)
        if state_json is None:
            self.start(query, state_json)
        else:
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
            tcp_port: Optional[Iterable[Any]] = None
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
                if not word_before_last_bracket(query):
                    start_list.append(result_ffm)

            result_await_configuration = Result(Title='await-configuration',
                                                SubTitle="Wait for 'komorebic complete-configuration' to be sent before processing events",
                                                AutoCompleteText="await-configuration",
                                                JsonRPCAction=JsonRPCAction(method="change",
                                                                            parameters=[query, "await-configuration"],
                                                                            dontHideAfterAction=True))

            if 'await-configuration' in query:
                await_configuration = True
                new_query = new_query.replace(" await-configuration", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_await_configuration)

            result_whkd = Result(Title='whkd',
                                 SubTitle="Start whkd in a background process",
                                 AutoCompleteText="whkd",
                                 JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "whkd"],
                                                             dontHideAfterAction=True))

            if 'whkd' in query:
                whkd = True
                new_query = new_query.replace(" whkd", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_whkd)

            result_ahk = Result(Title='ahk',
                                SubTitle="Start autohotkey configuration file",
                                AutoCompleteText="ahk",
                                JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "ahk"],
                                                            dontHideAfterAction=True))

            if 'ahk' in query:
                ahk = True
                new_query = new_query.replace(" ahk", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_ahk)

            result_config = Result(Title='config',
                                   SubTitle="Path to a static configuration JSON file",
                                   AutoCompleteText="config",
                                   JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "config [ "],
                                                               dontHideAfterAction=True))

            if 'config' in query:
                if re.search(r'\s+config\s*\[.*?\]', new_query):
                    matches = re.search(r'\s+config\s*\[(.*?)\]', query)
                    config = [matches.group(1)]
                    new_query = re.sub(r'\s+config\s*\[.*?\]', '', new_query)
                else:
                    new_query = new_query.replace(" config", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_config)

            result_tcp_port = Result(Title='tcp-port',
                                     SubTitle="Start a TCP server on the given port to allow the direct sending of SocketMessages",
                                     AutoCompleteText="tcp-port",
                                     JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "tcp-port [ "],
                                                                 dontHideAfterAction=True))

            if 'tcp-port' in query:
                if re.search(r'\s+tcp-port\s*\[.*?\]', new_query):
                    matches = re.search(r'\s+tcp-port\s*\[(.*?)\]', query)
                    tcp_port = [matches.group(1).strip()]
                    new_query = re.sub(r'\s+tcp-port\s*\[.*?\]', '', new_query)
                else:
                    new_query = new_query.replace(" tcp-port", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_tcp_port)

            if word_before_last_bracket(query):
                word_before = word_before_last_bracket(query)

                if word_before == "config":
                    matches = find_files_in_user_directory()

                    new_query = new_query.replace(" [", "")

                    for match in matches:
                        match_result = Result(Title=match,
                                              AutoCompleteText=match,
                                              JsonRPCAction=JsonRPCAction(method="change",
                                                                          parameters=[query, match + " ]"],
                                                                          dontHideAfterAction=True))

                        start_list.append(match_result)

                elif word_before == "tcp-port":

                    new_query = re.sub(r'\s*\[\s*', '', new_query)

                    if not new_query.strip().isdigit():
                        notdigit = Result(Title='Not a number needs to be a number')
                        self.add_result(notdigit)

            rr = utils.score_results(new_query, start_list, match_on_empty_query=True)

            r = Result(Title='run',
                       SubTitle='run start command with this parameters')

            r.JsonRPCAction = JsonRPCAction(method="start",
                                            parameters=[ffm, config, await_configuration, tcp_port, whkd, ahk])

            if not word_before_last_bracket(query):
                self.add_result(r)

        else:
            r.JsonRPCAction = JsonRPCAction(method="start", parameters=[])
            start_list.append(r)
            rr = utils.score_results(query, start_list, match_on_empty_query=True)

        tcp_port_nummer = re.search(r'\s+tcp-port\s*\[(.*?)\]', query)

        for scored_results in rr:
            self.add_result(scored_results)

        if tcp_port_nummer:
            if not tcp_port_nummer.group(1).strip().isdigit():
                self._results = [Result(Title='Not a number needs to be a number')]

        config_path = re.search(r'\s+config\s*\[(.*?)\]', query)
        if config_path:
            if not os.path.exists(config_path.group(1).strip()):
                if not config_path.group(1).strip().endswith('komorebi.json'):
                    self._results = [Result(Title='Path dont exits or is not a komorebi.json path')]

    def stop(self, query: str, state_j):

        stop_list = []

        first_word = get_first_word(query)

        r = Result(Title='stop',
                   SubTitle='Stop the komorebi.exe process and restore all hidden windows')

        if first_word == "stop":

            new_query = query.replace('stop', '')

            whkd: bool = False

            result_whkd = Result(Title='whkd',
                                 SubTitle="Start whkd in a background process",
                                 AutoCompleteText="whkd",
                                 JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "whkd"],
                                                             dontHideAfterAction=True))

            if 'whkd' in query:
                whkd = True
                new_query = new_query.replace(" whkd", "")
            else:
                if not word_before_last_bracket(query):
                    stop_list.append(result_whkd)

            rr = utils.score_results(new_query, stop_list, match_on_empty_query=True)

            r = Result(Title='run',
                       SubTitle='Stop the komorebi.exe process and restore all hidden windows',
                       JsonRPCAction=JsonRPCAction(method="stop", parameters=[whkd]))

            if not word_before_last_bracket(query):
                self.add_result(r)

        else:
            r.JsonRPCAction = JsonRPCAction(method="stop", parameters=[])
            stop_list.append(r)
            rr = utils.score_results(query, stop_list, match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def check(self, query: str, state_j):
        r = Result(Title='check',
                   SubTitle='Check komorebi configuration and related files for common errors',
                   JsonRPCAction=JsonRPCAction(method="check",
                                               parameters=[]))
        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def configuration(self, query: str, state_j):
        r = Result(Title='configuration',
                   SubTitle='Show the path to komorebi.json',
                   JsonRPCAction=JsonRPCAction(method="configuration",
                                               parameters=[]))
        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def whkdrc(self, query: str, state_j):
        r = Result(Title='whkdrc',
                   SubTitle='Show the path to whkdrc',
                   JsonRPCAction=JsonRPCAction(method="whkdrc",
                                               parameters=[]))
        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)




class Context_menu(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, data) -> ResultResponse:
        return self.return_results()


class Change(Method):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def __call__(self, query, word_to_check) -> JsonRPCAction:
        query = "kc" + " " + query

        return api.change_query(query=append_if_matches(query, word_to_check))


class App_focus(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, exe: str, hwnd: int):
        self.komorebic.focus_exe(exe=[exe], hwnd=[str(hwnd)])


class Quickstart(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self):
        self.komorebic.quickstart()


class Start(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, ffm: bool = False, config: Optional[Iterable[Any]] = None, await_configuration: bool = False,
                 tcp_port: Optional[Iterable[Any]] = None, whkd: bool = False, ahk: bool = False):
        self.komorebic.start(ffm=ffm, config=config, await_configuration=await_configuration, tcp_port=tcp_port,
                             whkd=whkd, ahk=ahk)


class Stop(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, whkd: bool):
        self.komorebic.start(whkd=whkd)


class Check(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.check()

        return api.copy_to_clipboard(str(result.stdout))


class Configuration(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.configuration()

        return api.copy_to_clipboard(str(result.stdout))


class Whkdrc(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.whkdrc()

        return api.copy_to_clipboard(str(result.stdout))
