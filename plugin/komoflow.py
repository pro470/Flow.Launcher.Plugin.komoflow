from pyflowlauncher import Plugin
from komorebic_client import WKomorebic
from methods import Query, Context_menu, App_focus, Quickstart, Start, Change
from utils import create_named_pipe, exit_komoflow, connect_komorebi


class Komoflow(Plugin):

    def __init__(self):
        super().__init__()
        self.komorebic = WKomorebic()
        self.pipename = 'komoflow'
        self.pipe = create_named_pipe(self.pipename)
        connect_komorebi(self.komorebic, self.pipename)

    def __del__(self):
        exit_komoflow(self.komorebic, self.pipe, self.pipename)


plugin = Komoflow()

plugin.add_method(Query(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Context_menu(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(App_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Quickstart(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Start(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Change(plugin.settings))
