from pyflowlauncher import Plugin
from methods import *
from utils import *

plugin = Plugin()

plugin.komorebic = WKomorebic()
plugin.pipename = 'komoflow'
plugin.pipe = create_named_pipe(plugin.pipename)

plugin.add_method(Query(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Context_menu(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(App_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
