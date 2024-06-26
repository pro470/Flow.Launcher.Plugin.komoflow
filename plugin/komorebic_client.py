import subprocess

class WKomorebic:
    def __init__(self) -> None:
        self.path = 'komorebic.exe'
        pass
        
    def quickstart(self):
        subprocess.run(args=[self.path, 'quickstart'], shell=True)

    def start(self):
        subprocess.run(args=[self.path, 'start'], shell=True)

    def stop(self):
        subprocess.run(args=[self.path, 'stop'], shell=True)

    def check(self):
        subprocess.run(args=[self.path, 'check'], shell=True)

    def configuration(self):
        subprocess.run(args=[self.path, 'configuration'], shell=True)

    def whkdrc(self):
        subprocess.run(args=[self.path, 'whkdrc'], shell=True)

    def state(self):
        subprocess.run(args=[self.path, 'state'], shell=True)

    def global_state(self):
        subprocess.run(args=[self.path, 'global-state'], shell=True)

    def gui(self):
        subprocess.run(args=[self.path, 'gui'], shell=True)

    def visible_windows(self):
        subprocess.run(args=[self.path, 'visible-windows'], shell=True)

    def monitor_information(self):
        subprocess.run(args=[self.path, 'monitor-information'], shell=True)

    def query(self, STATE_QUERY):
        subprocess.run(args=[self.path, 'query', STATE_QUERY], shell=True)

    def subscribe_socket(self, SOCKET):
        subprocess.run(args=[self.path, 'subscribe-socket', SOCKET], shell=True)

    def unsubscribe_socket(self, SOCKET):
        subprocess.run(args=[self.path, 'unsubscribe-socket', SOCKET], shell=True)

    def subscribe_pipe(self, NAMED_PIPE):
        subprocess.run(args=[self.path, 'subscribe-pipe', NAMED_PIPE], shell=True)

    def unsubscribe_pipe(self, NAMED_PIPE):
        subprocess.run(args=[self.path, 'unsubscribe-pipe', NAMED_PIPE], shell=True)

    def log(self):
        subprocess.run(args=[self.path, 'log'], shell=True)

    def quick_save_resize(self):
        subprocess.run(args=[self.path, 'quick-save-resize'], shell=True)

    def quick_load_resize(self):
        subprocess.run(args=[self.path, 'quick-load-resize'], shell=True)

    def save_resize(self, PATH):
        subprocess.run(args=[self.path, 'save-resize', PATH], shell=True)

    def load_resize(self, PATH):
        subprocess.run(args=[self.path, 'load-resize', PATH], shell=True)

    def display_monitor_workspace(self, MONITOR):
        subprocess.run(args=[self.path, 'display-monitor-workspace', MONITOR], shell=True)

    def focus(self, OPERATION_DIRECTION):
        subprocess.run(args=[self.path, 'focus', OPERATION_DIRECTION], shell=True)

    def focus_exe(self):
        subprocess.run(args=[self.path, 'focus-exe'], shell=True)

    def move(self, OPERATION_DIRECTION):
        subprocess.run(args=[self.path, 'move', OPERATION_DIRECTION], shell=True)

    def minimize(self):
        subprocess.run(args=[self.path, 'minimize'], shell=True)

    def close(self):
        subprocess.run(args=[self.path, 'close'], shell=True)

    def force_focus(self):
        subprocess.run(args=[self.path, 'force-focus'], shell=True)

    def cycle_focus(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-focus', CYCLE_DIRECTION], shell=True)

    def cycle_move(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-move', CYCLE_DIRECTION], shell=True)

    def stack(self, OPERATION_DIRECTION):
        subprocess.run(args=[self.path, 'stack', OPERATION_DIRECTION], shell=True)

    def stack_all(self):
        subprocess.run(args=[self.path, 'stack-all'], shell=True)

    def unstack_all(self):
        subprocess.run(args=[self.path, 'unstack-all'], shell=True)

    def resize_edge(self, EDGE):
        subprocess.run(args=[self.path, 'resize-edge', EDGE], shell=True)

    def resize_axis(self, AXIS):
        subprocess.run(args=[self.path, 'resize-axis', AXIS], shell=True)

    def unstack(self):
        subprocess.run(args=[self.path, 'unstack'], shell=True)

    def cycle_stack(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-stack', CYCLE_DIRECTION], shell=True)

    def move_to_monitor(self, TARGET):
        subprocess.run(args=[self.path, 'move-to-monitor', TARGET], shell=True)

    def cycle_move_to_monitor(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-move-to-monitor', CYCLE_DIRECTION], shell=True)

    def move_to_workspace(self, TARGET):
        subprocess.run(args=[self.path, 'move-to-workspace', TARGET], shell=True)

    def move_to_named_workspace(self, WORKSPACE):
        subprocess.run(args=[self.path, 'move-to-named-workspace', WORKSPACE], shell=True)

    def cycle_move_to_workspace(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-move-to-workspace', CYCLE_DIRECTION], shell=True)

    def send_to_monitor(self, TARGET):
        subprocess.run(args=[self.path, 'send-to-monitor', TARGET], shell=True)

    def cycle_send_to_monitor(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-send-to-monitor', CYCLE_DIRECTION], shell=True)

    def send_to_workspace(self, TARGET):
        subprocess.run(args=[self.path, 'send-to-workspace', TARGET], shell=True)

    def send_to_named_workspace(self, WORKSPACE):
        subprocess.run(args=[self.path, 'send-to-named-workspace', WORKSPACE], shell=True)

    def cycle_send_to_workspace(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-send-to-workspace', CYCLE_DIRECTION], shell=True)

    def send_to_monitor_workspace(self, TARGET_MONITOR):
        subprocess.run(args=[self.path, 'send-to-monitor-workspace', TARGET_MONITOR], shell=True)

    def move_to_monitor_workspace(self, TARGET_MONITOR):
        subprocess.run(args=[self.path, 'move-to-monitor-workspace', TARGET_MONITOR], shell=True)

    def focus_monitor(self, TARGET):
        subprocess.run(args=[self.path, 'focus-monitor', TARGET], shell=True)

    def focus_last_workspace(self):
        subprocess.run(args=[self.path, 'focus-last-workspace'], shell=True)

    def focus_workspace(self, TARGET):
        subprocess.run(args=[self.path, 'focus-workspace', TARGET], shell=True)

    def focus_workspaces(self, TARGET):
        subprocess.run(args=[self.path, 'focus-workspaces', TARGET], shell=True)

    def focus_monitor_workspace(self, TARGET_MONITOR):
        subprocess.run(args=[self.path, 'focus-monitor-workspace', TARGET_MONITOR], shell=True)

    def focus_named_workspace(self, WORKSPACE):
        subprocess.run(args=[self.path, 'focus-named-workspace', WORKSPACE], shell=True)

    def cycle_monitor(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-monitor', CYCLE_DIRECTION], shell=True)

    def cycle_workspace(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-workspace', CYCLE_DIRECTION], shell=True)

    def move_workspace_to_monitor(self, TARGET):
        subprocess.run(args=[self.path, 'move-workspace-to-monitor', TARGET], shell=True)

    def cycle_move_workspace_to_monitor(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-move-workspace-to-monitor', CYCLE_DIRECTION], shell=True)

    def swap_workspaces_with_monitor(self, TARGET):
        subprocess.run(args=[self.path, 'swap-workspaces-with-monitor', TARGET], shell=True)

    def new_workspace(self):
        subprocess.run(args=[self.path, 'new-workspace'], shell=True)

    def resize_delta(self, PIXELS):
        subprocess.run(args=[self.path, 'resize-delta', PIXELS], shell=True)

    def invisible_borders(self, LEFT):
        subprocess.run(args=[self.path, 'invisible-borders', LEFT], shell=True)

    def global_work_area_offset(self, LEFT):
        subprocess.run(args=[self.path, 'global-work-area-offset', LEFT], shell=True)

    def monitor_work_area_offset(self, MONITOR):
        subprocess.run(args=[self.path, 'monitor-work-area-offset', MONITOR], shell=True)

    def focused_workspace_container_padding(self, SIZE):
        subprocess.run(args=[self.path, 'focused-workspace-container-padding', SIZE], shell=True)

    def focused_workspace_padding(self, SIZE):
        subprocess.run(args=[self.path, 'focused-workspace-padding', SIZE], shell=True)

    def adjust_container_padding(self, SIZING):
        subprocess.run(args=[self.path, 'adjust-container-padding', SIZING], shell=True)

    def adjust_workspace_padding(self, SIZING):
        subprocess.run(args=[self.path, 'adjust-workspace-padding', SIZING], shell=True)

    def change_layout(self, DEFAULT_LAYOUT):
        subprocess.run(args=[self.path, 'change-layout', DEFAULT_LAYOUT], shell=True)

    def cycle_layout(self, CYCLE_DIRECTION):
        subprocess.run(args=[self.path, 'cycle-layout', CYCLE_DIRECTION], shell=True)

    def load_custom_layout(self, PATH):
        subprocess.run(args=[self.path, 'load-custom-layout', PATH], shell=True)

    def flip_layout(self, AXIS):
        subprocess.run(args=[self.path, 'flip-layout', AXIS], shell=True)

    def promote(self):
        subprocess.run(args=[self.path, 'promote'], shell=True)

    def promote_focus(self):
        subprocess.run(args=[self.path, 'promote-focus'], shell=True)

    def promote_window(self, OPERATION_DIRECTION):
        subprocess.run(args=[self.path, 'promote-window', OPERATION_DIRECTION], shell=True)

    def retile(self):
        subprocess.run(args=[self.path, 'retile'], shell=True)

    def monitor_index_preference(self, INDEX_PREFERENCE):
        subprocess.run(args=[self.path, 'monitor-index-preference', INDEX_PREFERENCE], shell=True)

    def display_index_preference(self, INDEX_PREFERENCE):
        subprocess.run(args=[self.path, 'display-index-preference', INDEX_PREFERENCE], shell=True)

    def ensure_workspaces(self, MONITOR):
        subprocess.run(args=[self.path, 'ensure-workspaces', MONITOR], shell=True)

    def ensure_named_workspaces(self, MONITOR):
        subprocess.run(args=[self.path, 'ensure-named-workspaces', MONITOR], shell=True)

    def container_padding(self, MONITOR):
        subprocess.run(args=[self.path, 'container-padding', MONITOR], shell=True)

    def named_workspace_container_padding(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-container-padding', WORKSPACE], shell=True)

    def workspace_padding(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-padding', MONITOR], shell=True)

    def named_workspace_padding(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-padding', WORKSPACE], shell=True)

    def workspace_layout(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-layout', MONITOR], shell=True)

    def named_workspace_layout(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-layout', WORKSPACE], shell=True)

    def workspace_custom_layout(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-custom-layout', MONITOR], shell=True)

    def named_workspace_custom_layout(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-custom-layout', WORKSPACE], shell=True)

    def workspace_layout_rule(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-layout-rule', MONITOR], shell=True)

    def named_workspace_layout_rule(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-layout-rule', WORKSPACE], shell=True)

    def workspace_custom_layout_rule(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-custom-layout-rule', MONITOR], shell=True)

    def named_workspace_custom_layout_rule(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-custom-layout-rule', WORKSPACE], shell=True)

    def clear_workspace_layout_rules(self, MONITOR):
        subprocess.run(args=[self.path, 'clear-workspace-layout-rules', MONITOR], shell=True)

    def clear_named_workspace_layout_rules(self, WORKSPACE):
        subprocess.run(args=[self.path, 'clear-named-workspace-layout-rules', WORKSPACE], shell=True)

    def workspace_tiling(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-tiling', MONITOR], shell=True)

    def named_workspace_tiling(self, WORKSPACE):
        subprocess.run(args=[self.path, 'named-workspace-tiling', WORKSPACE], shell=True)

    def workspace_name(self, MONITOR):
        subprocess.run(args=[self.path, 'workspace-name', MONITOR], shell=True)

    def toggle_window_container_behaviour(self):
        subprocess.run(args=[self.path, 'toggle-window-container-behaviour'], shell=True)

    def toggle_pause(self):
        subprocess.run(args=[self.path, 'toggle-pause'], shell=True)

    def toggle_tiling(self):
        subprocess.run(args=[self.path, 'toggle-tiling'], shell=True)

    def toggle_float(self):
        subprocess.run(args=[self.path, 'toggle-float'], shell=True)

    def toggle_monocle(self):
        subprocess.run(args=[self.path, 'toggle-monocle'], shell=True)

    def toggle_maximize(self):
        subprocess.run(args=[self.path, 'toggle-maximize'], shell=True)

    def toggle_always_on_top(self):
        subprocess.run(args=[self.path, 'toggle-always-on-top'], shell=True)

    def restore_windows(self):
        subprocess.run(args=[self.path, 'restore-windows'], shell=True)

    def manage(self):
        subprocess.run(args=[self.path, 'manage'], shell=True)

    def unmanage(self):
        subprocess.run(args=[self.path, 'unmanage'], shell=True)

    def reload_configuration(self):
        subprocess.run(args=[self.path, 'reload-configuration'], shell=True)

    def watch_configuration(self, BOOLEAN_STATE):
        subprocess.run(args=[self.path, 'watch-configuration', BOOLEAN_STATE], shell=True)

    def complete_configuration(self):
        subprocess.run(args=[self.path, 'complete-configuration'], shell=True)

    def window_hiding_behaviour(self, HIDING_BEHAVIOUR):
        subprocess.run(args=[self.path, 'window-hiding-behaviour', HIDING_BEHAVIOUR], shell=True)

    def cross_monitor_move_behaviour(self, MOVE_BEHAVIOUR):
        subprocess.run(args=[self.path, 'cross-monitor-move-behaviour', MOVE_BEHAVIOUR], shell=True)

    def toggle_cross_monitor_move_behaviour(self):
        subprocess.run(args=[self.path, 'toggle-cross-monitor-move-behaviour'], shell=True)

    def unmanaged_window_operation_behaviour(self, OPERATION_BEHAVIOUR):
        subprocess.run(args=[self.path, 'unmanaged-window-operation-behaviour', OPERATION_BEHAVIOUR], shell=True)

    def float_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'float-rule', IDENTIFIER], shell=True)

    def manage_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'manage-rule', IDENTIFIER], shell=True)

    def initial_workspace_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'initial-workspace-rule', IDENTIFIER], shell=True)

    def initial_named_workspace_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'initial-named-workspace-rule', IDENTIFIER], shell=True)

    def workspace_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'workspace-rule', IDENTIFIER], shell=True)

    def named_workspace_rule(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'named-workspace-rule', IDENTIFIER], shell=True)

    def identify_object_name_change_application(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'identify-object-name-change-application', IDENTIFIER], shell=True)

    def identify_tray_application(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'identify-tray-application', IDENTIFIER], shell=True)

    def identify_layered_application(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'identify-layered-application', IDENTIFIER], shell=True)

    def remove_title_bar(self, IDENTIFIER):
        subprocess.run(args=[self.path, 'remove-title-bar', IDENTIFIER], shell=True)

    def toggle_title_bars(self):
        subprocess.run(args=[self.path, 'toggle-title-bars'], shell=True)

    def border(self, BOOLEAN_STATE):
        subprocess.run(args=[self.path, 'border', BOOLEAN_STATE], shell=True)

    def border_colour(self, R):
        subprocess.run(args=[self.path, 'border-colour', R], shell=True)

    def border_width(self, WIDTH):
        subprocess.run(args=[self.path, 'border-width', WIDTH], shell=True)

    def border_offset(self, OFFSET):
        subprocess.run(args=[self.path, 'border-offset', OFFSET], shell=True)

    def border_style(self, STYLE):
        subprocess.run(args=[self.path, 'border-style', STYLE], shell=True)

    def border_implementation(self, STYLE):
        subprocess.run(args=[self.path, 'border-implementation', STYLE], shell=True)

    def transparency(self, BOOLEAN_STATE):
        subprocess.run(args=[self.path, 'transparency', BOOLEAN_STATE], shell=True)

    def transparency_alpha(self, ALPHA):
        subprocess.run(args=[self.path, 'transparency-alpha', ALPHA], shell=True)

    def focus_follows_mouse(self, BOOLEAN_STATE):
        subprocess.run(args=[self.path, 'focus-follows-mouse', BOOLEAN_STATE], shell=True)

    def toggle_focus_follows_mouse(self):
        subprocess.run(args=[self.path, 'toggle-focus-follows-mouse'], shell=True)

    def mouse_follows_focus(self, BOOLEAN_STATE):
        subprocess.run(args=[self.path, 'mouse-follows-focus', BOOLEAN_STATE], shell=True)

    def toggle_mouse_follows_focus(self):
        subprocess.run(args=[self.path, 'toggle-mouse-follows-focus'], shell=True)

    def ahk_app_specific_configuration(self, PATH):
        subprocess.run(args=[self.path, 'ahk-app-specific-configuration', PATH], shell=True)

    def pwsh_app_specific_configuration(self, PATH):
        subprocess.run(args=[self.path, 'pwsh-app-specific-configuration', PATH], shell=True)

    def format_app_specific_configuration(self, PATH):
        subprocess.run(args=[self.path, 'format-app-specific-configuration', PATH], shell=True)

    def fetch_app_specific_configuration(self):
        subprocess.run(args=[self.path, 'fetch-app-specific-configuration'], shell=True)

    def application_specific_configuration_schema(self):
        subprocess.run(args=[self.path, 'application-specific-configuration-schema'], shell=True)

    def notification_schema(self):
        subprocess.run(args=[self.path, 'notification-schema'], shell=True)

    def socket_schema(self):
        subprocess.run(args=[self.path, 'socket-schema'], shell=True)

    def static_config_schema(self):
        subprocess.run(args=[self.path, 'static-config-schema'], shell=True)

    def generate_static_config(self):
        subprocess.run(args=[self.path, 'generate-static-config'], shell=True)

    def enable_autostart(self):
        subprocess.run(args=[self.path, 'enable-autostart'], shell=True)

    def disable_autostart(self):
        subprocess.run(args=[self.path, 'disable-autostart'], shell=True)


if __name__ == "__main__":
    tkomo = WKomorebic()
