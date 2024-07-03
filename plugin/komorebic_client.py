import subprocess 
from typing import Iterable, Optional, Any
 

class WKomorebic:
    def __init__(self) -> None:
        self.path = 'komorebic.exe'
        pass
        
    def quickstart(self):
        cmd = [self.path, 'quickstart']
        subprocess.run(args=cmd, shell=True)

    def start(self, ffm: bool = False, config: Optional[Iterable[Any]] = None, await_configuration: bool = False, tcp_port: Optional[Iterable[Any]] = None, whkd: bool = False, ahk: bool = False):
        cmd = [self.path, 'start']
        if ffm: 
            cmd.extend(['--ffm'])
        if config:
            cmd.extend(['--config'])
            cmd.extend(config)
        if await_configuration: 
            cmd.extend(['--await-configuration'])
        if tcp_port:
            cmd.extend(['--tcp-port'])
            cmd.extend(tcp_port)
        if whkd: 
            cmd.extend(['--whkd'])
        if ahk: 
            cmd.extend(['--ahk'])
        subprocess.run(args=cmd, shell=True)

    def stop(self, whkd: bool = False):
        cmd = [self.path, 'stop']
        if whkd: 
            cmd.extend(['--whkd'])
        subprocess.run(args=cmd, shell=True)

    def check(self):
        cmd = [self.path, 'check']
        subprocess.run(args=cmd, shell=True)

    def configuration(self):
        cmd = [self.path, 'configuration']
        subprocess.run(args=cmd, shell=True)

    def whkdrc(self):
        cmd = [self.path, 'whkdrc']
        subprocess.run(args=cmd, shell=True)

    def state(self):
        cmd = [self.path, 'state']
        subprocess.run(args=cmd, shell=True)

    def global_state(self):
        cmd = [self.path, 'global-state']
        subprocess.run(args=cmd, shell=True)

    def gui(self):
        cmd = [self.path, 'gui']
        subprocess.run(args=cmd, shell=True)

    def visible_windows(self):
        cmd = [self.path, 'visible-windows']
        subprocess.run(args=cmd, shell=True)

    def monitor_information(self):
        cmd = [self.path, 'monitor-information']
        subprocess.run(args=cmd, shell=True)

    def query(self, STATE_QUERY):
        cmd = [self.path, 'query', STATE_QUERY]
        subprocess.run(args=cmd, shell=True)

    def subscribe_socket(self, SOCKET):
        cmd = [self.path, 'subscribe-socket', SOCKET]
        subprocess.run(args=cmd, shell=True)

    def unsubscribe_socket(self, SOCKET):
        cmd = [self.path, 'unsubscribe-socket', SOCKET]
        subprocess.run(args=cmd, shell=True)

    def subscribe_pipe(self, NAMED_PIPE):
        cmd = [self.path, 'subscribe-pipe', NAMED_PIPE]
        subprocess.run(args=cmd, shell=True)

    def unsubscribe_pipe(self, NAMED_PIPE):
        cmd = [self.path, 'unsubscribe-pipe', NAMED_PIPE]
        subprocess.run(args=cmd, shell=True)

    def log(self):
        cmd = [self.path, 'log']
        subprocess.run(args=cmd, shell=True)

    def quick_save_resize(self):
        cmd = [self.path, 'quick-save-resize']
        subprocess.run(args=cmd, shell=True)

    def quick_load_resize(self):
        cmd = [self.path, 'quick-load-resize']
        subprocess.run(args=cmd, shell=True)

    def save_resize(self, PATH):
        cmd = [self.path, 'save-resize', PATH]
        subprocess.run(args=cmd, shell=True)

    def load_resize(self, PATH):
        cmd = [self.path, 'load-resize', PATH]
        subprocess.run(args=cmd, shell=True)

    def display_monitor_workspace(self, MONITOR, WORKSPACE):
        cmd = [self.path, 'display-monitor-workspace', MONITOR, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def focus(self, OPERATION_DIRECTION):
        cmd = [self.path, 'focus', OPERATION_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def focus_exe(self, exe: Optional[Iterable[Any]] = None, hwnd: Optional[Iterable[Any]] = None):
        cmd = [self.path, 'focus-exe']
        if exe:
            cmd.extend(['--exe'])
            cmd.extend(exe)
        if hwnd:
            cmd.extend(['--hwnd'])
            cmd.extend(hwnd)
        subprocess.run(args=cmd, shell=True)

    def move(self, OPERATION_DIRECTION):
        cmd = [self.path, 'move', OPERATION_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def minimize(self):
        cmd = [self.path, 'minimize']
        subprocess.run(args=cmd, shell=True)

    def close(self):
        cmd = [self.path, 'close']
        subprocess.run(args=cmd, shell=True)

    def force_focus(self):
        cmd = [self.path, 'force-focus']
        subprocess.run(args=cmd, shell=True)

    def cycle_focus(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-focus', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def cycle_move(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-move', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def stack(self, OPERATION_DIRECTION):
        cmd = [self.path, 'stack', OPERATION_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def stack_all(self):
        cmd = [self.path, 'stack-all']
        subprocess.run(args=cmd, shell=True)

    def unstack_all(self):
        cmd = [self.path, 'unstack-all']
        subprocess.run(args=cmd, shell=True)

    def resize_edge(self, EDGE, SIZING):
        cmd = [self.path, 'resize-edge', EDGE, SIZING]
        subprocess.run(args=cmd, shell=True)

    def resize_axis(self, AXIS, SIZING):
        cmd = [self.path, 'resize-axis', AXIS, SIZING]
        subprocess.run(args=cmd, shell=True)

    def unstack(self):
        cmd = [self.path, 'unstack']
        subprocess.run(args=cmd, shell=True)

    def cycle_stack(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-stack', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def move_to_monitor(self, TARGET):
        cmd = [self.path, 'move-to-monitor', TARGET]
        subprocess.run(args=cmd, shell=True)

    def cycle_move_to_monitor(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-move-to-monitor', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def move_to_workspace(self, TARGET):
        cmd = [self.path, 'move-to-workspace', TARGET]
        subprocess.run(args=cmd, shell=True)

    def move_to_named_workspace(self, WORKSPACE):
        cmd = [self.path, 'move-to-named-workspace', WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def cycle_move_to_workspace(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-move-to-workspace', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def send_to_monitor(self, TARGET):
        cmd = [self.path, 'send-to-monitor', TARGET]
        subprocess.run(args=cmd, shell=True)

    def cycle_send_to_monitor(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-send-to-monitor', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def send_to_workspace(self, TARGET):
        cmd = [self.path, 'send-to-workspace', TARGET]
        subprocess.run(args=cmd, shell=True)

    def send_to_named_workspace(self, WORKSPACE):
        cmd = [self.path, 'send-to-named-workspace', WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def cycle_send_to_workspace(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-send-to-workspace', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def send_to_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE):
        cmd = [self.path, 'send-to-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def move_to_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE):
        cmd = [self.path, 'move-to-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def focus_monitor(self, TARGET):
        cmd = [self.path, 'focus-monitor', TARGET]
        subprocess.run(args=cmd, shell=True)

    def focus_last_workspace(self):
        cmd = [self.path, 'focus-last-workspace']
        subprocess.run(args=cmd, shell=True)

    def focus_workspace(self, TARGET):
        cmd = [self.path, 'focus-workspace', TARGET]
        subprocess.run(args=cmd, shell=True)

    def focus_workspaces(self, TARGET):
        cmd = [self.path, 'focus-workspaces', TARGET]
        subprocess.run(args=cmd, shell=True)

    def focus_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE):
        cmd = [self.path, 'focus-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def focus_named_workspace(self, WORKSPACE):
        cmd = [self.path, 'focus-named-workspace', WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def cycle_monitor(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-monitor', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def cycle_workspace(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-workspace', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def move_workspace_to_monitor(self, TARGET):
        cmd = [self.path, 'move-workspace-to-monitor', TARGET]
        subprocess.run(args=cmd, shell=True)

    def cycle_move_workspace_to_monitor(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-move-workspace-to-monitor', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def swap_workspaces_with_monitor(self, TARGET):
        cmd = [self.path, 'swap-workspaces-with-monitor', TARGET]
        subprocess.run(args=cmd, shell=True)

    def new_workspace(self):
        cmd = [self.path, 'new-workspace']
        subprocess.run(args=cmd, shell=True)

    def resize_delta(self, PIXELS):
        cmd = [self.path, 'resize-delta', PIXELS]
        subprocess.run(args=cmd, shell=True)

    def invisible_borders(self, LEFT, TOP, RIGHT, BOTTOM):
        cmd = [self.path, 'invisible-borders', LEFT, TOP, RIGHT, BOTTOM]
        subprocess.run(args=cmd, shell=True)

    def global_work_area_offset(self, LEFT, TOP, RIGHT, BOTTOM):
        cmd = [self.path, 'global-work-area-offset', LEFT, TOP, RIGHT, BOTTOM]
        subprocess.run(args=cmd, shell=True)

    def monitor_work_area_offset(self, MONITOR, LEFT, TOP, RIGHT, BOTTOM):
        cmd = [self.path, 'monitor-work-area-offset', MONITOR, LEFT, TOP, RIGHT, BOTTOM]
        subprocess.run(args=cmd, shell=True)

    def focused_workspace_container_padding(self, SIZE):
        cmd = [self.path, 'focused-workspace-container-padding', SIZE]
        subprocess.run(args=cmd, shell=True)

    def focused_workspace_padding(self, SIZE):
        cmd = [self.path, 'focused-workspace-padding', SIZE]
        subprocess.run(args=cmd, shell=True)

    def adjust_container_padding(self, SIZING, ADJUSTMENT):
        cmd = [self.path, 'adjust-container-padding', SIZING, ADJUSTMENT]
        subprocess.run(args=cmd, shell=True)

    def adjust_workspace_padding(self, SIZING, ADJUSTMENT):
        cmd = [self.path, 'adjust-workspace-padding', SIZING, ADJUSTMENT]
        subprocess.run(args=cmd, shell=True)

    def change_layout(self, DEFAULT_LAYOUT):
        cmd = [self.path, 'change-layout', DEFAULT_LAYOUT]
        subprocess.run(args=cmd, shell=True)

    def cycle_layout(self, CYCLE_DIRECTION):
        cmd = [self.path, 'cycle-layout', CYCLE_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def load_custom_layout(self, PATH):
        cmd = [self.path, 'load-custom-layout', PATH]
        subprocess.run(args=cmd, shell=True)

    def flip_layout(self, AXIS):
        cmd = [self.path, 'flip-layout', AXIS]
        subprocess.run(args=cmd, shell=True)

    def promote(self):
        cmd = [self.path, 'promote']
        subprocess.run(args=cmd, shell=True)

    def promote_focus(self):
        cmd = [self.path, 'promote-focus']
        subprocess.run(args=cmd, shell=True)

    def promote_window(self, OPERATION_DIRECTION):
        cmd = [self.path, 'promote-window', OPERATION_DIRECTION]
        subprocess.run(args=cmd, shell=True)

    def retile(self):
        cmd = [self.path, 'retile']
        subprocess.run(args=cmd, shell=True)

    def monitor_index_preference(self, INDEX_PREFERENCE, LEFT, TOP, RIGHT, BOTTOM):
        cmd = [self.path, 'monitor-index-preference', INDEX_PREFERENCE, LEFT, TOP, RIGHT, BOTTOM]
        subprocess.run(args=cmd, shell=True)

    def display_index_preference(self, INDEX_PREFERENCE, DISPLAY):
        cmd = [self.path, 'display-index-preference', INDEX_PREFERENCE, DISPLAY]
        subprocess.run(args=cmd, shell=True)

    def ensure_workspaces(self, MONITOR, WORKSPACE_COUNT):
        cmd = [self.path, 'ensure-workspaces', MONITOR, WORKSPACE_COUNT]
        subprocess.run(args=cmd, shell=True)

    def ensure_named_workspaces(self, MONITOR):
        cmd = [self.path, 'ensure-named-workspaces', MONITOR]
        subprocess.run(args=cmd, shell=True)

    def container_padding(self, MONITOR, WORKSPACE, SIZE):
        cmd = [self.path, 'container-padding', MONITOR, WORKSPACE, SIZE]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_container_padding(self, WORKSPACE, SIZE):
        cmd = [self.path, 'named-workspace-container-padding', WORKSPACE, SIZE]
        subprocess.run(args=cmd, shell=True)

    def workspace_padding(self, MONITOR, WORKSPACE, SIZE):
        cmd = [self.path, 'workspace-padding', MONITOR, WORKSPACE, SIZE]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_padding(self, WORKSPACE, SIZE):
        cmd = [self.path, 'named-workspace-padding', WORKSPACE, SIZE]
        subprocess.run(args=cmd, shell=True)

    def workspace_layout(self, MONITOR, WORKSPACE, VALUE):
        cmd = [self.path, 'workspace-layout', MONITOR, WORKSPACE, VALUE]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_layout(self, WORKSPACE, VALUE):
        cmd = [self.path, 'named-workspace-layout', WORKSPACE, VALUE]
        subprocess.run(args=cmd, shell=True)

    def workspace_custom_layout(self, MONITOR, WORKSPACE, PATH):
        cmd = [self.path, 'workspace-custom-layout', MONITOR, WORKSPACE, PATH]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_custom_layout(self, WORKSPACE, PATH):
        cmd = [self.path, 'named-workspace-custom-layout', WORKSPACE, PATH]
        subprocess.run(args=cmd, shell=True)

    def workspace_layout_rule(self, MONITOR, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT):
        cmd = [self.path, 'workspace-layout-rule', MONITOR, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_layout_rule(self, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT):
        cmd = [self.path, 'named-workspace-layout-rule', WORKSPACE, AT_CONTAINER_COUNT, LAYOUT]
        subprocess.run(args=cmd, shell=True)

    def workspace_custom_layout_rule(self, MONITOR, WORKSPACE, AT_CONTAINER_COUNT, PATH):
        cmd = [self.path, 'workspace-custom-layout-rule', MONITOR, WORKSPACE, AT_CONTAINER_COUNT, PATH]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_custom_layout_rule(self, WORKSPACE, AT_CONTAINER_COUNT, PATH):
        cmd = [self.path, 'named-workspace-custom-layout-rule', WORKSPACE, AT_CONTAINER_COUNT, PATH]
        subprocess.run(args=cmd, shell=True)

    def clear_workspace_layout_rules(self, MONITOR, WORKSPACE):
        cmd = [self.path, 'clear-workspace-layout-rules', MONITOR, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def clear_named_workspace_layout_rules(self, WORKSPACE):
        cmd = [self.path, 'clear-named-workspace-layout-rules', WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def workspace_tiling(self, MONITOR, WORKSPACE, VALUE):
        cmd = [self.path, 'workspace-tiling', MONITOR, WORKSPACE, VALUE]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_tiling(self, WORKSPACE, VALUE):
        cmd = [self.path, 'named-workspace-tiling', WORKSPACE, VALUE]
        subprocess.run(args=cmd, shell=True)

    def workspace_name(self, MONITOR, WORKSPACE, VALUE):
        cmd = [self.path, 'workspace-name', MONITOR, WORKSPACE, VALUE]
        subprocess.run(args=cmd, shell=True)

    def toggle_window_container_behaviour(self):
        cmd = [self.path, 'toggle-window-container-behaviour']
        subprocess.run(args=cmd, shell=True)

    def toggle_pause(self):
        cmd = [self.path, 'toggle-pause']
        subprocess.run(args=cmd, shell=True)

    def toggle_tiling(self):
        cmd = [self.path, 'toggle-tiling']
        subprocess.run(args=cmd, shell=True)

    def toggle_float(self):
        cmd = [self.path, 'toggle-float']
        subprocess.run(args=cmd, shell=True)

    def toggle_monocle(self):
        cmd = [self.path, 'toggle-monocle']
        subprocess.run(args=cmd, shell=True)

    def toggle_maximize(self):
        cmd = [self.path, 'toggle-maximize']
        subprocess.run(args=cmd, shell=True)

    def toggle_always_on_top(self):
        cmd = [self.path, 'toggle-always-on-top']
        subprocess.run(args=cmd, shell=True)

    def restore_windows(self):
        cmd = [self.path, 'restore-windows']
        subprocess.run(args=cmd, shell=True)

    def manage(self):
        cmd = [self.path, 'manage']
        subprocess.run(args=cmd, shell=True)

    def unmanage(self):
        cmd = [self.path, 'unmanage']
        subprocess.run(args=cmd, shell=True)

    def reload_configuration(self):
        cmd = [self.path, 'reload-configuration']
        subprocess.run(args=cmd, shell=True)

    def watch_configuration(self, BOOLEAN_STATE):
        cmd = [self.path, 'watch-configuration', BOOLEAN_STATE]
        subprocess.run(args=cmd, shell=True)

    def complete_configuration(self):
        cmd = [self.path, 'complete-configuration']
        subprocess.run(args=cmd, shell=True)

    def window_hiding_behaviour(self, HIDING_BEHAVIOUR):
        cmd = [self.path, 'window-hiding-behaviour', HIDING_BEHAVIOUR]
        subprocess.run(args=cmd, shell=True)

    def cross_monitor_move_behaviour(self, MOVE_BEHAVIOUR):
        cmd = [self.path, 'cross-monitor-move-behaviour', MOVE_BEHAVIOUR]
        subprocess.run(args=cmd, shell=True)

    def toggle_cross_monitor_move_behaviour(self):
        cmd = [self.path, 'toggle-cross-monitor-move-behaviour']
        subprocess.run(args=cmd, shell=True)

    def unmanaged_window_operation_behaviour(self, OPERATION_BEHAVIOUR):
        cmd = [self.path, 'unmanaged-window-operation-behaviour', OPERATION_BEHAVIOUR]
        subprocess.run(args=cmd, shell=True)

    def float_rule(self, IDENTIFIER, ID):
        cmd = [self.path, 'float-rule', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def manage_rule(self, IDENTIFIER, ID):
        cmd = [self.path, 'manage-rule', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def initial_workspace_rule(self, IDENTIFIER, ID, MONITOR, WORKSPACE):
        cmd = [self.path, 'initial-workspace-rule', IDENTIFIER, ID, MONITOR, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def initial_named_workspace_rule(self, IDENTIFIER, ID, WORKSPACE):
        cmd = [self.path, 'initial-named-workspace-rule', IDENTIFIER, ID, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def workspace_rule(self, IDENTIFIER, ID, MONITOR, WORKSPACE):
        cmd = [self.path, 'workspace-rule', IDENTIFIER, ID, MONITOR, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def named_workspace_rule(self, IDENTIFIER, ID, WORKSPACE):
        cmd = [self.path, 'named-workspace-rule', IDENTIFIER, ID, WORKSPACE]
        subprocess.run(args=cmd, shell=True)

    def identify_object_name_change_application(self, IDENTIFIER, ID):
        cmd = [self.path, 'identify-object-name-change-application', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def identify_tray_application(self, IDENTIFIER, ID):
        cmd = [self.path, 'identify-tray-application', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def identify_layered_application(self, IDENTIFIER, ID):
        cmd = [self.path, 'identify-layered-application', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def remove_title_bar(self, IDENTIFIER, ID):
        cmd = [self.path, 'remove-title-bar', IDENTIFIER, ID]
        subprocess.run(args=cmd, shell=True)

    def toggle_title_bars(self):
        cmd = [self.path, 'toggle-title-bars']
        subprocess.run(args=cmd, shell=True)

    def border(self, BOOLEAN_STATE):
        cmd = [self.path, 'border', BOOLEAN_STATE]
        subprocess.run(args=cmd, shell=True)

    def border_colour(self, R, G, B, window_kind: Optional[Iterable[Any]] = None):
        cmd = [self.path, 'border-colour', R, G, B]
        if window_kind:
            cmd.extend(['--window-kind'])
            cmd.extend(window_kind)
        subprocess.run(args=cmd, shell=True)

    def border_width(self, WIDTH):
        cmd = [self.path, 'border-width', WIDTH]
        subprocess.run(args=cmd, shell=True)

    def border_offset(self, OFFSET):
        cmd = [self.path, 'border-offset', OFFSET]
        subprocess.run(args=cmd, shell=True)

    def border_style(self, STYLE):
        cmd = [self.path, 'border-style', STYLE]
        subprocess.run(args=cmd, shell=True)

    def border_implementation(self, STYLE):
        cmd = [self.path, 'border-implementation', STYLE]
        subprocess.run(args=cmd, shell=True)

    def transparency(self, BOOLEAN_STATE):
        cmd = [self.path, 'transparency', BOOLEAN_STATE]
        subprocess.run(args=cmd, shell=True)

    def transparency_alpha(self, ALPHA):
        cmd = [self.path, 'transparency-alpha', ALPHA]
        subprocess.run(args=cmd, shell=True)

    def focus_follows_mouse(self, BOOLEAN_STATE, implementation: Optional[Iterable[Any]] = None):
        cmd = [self.path, 'focus-follows-mouse', BOOLEAN_STATE]
        if implementation:
            cmd.extend(['--implementation'])
            cmd.extend(implementation)
        subprocess.run(args=cmd, shell=True)

    def toggle_focus_follows_mouse(self, implementation: Optional[Iterable[Any]] = None):
        cmd = [self.path, 'toggle-focus-follows-mouse']
        if implementation:
            cmd.extend(['--implementation'])
            cmd.extend(implementation)
        subprocess.run(args=cmd, shell=True)

    def mouse_follows_focus(self, BOOLEAN_STATE):
        cmd = [self.path, 'mouse-follows-focus', BOOLEAN_STATE]
        subprocess.run(args=cmd, shell=True)

    def toggle_mouse_follows_focus(self):
        cmd = [self.path, 'toggle-mouse-follows-focus']
        subprocess.run(args=cmd, shell=True)

    def ahk_app_specific_configuration(self, PATH):
        cmd = [self.path, 'ahk-app-specific-configuration', PATH]
        subprocess.run(args=cmd, shell=True)

    def pwsh_app_specific_configuration(self, PATH):
        cmd = [self.path, 'pwsh-app-specific-configuration', PATH]
        subprocess.run(args=cmd, shell=True)

    def format_app_specific_configuration(self, PATH):
        cmd = [self.path, 'format-app-specific-configuration', PATH]
        subprocess.run(args=cmd, shell=True)

    def fetch_app_specific_configuration(self):
        cmd = [self.path, 'fetch-app-specific-configuration']
        subprocess.run(args=cmd, shell=True)

    def application_specific_configuration_schema(self):
        cmd = [self.path, 'application-specific-configuration-schema']
        subprocess.run(args=cmd, shell=True)

    def notification_schema(self):
        cmd = [self.path, 'notification-schema']
        subprocess.run(args=cmd, shell=True)

    def socket_schema(self):
        cmd = [self.path, 'socket-schema']
        subprocess.run(args=cmd, shell=True)

    def static_config_schema(self):
        cmd = [self.path, 'static-config-schema']
        subprocess.run(args=cmd, shell=True)

    def generate_static_config(self):
        cmd = [self.path, 'generate-static-config']
        subprocess.run(args=cmd, shell=True)

    def enable_autostart(self, config: Optional[Iterable[Any]] = None, ffm: bool = False, whkd: bool = False, ahk: bool = False):
        cmd = [self.path, 'enable-autostart']
        if config:
            cmd.extend(['--config'])
            cmd.extend(config)
        if ffm: 
            cmd.extend(['--ffm'])
        if whkd: 
            cmd.extend(['--whkd'])
        if ahk: 
            cmd.extend(['--ahk'])
        subprocess.run(args=cmd, shell=True)

    def disable_autostart(self):
        cmd = [self.path, 'disable-autostart']
        subprocess.run(args=cmd, shell=True)


if __name__ == "__main__":
    tkomo = WKomorebic()
