import subprocess
from pathlib import Path
from typing import Optional, Iterable, Any
import re, os, fnmatch
from pyflowlauncher import Method, ResultResponse, Result, shared, JsonRPCAction, string_matcher, utils, icons, api
from plugin.komorebic_client import WKomorebic
from utils import state, score_resluts_with_sub, get_first_word, append_if_matches, word_before_last_bracket, \
    find_files_in_user_directory, extract_icon_from_running_process, IconSize, save_icon_as_png, query_windows_search, \
    everything_search


class Query(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename, root_dir: Path):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename
        self.root_dir = root_dir
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

        for i, monitor in enumerate(state_j['monitors']['elements']):
            for j, workspace in enumerate(monitor['workspaces']['elements']):
                for k, container in enumerate(workspace['containers']['elements']):
                    for l, window in enumerate(container['windows']['elements']):

                        exe_path = "icons/" + window['exe'][:-4] + ".png"

                        png_path = self.root_dir / exe_path
                        if not os.path.exists(png_path):
                            bits = extract_icon_from_running_process(window['exe'])
                            icon_size = IconSize.LARGE
                            w, h = IconSize.to_wh(icon_size)
                            if bits:
                                save_icon_as_png(bits, png_path, w, h)

                        if os.path.exists(png_path):
                            r = Result(
                                Title=str(window['title']),
                                SubTitle=f"EXE: {str(window['exe'])}, HWND: {str(window['hwnd'])}, MONITOR: {str(i + 1)}, WORKSPACE: {str(j + 1)}",
                                IcoPath=png_path.__str__(),
                                JsonRPCAction=JsonRPCAction(method="app_focus",
                                                            parameters=[str(window['exe']), int(window['hwnd'])]),
                            )
                        else:
                            r = Result(
                                Title=str(window['title']),
                                SubTitle=f"EXE: {str(window['exe'])}, HWND: {str(window['hwnd'])}, MONITOR: {str(i + 1)}, WORKSPACE: {str(j + 1)}",
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

            new_query = query.strip().replace('start', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()
            ffm: bool = False
            config: Optional[Iterable[Any]] = None
            await_configuration: bool = False
            tcp_port: Optional[Iterable[Any]] = None
            whkd: bool = False
            ahk: bool = False
            result_ffm = Result(Title='ffm',
                                SubTitle="Allow the use of komorebi's custom focus-follows-mouse implementation",
                                AutoCompleteText="ffm",
                                JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "ffm", ['ffm', 'config',
                                                                                                        'await-configuration',
                                                                                                        'tcp-port',
                                                                                                        'whkd', 'ahk',
                                                                                                        'start']],
                                                            dontHideAfterAction=True))

            if 'ffm' in query:
                ffm = True
                new_query = new_query.strip().replace("ffm", "")
                new_query = re.sub(r'\s+', ' ', new_query).strip()
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_ffm)

            result_await_configuration = Result(Title='await-configuration',
                                                SubTitle="Wait for 'komorebic complete-configuration' to be sent before processing events",
                                                AutoCompleteText="await-configuration",
                                                JsonRPCAction=JsonRPCAction(method="change",
                                                                            parameters=[query, "await-configuration",
                                                                                        ['ffm', 'config',
                                                                                         'await-configuration',
                                                                                         'tcp-port', 'whkd', 'ahk',
                                                                                         'start']],
                                                                            dontHideAfterAction=True))

            if 'await-configuration' in query:
                await_configuration = True
                new_query = new_query.strip().replace("await-configuration", "")
                new_query = re.sub(r'\s+', ' ', new_query).strip()
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_await_configuration)

            result_whkd = Result(Title='whkd',
                                 SubTitle="Start whkd in a background process",
                                 AutoCompleteText="whkd",
                                 JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "whkd",
                                                                                          ['ffm', 'config',
                                                                                           'await-configuration',
                                                                                           'tcp-port', 'whkd', 'ahk',
                                                                                           'start']],
                                                             dontHideAfterAction=True))

            if 'whkd' in query:
                whkd = True
                new_query = new_query.strip().replace("whkd", "")
                new_query = re.sub(r'\s+', ' ', new_query).strip()
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_whkd)

            result_ahk = Result(Title='ahk',
                                SubTitle="Start autohotkey configuration file",
                                AutoCompleteText="ahk",
                                JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "ahk", ['ffm', 'config',
                                                                                                        'await-configuration',
                                                                                                        'tcp-port',
                                                                                                        'whkd', 'ahk',
                                                                                                        'start']],
                                                            dontHideAfterAction=True))

            if 'ahk' in query:
                ahk = True
                new_query = new_query.strip().replace("ahk", "")
                new_query = re.sub(r'\s+', ' ', new_query).strip()
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_ahk)

            result_config = Result(Title='config',
                                   SubTitle="Path to a static configuration JSON file",
                                   AutoCompleteText="config",
                                   JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "config [ ",
                                                                                            ['ffm', 'config',
                                                                                             'await-configuration',
                                                                                             'tcp-port', 'whkd', 'ahk',
                                                                                             'start']],
                                                               dontHideAfterAction=True))

            if ' config ' in query:
                if re.search(r'\bconfig\s*\[.*?\]', new_query):
                    matches = re.search(r'\bconfig\s*\[(.*?)\]', query)
                    config = [matches.group(1).strip()]
                    new_query = re.sub(r'\bconfig\b\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("config", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_config)

            result_tcp_port = Result(Title='tcp-port',
                                     SubTitle="Start a TCP server on the given port to allow the direct sending of SocketMessages",
                                     AutoCompleteText="tcp-port",
                                     JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "tcp-port [ ",
                                                                                              ['ffm', 'config',
                                                                                               'await-configuration',
                                                                                               'tcp-port', 'whkd',
                                                                                               'ahk', 'start']],
                                                                 dontHideAfterAction=True))

            if 'tcp-port' in query:
                if re.search(r'\btcp-port\s*\[.*?\]', new_query):
                    matches = re.search(r'\btcp-port\s*\[(.*?)\]', query)
                    tcp_port = [matches.group(1).strip()]
                    new_query = re.sub(r'\btcp-port\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("tcp-port", "")
            else:
                if not word_before_last_bracket(query):
                    start_list.append(result_tcp_port)

            if word_before_last_bracket(query):
                word_before = word_before_last_bracket(query)

                if word_before == "config":

                    new_query = new_query.strip().replace("[", "")
                    new_query = re.sub(r'\s+', ' ', new_query).strip()

                    if new_query == "":
                        everything_matches = everything_search("komorebi.json")
                    else:
                        everything_matches = everything_search(new_query)

                    if everything_matches:
                        for match in everything_matches:
                            match_result = Result(Title=match,
                                                  AutoCompleteText=match,
                                                  JsonRPCAction=JsonRPCAction(method="change",
                                                                              parameters=[query, match + " ]",
                                                                                          ['ffm', 'config',
                                                                                           'await-configuration',
                                                                                           'tcp-port', 'whkd', 'ahk',
                                                                                           'start', '[']],
                                                                              dontHideAfterAction=True))

                            start_list.append(match_result)
                    else:

                        if new_query == "":

                            matches = query_windows_search("komorebi.json")

                        else:
                            matches = query_windows_search(new_query)

                        if isinstance(matches, list):

                            for match in matches:
                                match_result = Result(Title=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, match[
                                                                                      'SYSTEM.ITEMPATHDISPLAY'] + " ]",
                                                                                              ['ffm', 'config',
                                                                                               'await-configuration',
                                                                                               'tcp-port', 'whkd',
                                                                                               'ahk',
                                                                                               'start', '[']],
                                                                                  dontHideAfterAction=True))

                                start_list.append(match_result)
                        else:
                            if matches:
                                match_result = Result(Title=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, matches[
                                                                                      'SYSTEM.ITEMPATHDISPLAY'] + " ]",
                                                                                              ['ffm', 'config',
                                                                                               'await-configuration',
                                                                                               'tcp-port', 'whkd',
                                                                                               'ahk',
                                                                                               'start', '[']],
                                                                                  dontHideAfterAction=True))

                                start_list.append(match_result)

                elif word_before == "tcp-port":

                    new_query = re.sub(r'\s*\[\s*', '', new_query)

                    if not new_query.strip().isdigit():
                        notdigit = Result(Title='Not a number needs to be a number')
                        self.add_result(notdigit)

            rr = utils.score_results(new_query.strip(), start_list, match_on_empty_query=True)

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
                self._results = [Result(Title='Path dont exits')]

    def stop(self, query: str, state_j):

        stop_list = []

        first_word = get_first_word(query)

        r = Result(Title='stop',
                   SubTitle='Stop the komorebi.exe process and restore all hidden windows')

        if first_word == "stop":

            new_query = query.strip().replace('stop', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            whkd: bool = False

            result_whkd = Result(Title='whkd',
                                 SubTitle="Start whkd in a background process",
                                 AutoCompleteText="whkd",
                                 JsonRPCAction=JsonRPCAction(method="change",
                                                             parameters=[query, "whkd", ["stop", "whkd"]],
                                                             dontHideAfterAction=True))

            if 'whkd' in query:
                whkd = True
                new_query = new_query.strip().replace("whkd", "")
                new_query = re.sub(r'\s+', ' ', new_query).strip()

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

    def state(self, query: str, state_j):
        r = Result(Title='state',
                   SubTitle='Show a JSON representation of the current window manager state',
                   JsonRPCAction=JsonRPCAction(method="state", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def global_state(self, query: str, state_j):
        r = Result(Title='global-state',
                   SubTitle='Show a JSON representation of the current global state',
                   JsonRPCAction=JsonRPCAction(method="global_state", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def gui(self, query: str, state_j):
        r = Result(Title='gui',
                   SubTitle='Launch the komorebi-gui debugging tool',
                   JsonRPCAction=JsonRPCAction(method="gui", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def visible_windows(self, query: str, state_j):

        visible_windows_list = []

        first_word = get_first_word(query)

        if first_word == 'visible-windows':

            new_query = query.strip().replace('visible-windows', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            for i, monitor in enumerate(state_j['monitors']['elements']):
                monitor_result = Result(Title=monitor['device_id'],
                                        SubTitle=f"name: {monitor['name']} divice: {monitor['device']}",
                                        JsonRPCAction=JsonRPCAction(method="change",
                                                                    parameters=[query, monitor['device'],
                                                                                ['visible-windows']],
                                                                    dontHideAfterAction=True))
                visible_windows_list.append(monitor_result)
                focused_w_index = monitor['workspaces']['focused']
                focused_workspace = monitor['workspaces']['elements'][focused_w_index]
                for k, container in enumerate(focused_workspace['containers']['elements']):
                    for l, window in enumerate(container['windows']['elements']):

                        exe_path = "icons/" + window['exe'][:-4] + ".png"

                        png_path = self.root_dir / exe_path
                        if not os.path.exists(png_path):
                            bits = extract_icon_from_running_process(window['exe'])
                            icon_size = IconSize.LARGE
                            w, h = IconSize.to_wh(icon_size)
                            if bits:
                                save_icon_as_png(bits, png_path, w, h)

                        json_window = f'''{{
    "title": "{window['title']}",
    "exe": "{window['exe']}",
    "class": "{window['class']}"
}}'''

                        if os.path.exists(png_path):
                            r = Result(
                                Title=window['title'] + ' - ' + f"name: {monitor['name']} divice: {monitor['device']}",
                                SubTitle=f"EXE: {str(window['exe'])}, MONITOR: {str(i + 1)}, WORKSPACE: {str(focused_w_index + 1)}, CLASS: {str(window['class'])}",
                                IcoPath=png_path.__str__(),
                                JsonRPCAction=JsonRPCAction(method="copy_to_clipboard",
                                                            parameters=[json_window]),
                            )
                        else:
                            r = Result(
                                Title=window['title'] + f"name: {monitor['name']} divice: {monitor['device']}",
                                SubTitle=f"EXE: {str(window['exe'])}, MONITOR: {str(i + 1)}, WORKSPACE: {str(focused_w_index + 1)}, CLASS: {str(window['class'])}",
                                JsonRPCAction=JsonRPCAction(method="copy_to_clipboard",
                                                            parameters=[json_window]),

                            )

                        visible_windows_list.append(r)

            run = Result(Title='copy to clipboard (all)',
                         SubTitle='Show a JSON representation of visible windows',
                         JsonRPCAction=JsonRPCAction(method="visible_windows", parameters=[]))

            rr = utils.score_results(new_query, visible_windows_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

            self.add_result(run)




        else:
            r = Result(Title='visible-windows',
                       SubTitle='Show a JSON representation of visible windows',
                       JsonRPCAction=JsonRPCAction(method="visible_windows", parameters=[]))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def monitor_information(self, query: str, state_j):

        monitor_information_list = []

        first_word = get_first_word(query)

        if first_word == 'monitor-information':

            new_query = query.strip().replace('monitor-information', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            for i, monitor in enumerate(state_j['monitors']['elements']):
                json_window = f'''{{
    "{monitor['device_id']}": {{
        "left": {monitor['size']['left']},
        "top": {monitor['size']['top']},
        "right": {monitor['size']['right']},
        "bottom": {monitor['size']['bottom']} 
    }}
}}'''

                monitor_result = Result(Title=monitor['device_id'],
                                        SubTitle=f"name: {monitor['name']} divice: {monitor['device']}",
                                        JsonRPCAction=JsonRPCAction(method="copy_to_clipboard",
                                                                    parameters=[json_window]))
                monitor_information_list.append(monitor_result)

            run = Result(Title='copy to clipboard (all)',
                         SubTitle='Show information about connected monitors',
                         JsonRPCAction=JsonRPCAction(method="monitor_information", parameters=[]))

            rr = utils.score_results(new_query, monitor_information_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

            self.add_result(run)
        else:
            r = Result(Title='monitor-information',
                       SubTitle='Show information about connected monitors',
                       JsonRPCAction=JsonRPCAction(method="monitor_information", parameters=[]))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def query(self, query: str, state_j):

        query_list = []

        first_word = get_first_word(query)

        if first_word == "query":

            new_query = query.strip().replace('query', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            fmi_result = Result(Title="focused-monitor-index",
                                SubTitle="",
                                JsonRPCAction=JsonRPCAction(method="state_query",
                                                            parameters=['focused-monitor-index']))

            fwi_result = Result(Title="focused-workspace-index",
                                SubTitle="",
                                JsonRPCAction=JsonRPCAction(method="state_query",
                                                            parameters=['focused-workspace-index']))

            fci_result = Result(Title="focused-container-index",
                                SubTitle="",
                                JsonRPCAction=JsonRPCAction(method="state_query",
                                                            parameters=['focused-container-index']))

            fwwi_result = Result(Title="focused-window-index",
                                 SubTitle="",
                                 JsonRPCAction=JsonRPCAction(method="state_query",
                                                             parameters=['focused-window-index']))

            query_list.append(fmi_result)
            query_list.append(fwi_result)
            query_list.append(fci_result)
            query_list.append(fwwi_result)

            rr = utils.score_results(new_query, query_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)
        else:
            r = Result(Title="query",
                       SubTitle="Query the current window manager state",
                       JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "query", ["query"]],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def subscribe_socket(self, query: str, state_j):

        first_word = get_first_word(query)

        if first_word == 'subscribe-socket':

            new_query = query.strip().replace('subscribe-socket', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            if re.search(r'\s+', new_query):

                r = Result(Title="need to provide only one word")
                self._results = [r]
            elif '' == new_query:
                r = Result(Title="Need to provide a name")
                self._results = [r]
            else:
                r = Result(Title="run",
                           SubTitle="Subscribe to komorebi events using a Unix Domain Socket",
                           JsonRPCAction=JsonRPCAction(method='subscribe-socket', parameters=[new_query])
                           )

                self.add_result(r)

        else:
            r = Result(Title='subscribe-socket',
                       SubTitle="Subscribe to komorebi events using a Unix Domain Socket",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'subscribe-socket', ['subscribe-socket']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def unsubscribe_socket(self, query: str, state_j):

        first_word = get_first_word(query)

        if first_word == 'unsubscribe-socket':

            new_query = query.strip().replace('unsubscribe-socket', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            if re.search(r'\s+', new_query):

                r = Result(Title="need to provide only one word")
                self._results = [r]
            elif '' == new_query:
                r = Result(Title="Need to provide a name")
                self._results = [r]
            else:
                r = Result(Title="run",
                           SubTitle="Unsubscribe from komorebi events",
                           JsonRPCAction=JsonRPCAction(method='unsubscribe-socket', parameters=[new_query])
                           )

                self.add_result(r)

        else:
            r = Result(Title='unsubscribe-socket',
                       SubTitle="Unsubscribe from komorebi events",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'unsubscribe-socket', ['unsubscribe-socket']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def subscribe_pipe(self, query: str, state_j):

        first_word = get_first_word(query)

        if first_word == 'subscribe-pipe':

            new_query = query.strip().replace('subscribe-pipe', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            if re.search(r'\s+', new_query):

                r = Result(Title="need to provide only one word")
                self._results = [r]
            elif '' == new_query:
                r = Result(Title="Need to provide a name")
                self._results = [r]
            else:
                r = Result(Title="run",
                           SubTitle="Subscribe to komorebi events using a Named Pipe",
                           JsonRPCAction=JsonRPCAction(method='subscribe-pipe', parameters=[new_query])
                           )

                self.add_result(r)

        else:
            r = Result(Title='subscribe-pipe',
                       SubTitle="Subscribe to komorebi events using a Named Pipe",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'subscribe-pipe', ['subscribe-pipe']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def unsubscribe_pipe(self, query: str, state_j):

        first_word = get_first_word(query)

        if first_word == 'unsubscribe-pipe':

            new_query = query.strip().replace('unsubscribe-pipe', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            if re.search(r'\s+', new_query):

                r = Result(Title="need to provide only one word")
                self._results = [r]

            elif '' == new_query:
                r = Result(Title="Need to provide a name")
                self._results = [r]
            else:
                r = Result(Title="run",
                           SubTitle="Unsubscribe from komorebi events",
                           JsonRPCAction=JsonRPCAction(method='unsubscribe-pipe', parameters=[new_query])
                           )

                self.add_result(r)

        else:
            r = Result(Title='unsubscribe-pipe',
                       SubTitle="Unsubscribe from komorebi events",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'unsubscribe-pipe', ['unsubscribe-pipe']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def log(self, query: str, state_j):

        r = Result(Title="log",
                   SubTitle="Tail komorebi.exe's process logs (cancel with Ctrl-C)",
                   JsonRPCAction=JsonRPCAction(method="log", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def quick_save_resize(self, query: str, state_j):

        r = Result(Title="quick-save-resize",
                   SubTitle="Quicksave the current resize layout dimensions",
                   JsonRPCAction=JsonRPCAction(method="quick_save_resize", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def quick_load_resize(self, query: str, state_j):

        r = Result(Title="quick-load-resize",
                   SubTitle="Load the last quicksaved resize layout dimensions",
                   JsonRPCAction=JsonRPCAction(method="quick_load_resize", parameters=[]))

        rr = utils.score_results(query, [r], match_on_empty_query=True)

        for scored_results in rr:
            self.add_result(scored_results)

    def save_resize(self, query: str, state_j):

        save_resize_list = []

        first_word = get_first_word(query)

        if first_word == 'save-resize':

            save_resize = ''

            new_query = re.sub(r'\s+', ' ', query).strip()

            result_save_resize = Result(Title='save-resize',
                                        SubTitle="Save the current resize layout dimensions to a file",
                                        AutoCompleteText="save-resize",
                                        JsonRPCAction=JsonRPCAction(method="change",
                                                                    parameters=[query, "save-resize [ ",
                                                                                ['save-resize', "["]],
                                                                    dontHideAfterAction=True))

            if 'save-resize' in query:
                if re.search(r'\bsave-resize\s*\[.*?\]', new_query):
                    matches = re.search(r'\bsave-resize\s*\[(.*?)\]', query)
                    save_resize = matches.group(1).strip()
                    new_query = re.sub(r'\bsave-resize\b\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("save-resize", "")
            else:
                if not word_before_last_bracket(query):
                    save_resize_list.append(result_save_resize)

            if word_before_last_bracket(query):
                word_before = word_before_last_bracket(query)

                if word_before == "save-resize":

                    new_query = new_query.strip().replace("[", "")
                    new_query = re.sub(r'\s+', ' ', new_query).strip()

                    if new_query == "":
                        everything_matches = everything_search("save-resize")
                    else:
                        everything_matches = everything_search(new_query)

                    if everything_matches:
                        for match in everything_matches:
                            match_result = Result(Title=match,
                                                  AutoCompleteText=match,
                                                  JsonRPCAction=JsonRPCAction(method="change",
                                                                              parameters=[query, match + " ]",
                                                                                          ['save-resize', '[']],
                                                                              dontHideAfterAction=True))

                            save_resize_list.append(match_result)
                    else:

                        if new_query == "":
                            matches = query_windows_search("save-resize")

                        else:
                            matches = query_windows_search(new_query)

                        if isinstance(matches, list):

                            for match in matches:
                                match_result = Result(Title=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, match + " ]",
                                                                                              ['save-resize', '[']],
                                                                                  dontHideAfterAction=True))

                                save_resize_list.append(match_result)
                        else:
                            if matches:
                                match_result = Result(Title=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, matches + " ]",
                                                                                              ['save-resize', '[']],
                                                                                  dontHideAfterAction=True))

                                save_resize_list.append(match_result)

            rr = utils.score_results(new_query.strip(), save_resize_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

            save_resize_path = re.search(r'\s*save-resize\s*\[(.*?)\]', query)

            if save_resize_path:
                if not os.path.exists(save_resize_path.group(1).strip()):
                    self._results = [Result(Title='Path doenst exits')]

                else:

                    r = Result(Title='run',
                               SubTitle='run start command with this parameters')

                    r.JsonRPCAction = JsonRPCAction(method="save_resize",
                                                    parameters=[save_resize])

                    if not word_before_last_bracket(query):
                        self.add_result(r)
        else:
            r = Result(Title='save-resize',
                       SubTitle="Save the current resize layout dimensions to a file",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'save-resize [', ['save-resize', '[']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def load_resize(self, query: str, state_j):

        load_resize_list = []

        first_word = get_first_word(query)

        if first_word == 'load-resize':

            load_resize = ''

            new_query = re.sub(r'\s+', ' ', query).strip()

            result_load_resize = Result(Title='load-resize',
                                        SubTitle="Save the current resize layout dimensions to a file",
                                        AutoCompleteText="load-resize",
                                        JsonRPCAction=JsonRPCAction(method="change",
                                                                    parameters=[query, "load-resize [ ",
                                                                                ['load-resize', "["]],
                                                                    dontHideAfterAction=True))

            if 'load-resize' in query:
                if re.search(r'\bload-resize\s*\[.*?\]', new_query):
                    matches = re.search(r'\bload-resize\s*\[(.*?)\]', query)
                    load_resize = matches.group(1).strip()
                    new_query = re.sub(r'\bload-resize\b\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("load-resize", "")
            else:
                if not word_before_last_bracket(query):
                    load_resize_list.append(result_load_resize)

            if word_before_last_bracket(query):
                word_before = word_before_last_bracket(query)

                if word_before == "load-resize":

                    new_query = new_query.strip().replace("[", "")
                    new_query = re.sub(r'\s+', ' ', new_query).strip()

                    if new_query == "":
                        everything_matches = everything_search("load-resize")
                    else:
                        everything_matches = everything_search(new_query)

                    if everything_matches:
                        for match in everything_matches:
                            match_result = Result(Title=match,
                                                  AutoCompleteText=match,
                                                  JsonRPCAction=JsonRPCAction(method="change",
                                                                              parameters=[query, match + " ]",
                                                                                          ['load-resize', '[']],
                                                                              dontHideAfterAction=True))

                            load_resize_list.append(match_result)
                    else:

                        if new_query == "":
                            matches = query_windows_search("load-resize")

                        else:
                            matches = query_windows_search(new_query)

                        if isinstance(matches, list):

                            for match in matches:
                                match_result = Result(Title=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=match['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, match + " ]",
                                                                                              ['load-resize', '[']],
                                                                                  dontHideAfterAction=True))

                                load_resize_list.append(match_result)
                        else:
                            if matches:
                                match_result = Result(Title=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      AutoCompleteText=matches['SYSTEM.ITEMPATHDISPLAY'],
                                                      JsonRPCAction=JsonRPCAction(method="change",
                                                                                  parameters=[query, matches + " ]",
                                                                                              ['load-resize', '[']],
                                                                                  dontHideAfterAction=True))

                                load_resize_list.append(match_result)

            rr = utils.score_results(new_query.strip(), load_resize_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

            load_resize_path = re.search(r'\s*load-resize\s*\[(.*?)\]', query)

            if load_resize_path:
                if not os.path.exists(load_resize_path.group(1).strip()):
                    self._results = [Result(Title='Path doenst exits')]

                else:
                    r = Result(Title='run',
                               SubTitle='run start command with this parameters')

                    r.JsonRPCAction = JsonRPCAction(method="load_resize",
                                                    parameters=[load_resize])

                    if not word_before_last_bracket(query):
                        self.add_result(r)
        else:
            r = Result(Title='load-resize',
                       SubTitle="Save the current resize layout dimensions to a file",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'load-resize [', ['load-resize', '[']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def display_monitor_workspace(self, query: str, state_j):

        display_monitor_workspace_list = []

        first_word = get_first_word(query)

        if first_word == "display-monitor-workspace":

            wk = re.search(r'\bworkspace\s*\[(.*?)\]', query)
            m = re.search(r'\bmonitor\s*\[(.*?)\]', query)

            new_query = query.strip().replace("display-monitor-workspace", "")
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            result_monitor = Result(Title='monitor',
                                    SubTitle="Monitor index (zero-indexed)",
                                    AutoCompleteText="monitor",
                                    JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "monitor [ ",
                                                                                             [
                                                                                                 'display-monitor-workspace',
                                                                                                 'monitor',
                                                                                                 'workspace']],
                                                                dontHideAfterAction=True))

            if ' monitor ' in query:
                if re.search(r'\bmonitor\s*\[.*?\]', new_query):
                    matches = re.search(r'\bmonitor\s*\[(.*?)\]', query)
                    monitor = matches.group(1).strip()
                    new_query = re.sub(r'\bmonitor\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("monitor", "")
            else:
                if not word_before_last_bracket(query):
                    display_monitor_workspace_list.append(result_monitor)

            result_workspace = Result(Title='workspace',
                                      SubTitle="Workspace index on the specified monitor (zero-indexed)",
                                      AutoCompleteText="monitor",
                                      JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "workspace [ ",
                                                                                               [
                                                                                                   'display-monitor-workspace',
                                                                                                   'monitor',
                                                                                                   'workspace']],
                                                                  dontHideAfterAction=True))

            if ' workspace ' in query:
                if re.search(r'\bworkspace\s*\[.*?\]', new_query):
                    matches = re.search(r'\bworkspace\s*\[(.*?)\]', query)
                    workspace = matches.group(1).strip()
                    new_query = re.sub(r'\bworkspace\s*\[.*?\]', '', new_query)
                    new_query = re.sub(r'\s+', ' ', new_query).strip()
                else:
                    new_query = new_query.strip().replace("workspace", "")
            else:
                if m and not word_before_last_bracket(query):
                    display_monitor_workspace_list.append(result_workspace)

            if word_before_last_bracket(query):
                word_before = word_before_last_bracket(query)

                if word_before == "monitor":

                    new_query = re.sub(r'\s*\[\s*', '', new_query)

                    monitor_index = len(state_j['monitors']['elements'])

                    if not new_query.strip().isdigit():
                        notdigit = Result(Title='Not a number needs to be a number')
                        self.add_result(notdigit)
                    elif monitor_index - 1 < int(new_query.strip()) or int(new_query.strip()) < 0:
                        outofindex = Result(Title='There is no monitor with that index')
                        self.add_result(outofindex)

                elif word_before == "workspace":

                    new_query = re.sub(r'\s*\[\s*', '', new_query)

                    workspace_index = len(state_j['monitors']['elements'][int(monitor)]['workspaces']['elements'])

                    if not new_query.strip().isdigit():
                        notdigit = Result(Title='Not a number needs to be a number')
                        self.add_result(notdigit)
                    elif workspace_index - 1 < int(new_query.strip()) or int(new_query.strip()) < 0:
                        outofindex = Result(Title='There is no workspace with that index')
                        self.add_result(outofindex)

            rr = utils.score_results(new_query.strip(), display_monitor_workspace_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

            if wk and m:
                r = Result(Title='run',
                           SubTitle='run start command with this parameters')

                r.JsonRPCAction = JsonRPCAction(method="display_monitor_workspace",
                                                parameters=[monitor, workspace])

                if not word_before_last_bracket(query):
                    self.add_result(r)

        else:
            r = Result(Title='display-monitor-workspace',
                       SubTitle="Display the workspace index at monitor index",
                       JsonRPCAction=JsonRPCAction(method="change",
                                                   parameters=[query, 'display-monitor-workspace',
                                                               ['display-monitor-workspace', 'monitor', 'workspace']],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def focus(self, query: str, state_j):

        focus_list = []

        first_word = get_first_word(query)

        if first_word == "focus":

            new_query = query.strip().replace('focus', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            left_result = Result(Title="left",
                                 SubTitle="",
                                 JsonRPCAction=JsonRPCAction(method="focus",
                                                             parameters=['left']))

            right_result = Result(Title="right",
                                  SubTitle="",
                                  JsonRPCAction=JsonRPCAction(method="focus",
                                                              parameters=['right']))

            up_result = Result(Title="up",
                               SubTitle="",
                               JsonRPCAction=JsonRPCAction(method="focus",
                                                           parameters=['up']))

            down_result = Result(Title="down",
                                 SubTitle="",
                                 JsonRPCAction=JsonRPCAction(method="focus",
                                                             parameters=['down']))

            focus_list.append(left_result)
            focus_list.append(right_result)
            focus_list.append(up_result)
            focus_list.append(down_result)

            rr = utils.score_results(new_query, focus_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)
        else:
            r = Result(Title="focus",
                       SubTitle="Change focus to the window in the specified direction",
                       JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "focus", ["focus"]],
                                                   dontHideAfterAction=True))

            rr = utils.score_results(query, [r], match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)

    def move(self, query: str, state_j):

        move_list = []

        first_word = get_first_word(query)

        if first_word == "move":

            new_query = query.strip().replace('move', '')
            new_query = re.sub(r'\s+', ' ', new_query).strip()

            left_result = Result(Title="left",
                                 SubTitle="",
                                 JsonRPCAction=JsonRPCAction(method="move",
                                                             parameters=['left']))

            right_result = Result(Title="right",
                                  SubTitle="",
                                  JsonRPCAction=JsonRPCAction(method="move",
                                                              parameters=['right']))

            up_result = Result(Title="up",
                               SubTitle="",
                               JsonRPCAction=JsonRPCAction(method="move",
                                                           parameters=['up']))

            down_result = Result(Title="down",
                                 SubTitle="",
                                 JsonRPCAction=JsonRPCAction(method="move",
                                                             parameters=['down']))

            move_list.append(left_result)
            move_list.append(right_result)
            move_list.append(up_result)
            move_list.append(down_result)

            rr = utils.score_results(new_query, move_list, match_on_empty_query=True)

            for scored_results in rr:
                self.add_result(scored_results)
        else:
            r = Result(Title="move",
                       SubTitle="Move the focused window in the specified direction",
                       JsonRPCAction=JsonRPCAction(method="change", parameters=[query, "move", ["move"]],
                                                   dontHideAfterAction=True))

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

    def __call__(self, query: str, word_to_check: str, stop_words: [str]) -> JsonRPCAction:
        query = "kc" + " " + query

        return api.change_query(query=append_if_matches(query, word_to_check, stop_words))


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

        return api.copy_to_clipboard(result.stdout)


class Configuration(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.configuration()

        return api.copy_to_clipboard(result.stdout)


class Whkdrc(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.whkdrc()

        return api.copy_to_clipboard(result.stdout)


class State(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.state()

        return api.copy_to_clipboard(result.stdout)


class Global_state(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.global_state()

        return api.copy_to_clipboard(result.stdout)


class Gui(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self):
        self.komorebic.gui()


class Visible_windows(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.visible_windows()

        return api.copy_to_clipboard(result.stdout)


class Copy_to_clipboard(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, text_to_copy) -> JsonRPCAction:
        return api.copy_to_clipboard(text_to_copy)


class Monitor_information(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self) -> JsonRPCAction:
        result = self.komorebic.monitor_information()

        return api.copy_to_clipboard(result.stdout)


class State_query(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, state_q: str) -> JsonRPCAction:
        result = self.komorebic.query(state_q)

        return api.copy_to_clipboard(result.stdout)


class Subscribe_socket(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, socket: str):
        self.komorebic.subscribe_socket(socket)


class Unsubscribe_socket(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, socket: str):
        self.komorebic.unsubscribe_socket(socket)


class Subscribe_pipe(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, named_pipe: str):
        self.komorebic.subscribe_pipe(named_pipe)


class Unsubscribe_pipe(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, named_pipe: str):
        self.komorebic.unsubscribe_pipe(named_pipe)


class Log(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self):
        subprocess.run(['start', 'cmd', '/k', self.komorebic.path, 'log'], shell=True)


class Quick_save_resize(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self):
        self.komorebic.quick_save_resize()


class Quick_load_resize(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self):
        self.komorebic.quick_load_resize()


class Save_resize(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, path: str):
        self.komorebic.save_resize(path)


class Load_resize(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, path: str):
        self.komorebic.load_resize(path)


class Display_monitor_workspace(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, monitor: str, workspace: str) -> JsonRPCAction:
        result = self.komorebic.display_monitor_workspace(MONITOR=monitor, WORKSPACE=workspace)

        return api.copy_to_clipboard(result.stderr)


class Focus(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, operation_direction: str) -> JsonRPCAction:
        result = self.komorebic.focus(operation_direction)

        return api.copy_to_clipboard(result.stderr)


class Move(Method):

    def __init__(self, komorebic: WKomorebic, pipe, pipename):
        super().__init__()
        self.komorebic = komorebic
        self.pipe = pipe
        self.pipename = pipename

    def __call__(self, operation_direction: str) -> JsonRPCAction:
        result = self.komorebic.move(operation_direction)

        return api.copy_to_clipboard(result.stderr)

