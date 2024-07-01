from pyflowlauncher import Plugin
from komorebic_client import WKomorebic
from methods import Query, Context_menu, App_focus
from utils import create_named_pipe

plugin = Plugin()

plugin.komorebic = WKomorebic()
plugin.pipename = 'komoflow'
plugin.pipe = create_named_pipe(plugin.pipename)

plugin.add_method(Query(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Context_menu(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(App_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
