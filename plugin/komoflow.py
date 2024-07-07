from pyflowlauncher import Plugin
from komorebic_client import WKomorebic
from methods import Query, Context_menu, App_focus, Quickstart, Start, Change, Stop, Check, Configuration, State, \
    Global_state, Gui
from utils import create_named_pipe, exit_komoflow, connect_komorebi


class Komoflow(Plugin):
    komorebic = WKomorebic()
    pipename = 'komoflow'
    pipe = create_named_pipe(pipename)
    connect_komorebi(komorebic, pipename)

    def __init__(self):
        super().__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pipe:
            exit_komoflow(self.komorebic, self.pipe, self.pipename)


plugin = Komoflow()

plugin.add_method(Query(plugin.komorebic, plugin.pipe, plugin.pipename, plugin.root_dir()))
plugin.add_method(Context_menu(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(App_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Quickstart(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Start(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Stop(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Check(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Configuration(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(State(plugin.komorebic,plugin.pipe, plugin.pipename))
plugin.add_method(Global_state(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Gui(plugin.komorebic, plugin.pipe, plugin.pipename))

plugin.add_method(Change(plugin.settings))
