from pyflowlauncher import Plugin
from komorebic_client import WKomorebic
from methods import Query, Context_menu, App_focus, Quickstart, Start, Change, Stop, Check, Configuration, State, \
    Global_state, Gui, Visible_windows, Copy_to_clipboard, Monitor_information, State_query, Subscribe_socket, \
    Unsubscribe_socket, \
    Subscribe_pipe, Unsubscribe_pipe, Log, Quick_save_resize, Quick_load_resize, Save_resize, Load_resize, \
    Display_monitor_workspace, \
    Focus, Move, Minimize, Run, Force_focus, Cycle_focus, Cycle_move, Stack, Stack_all, Unstack_all, Resize_edge, \
    Resize_axis, Unstack, Cycle_stack, Move_to_monitor, Cycle_move_to_monitor, Move_to_workspace, Cycle_move_to_workspace,\
    Move_to_named_workspace, Send_to_monitor, Cycle_send_to_monitor, Send_to_workspace
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
plugin.add_method(State(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Global_state(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Gui(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Visible_windows(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Copy_to_clipboard(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Monitor_information(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(State_query(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Subscribe_socket(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Unsubscribe_socket(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Subscribe_pipe(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Unsubscribe_pipe(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Log(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Quick_save_resize(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Quick_load_resize(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Save_resize(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Load_resize(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Display_monitor_workspace(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Focus(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Move(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Minimize(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Run(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Force_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_focus(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_move(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Stack(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Stack_all(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Unstack_all(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Resize_edge(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Resize_axis(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Unstack(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_stack(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Move_to_monitor(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_move_to_monitor(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Move_to_workspace(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Move_to_named_workspace(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_move_to_workspace(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Send_to_monitor(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Cycle_send_to_monitor(plugin.komorebic, plugin.pipe, plugin.pipename))
plugin.add_method(Send_to_workspace(plugin.komorebic, plugin.pipe, plugin.pipename))

plugin.add_method(Change(plugin.settings, plugin.root_dir()))
