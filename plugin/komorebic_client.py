from subprocess import run, CompletedProcess 
from typing import Iterable, Optional, Any
 

class WKomorebic:
    def __init__(self) -> None:
        self.path = 'komorebic.exe'
        pass
        
    def quickstart(self) -> CompletedProcess[str]:
        cmd = [self.path, 'quickstart']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def start(self, config: Optional[Iterable[Any]] = None, await_configuration: bool = False, tcp_port: Optional[Iterable[Any]] = None, whkd: bool = False, ahk: bool = False, bar: bool = False, masir: bool = False, clean_state: bool = False) -> CompletedProcess[str]:
        cmd = [self.path, 'start']
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
        if bar: 
            cmd.extend(['--bar'])
        if masir: 
            cmd.extend(['--masir'])
        if clean_state: 
            cmd.extend(['--clean-state'])
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def stop(self, whkd: bool = False, ahk: bool = False, bar: bool = False, masir: bool = False) -> CompletedProcess[str]:
        cmd = [self.path, 'stop']
        if whkd: 
            cmd.extend(['--whkd'])
        if ahk: 
            cmd.extend(['--ahk'])
        if bar: 
            cmd.extend(['--bar'])
        if masir: 
            cmd.extend(['--masir'])
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def kill(self, whkd: bool = False, ahk: bool = False, bar: bool = False, masir: bool = False) -> CompletedProcess[str]:
        cmd = [self.path, 'kill']
        if whkd: 
            cmd.extend(['--whkd'])
        if ahk: 
            cmd.extend(['--ahk'])
        if bar: 
            cmd.extend(['--bar'])
        if masir: 
            cmd.extend(['--masir'])
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def check(self, komorebi_config: Optional[Iterable[Any]] = None) -> CompletedProcess[str]:
        cmd = [self.path, 'check']
        if komorebi_config:
            cmd.extend(['--komorebi-config'])
            cmd.extend(komorebi_config)
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def configuration(self) -> CompletedProcess[str]:
        cmd = [self.path, 'configuration']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def bar_configuration(self) -> CompletedProcess[str]:
        cmd = [self.path, 'bar-configuration']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def whkdrc(self) -> CompletedProcess[str]:
        cmd = [self.path, 'whkdrc']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def state(self) -> CompletedProcess[str]:
        cmd = [self.path, 'state']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def global_state(self) -> CompletedProcess[str]:
        cmd = [self.path, 'global-state']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def gui(self) -> CompletedProcess[str]:
        cmd = [self.path, 'gui']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def visible_windows(self) -> CompletedProcess[str]:
        cmd = [self.path, 'visible-windows']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def monitor_information(self) -> CompletedProcess[str]:
        cmd = [self.path, 'monitor-information']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def query(self, STATE_QUERY) -> CompletedProcess[str]:
        cmd = [self.path, 'query', STATE_QUERY]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def subscribe_socket(self, SOCKET) -> CompletedProcess[str]:
        cmd = [self.path, 'subscribe-socket', SOCKET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unsubscribe_socket(self, SOCKET) -> CompletedProcess[str]:
        cmd = [self.path, 'unsubscribe-socket', SOCKET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def subscribe_pipe(self, NAMED_PIPE) -> CompletedProcess[str]:
        cmd = [self.path, 'subscribe-pipe', NAMED_PIPE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unsubscribe_pipe(self, NAMED_PIPE) -> CompletedProcess[str]:
        cmd = [self.path, 'unsubscribe-pipe', NAMED_PIPE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def log(self) -> CompletedProcess[str]:
        cmd = [self.path, 'log']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def quick_save_resize(self) -> CompletedProcess[str]:
        cmd = [self.path, 'quick-save-resize']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def quick_load_resize(self) -> CompletedProcess[str]:
        cmd = [self.path, 'quick-load-resize']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def save_resize(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'save-resize', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def load_resize(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'load-resize', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus(self, OPERATION_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'focus', OPERATION_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move(self, OPERATION_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'move', OPERATION_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def minimize(self) -> CompletedProcess[str]:
        cmd = [self.path, 'minimize']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def close(self) -> CompletedProcess[str]:
        cmd = [self.path, 'close']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def force_focus(self) -> CompletedProcess[str]:
        cmd = [self.path, 'force-focus']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_focus(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-focus', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_move(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-move', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def eager_focus(self, EXE) -> CompletedProcess[str]:
        cmd = [self.path, 'eager-focus', EXE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def stack(self, OPERATION_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'stack', OPERATION_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unstack(self) -> CompletedProcess[str]:
        cmd = [self.path, 'unstack']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_stack(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-stack', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_stack_index(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-stack-index', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_stack_window(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-stack-window', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def stack_all(self) -> CompletedProcess[str]:
        cmd = [self.path, 'stack-all']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unstack_all(self) -> CompletedProcess[str]:
        cmd = [self.path, 'unstack-all']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def resize_edge(self, EDGE, SIZING) -> CompletedProcess[str]:
        cmd = [self.path, 'resize-edge', EDGE, SIZING]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def resize_axis(self, AXIS, SIZING) -> CompletedProcess[str]:
        cmd = [self.path, 'resize-axis', AXIS, SIZING]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move_to_monitor(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'move-to-monitor', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_move_to_monitor(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-move-to-monitor', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move_to_workspace(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'move-to-workspace', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move_to_named_workspace(self, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'move-to-named-workspace', WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_move_to_workspace(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-move-to-workspace', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def send_to_monitor(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'send-to-monitor', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_send_to_monitor(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-send-to-monitor', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def send_to_workspace(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'send-to-workspace', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def send_to_named_workspace(self, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'send-to-named-workspace', WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_send_to_workspace(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-send-to-workspace', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def send_to_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'send-to-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move_to_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'move-to-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_monitor(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-monitor', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_last_workspace(self) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-last-workspace']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_workspace(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-workspace', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_workspaces(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-workspaces', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_monitor_workspace(self, TARGET_MONITOR, TARGET_WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-monitor-workspace', TARGET_MONITOR, TARGET_WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focus_named_workspace(self, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'focus-named-workspace', WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def close_workspace(self) -> CompletedProcess[str]:
        cmd = [self.path, 'close-workspace']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_monitor(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-monitor', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_workspace(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-workspace', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def move_workspace_to_monitor(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'move-workspace-to-monitor', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_move_workspace_to_monitor(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-move-workspace-to-monitor', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def swap_workspaces_with_monitor(self, TARGET) -> CompletedProcess[str]:
        cmd = [self.path, 'swap-workspaces-with-monitor', TARGET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def new_workspace(self) -> CompletedProcess[str]:
        cmd = [self.path, 'new-workspace']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def resize_delta(self, PIXELS) -> CompletedProcess[str]:
        cmd = [self.path, 'resize-delta', PIXELS]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def invisible_borders(self, LEFT, TOP, RIGHT, BOTTOM) -> CompletedProcess[str]:
        cmd = [self.path, 'invisible-borders', LEFT, TOP, RIGHT, BOTTOM]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def global_work_area_offset(self, LEFT, TOP, RIGHT, BOTTOM) -> CompletedProcess[str]:
        cmd = [self.path, 'global-work-area-offset', LEFT, TOP, RIGHT, BOTTOM]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def monitor_work_area_offset(self, MONITOR, LEFT, TOP, RIGHT, BOTTOM) -> CompletedProcess[str]:
        cmd = [self.path, 'monitor-work-area-offset', MONITOR, LEFT, TOP, RIGHT, BOTTOM]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focused_workspace_container_padding(self, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'focused-workspace-container-padding', SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def focused_workspace_padding(self, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'focused-workspace-padding', SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def adjust_container_padding(self, SIZING, ADJUSTMENT) -> CompletedProcess[str]:
        cmd = [self.path, 'adjust-container-padding', SIZING, ADJUSTMENT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def adjust_workspace_padding(self, SIZING, ADJUSTMENT) -> CompletedProcess[str]:
        cmd = [self.path, 'adjust-workspace-padding', SIZING, ADJUSTMENT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def change_layout(self, DEFAULT_LAYOUT) -> CompletedProcess[str]:
        cmd = [self.path, 'change-layout', DEFAULT_LAYOUT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cycle_layout(self, CYCLE_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'cycle-layout', CYCLE_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def flip_layout(self, AXIS) -> CompletedProcess[str]:
        cmd = [self.path, 'flip-layout', AXIS]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def promote(self) -> CompletedProcess[str]:
        cmd = [self.path, 'promote']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def promote_focus(self) -> CompletedProcess[str]:
        cmd = [self.path, 'promote-focus']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def promote_window(self, OPERATION_DIRECTION) -> CompletedProcess[str]:
        cmd = [self.path, 'promote-window', OPERATION_DIRECTION]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def retile(self) -> CompletedProcess[str]:
        cmd = [self.path, 'retile']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def monitor_index_preference(self, INDEX_PREFERENCE, LEFT, TOP, RIGHT, BOTTOM) -> CompletedProcess[str]:
        cmd = [self.path, 'monitor-index-preference', INDEX_PREFERENCE, LEFT, TOP, RIGHT, BOTTOM]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def display_index_preference(self, INDEX_PREFERENCE, DISPLAY) -> CompletedProcess[str]:
        cmd = [self.path, 'display-index-preference', INDEX_PREFERENCE, DISPLAY]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def ensure_workspaces(self, MONITOR, WORKSPACE_COUNT) -> CompletedProcess[str]:
        cmd = [self.path, 'ensure-workspaces', MONITOR, WORKSPACE_COUNT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def ensure_named_workspaces(self, MONITOR) -> CompletedProcess[str]:
        cmd = [self.path, 'ensure-named-workspaces', MONITOR]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def container_padding(self, MONITOR, WORKSPACE, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'container-padding', MONITOR, WORKSPACE, SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_container_padding(self, WORKSPACE, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-container-padding', WORKSPACE, SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_padding(self, MONITOR, WORKSPACE, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-padding', MONITOR, WORKSPACE, SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_padding(self, WORKSPACE, SIZE) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-padding', WORKSPACE, SIZE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_layout(self, MONITOR, WORKSPACE, VALUE) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-layout', MONITOR, WORKSPACE, VALUE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_layout(self, WORKSPACE, VALUE) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-layout', WORKSPACE, VALUE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_layout_rule(self, MONITOR, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-layout-rule', MONITOR, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_layout_rule(self, WORKSPACE, AT_CONTAINER_COUNT, LAYOUT) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-layout-rule', WORKSPACE, AT_CONTAINER_COUNT, LAYOUT]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def clear_workspace_layout_rules(self, MONITOR, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'clear-workspace-layout-rules', MONITOR, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def clear_named_workspace_layout_rules(self, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'clear-named-workspace-layout-rules', WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_tiling(self, MONITOR, WORKSPACE, VALUE) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-tiling', MONITOR, WORKSPACE, VALUE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_tiling(self, WORKSPACE, VALUE) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-tiling', WORKSPACE, VALUE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_name(self, MONITOR, WORKSPACE, VALUE) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-name', MONITOR, WORKSPACE, VALUE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_window_container_behaviour(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-window-container-behaviour']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_float_override(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-float-override']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_workspace_window_container_behaviour(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-workspace-window-container-behaviour']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_workspace_float_override(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-workspace-float-override']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_pause(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-pause']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_tiling(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-tiling']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_float(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-float']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_monocle(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-monocle']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_maximize(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-maximize']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def restore_windows(self) -> CompletedProcess[str]:
        cmd = [self.path, 'restore-windows']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def manage(self) -> CompletedProcess[str]:
        cmd = [self.path, 'manage']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unmanage(self) -> CompletedProcess[str]:
        cmd = [self.path, 'unmanage']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def replace_configuration(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'replace-configuration', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def reload_configuration(self) -> CompletedProcess[str]:
        cmd = [self.path, 'reload-configuration']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def watch_configuration(self, BOOLEAN_STATE) -> CompletedProcess[str]:
        cmd = [self.path, 'watch-configuration', BOOLEAN_STATE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def complete_configuration(self) -> CompletedProcess[str]:
        cmd = [self.path, 'complete-configuration']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def window_hiding_behaviour(self, HIDING_BEHAVIOUR) -> CompletedProcess[str]:
        cmd = [self.path, 'window-hiding-behaviour', HIDING_BEHAVIOUR]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def cross_monitor_move_behaviour(self, MOVE_BEHAVIOUR) -> CompletedProcess[str]:
        cmd = [self.path, 'cross-monitor-move-behaviour', MOVE_BEHAVIOUR]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_cross_monitor_move_behaviour(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-cross-monitor-move-behaviour']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def unmanaged_window_operation_behaviour(self, OPERATION_BEHAVIOUR) -> CompletedProcess[str]:
        cmd = [self.path, 'unmanaged-window-operation-behaviour', OPERATION_BEHAVIOUR]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def ignore_rule(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'ignore-rule', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def manage_rule(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'manage-rule', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def initial_workspace_rule(self, IDENTIFIER, ID, MONITOR, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'initial-workspace-rule', IDENTIFIER, ID, MONITOR, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def initial_named_workspace_rule(self, IDENTIFIER, ID, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'initial-named-workspace-rule', IDENTIFIER, ID, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def workspace_rule(self, IDENTIFIER, ID, MONITOR, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'workspace-rule', IDENTIFIER, ID, MONITOR, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def named_workspace_rule(self, IDENTIFIER, ID, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'named-workspace-rule', IDENTIFIER, ID, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def clear_workspace_rules(self, MONITOR, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'clear-workspace-rules', MONITOR, WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def clear_named_workspace_rules(self, WORKSPACE) -> CompletedProcess[str]:
        cmd = [self.path, 'clear-named-workspace-rules', WORKSPACE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def clear_all_workspace_rules(self) -> CompletedProcess[str]:
        cmd = [self.path, 'clear-all-workspace-rules']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def enforce_workspace_rules(self) -> CompletedProcess[str]:
        cmd = [self.path, 'enforce-workspace-rules']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def identify_object_name_change_application(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'identify-object-name-change-application', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def identify_tray_application(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'identify-tray-application', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def identify_layered_application(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'identify-layered-application', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def remove_title_bar(self, IDENTIFIER, ID) -> CompletedProcess[str]:
        cmd = [self.path, 'remove-title-bar', IDENTIFIER, ID]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_title_bars(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-title-bars']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border(self, BOOLEAN_STATE) -> CompletedProcess[str]:
        cmd = [self.path, 'border', BOOLEAN_STATE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border_colour(self, R, G, B, window_kind: Optional[Iterable[Any]] = None) -> CompletedProcess[str]:
        cmd = [self.path, 'border-colour', R, G, B]
        if window_kind:
            cmd.extend(['--window-kind'])
            cmd.extend(window_kind)
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border_width(self, WIDTH) -> CompletedProcess[str]:
        cmd = [self.path, 'border-width', WIDTH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border_offset(self, OFFSET) -> CompletedProcess[str]:
        cmd = [self.path, 'border-offset', OFFSET]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border_style(self, STYLE) -> CompletedProcess[str]:
        cmd = [self.path, 'border-style', STYLE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def border_implementation(self, STYLE) -> CompletedProcess[str]:
        cmd = [self.path, 'border-implementation', STYLE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def stackbar_mode(self, MODE) -> CompletedProcess[str]:
        cmd = [self.path, 'stackbar-mode', MODE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def transparency(self, BOOLEAN_STATE) -> CompletedProcess[str]:
        cmd = [self.path, 'transparency', BOOLEAN_STATE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def transparency_alpha(self, ALPHA) -> CompletedProcess[str]:
        cmd = [self.path, 'transparency-alpha', ALPHA]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_transparency(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-transparency']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def animation(self, BOOLEAN_STATE, animation_type: Optional[Iterable[Any]] = None) -> CompletedProcess[str]:
        cmd = [self.path, 'animation', BOOLEAN_STATE]
        if animation_type:
            cmd.extend(['--animation-type'])
            cmd.extend(animation_type)
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def animation_duration(self, DURATION, animation_type: Optional[Iterable[Any]] = None) -> CompletedProcess[str]:
        cmd = [self.path, 'animation-duration', DURATION]
        if animation_type:
            cmd.extend(['--animation-type'])
            cmd.extend(animation_type)
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def animation_fps(self, FPS) -> CompletedProcess[str]:
        cmd = [self.path, 'animation-fps', FPS]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def animation_style(self, style: Optional[Iterable[Any]] = None, animation_type: Optional[Iterable[Any]] = None) -> CompletedProcess[str]:
        cmd = [self.path, 'animation-style']
        if style:
            cmd.extend(['--style'])
            cmd.extend(style)
        if animation_type:
            cmd.extend(['--animation-type'])
            cmd.extend(animation_type)
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def mouse_follows_focus(self, BOOLEAN_STATE) -> CompletedProcess[str]:
        cmd = [self.path, 'mouse-follows-focus', BOOLEAN_STATE]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def toggle_mouse_follows_focus(self) -> CompletedProcess[str]:
        cmd = [self.path, 'toggle-mouse-follows-focus']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def ahk_app_specific_configuration(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'ahk-app-specific-configuration', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def pwsh_app_specific_configuration(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'pwsh-app-specific-configuration', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def convert_app_specific_configuration(self, PATH) -> CompletedProcess[str]:
        cmd = [self.path, 'convert-app-specific-configuration', PATH]
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def fetch_app_specific_configuration(self) -> CompletedProcess[str]:
        cmd = [self.path, 'fetch-app-specific-configuration']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def application_specific_configuration_schema(self) -> CompletedProcess[str]:
        cmd = [self.path, 'application-specific-configuration-schema']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def notification_schema(self) -> CompletedProcess[str]:
        cmd = [self.path, 'notification-schema']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def socket_schema(self) -> CompletedProcess[str]:
        cmd = [self.path, 'socket-schema']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def static_config_schema(self) -> CompletedProcess[str]:
        cmd = [self.path, 'static-config-schema']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def generate_static_config(self) -> CompletedProcess[str]:
        cmd = [self.path, 'generate-static-config']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def enable_autostart(self, config: Optional[Iterable[Any]] = None, whkd: bool = False, ahk: bool = False, bar: bool = False, masir: bool = False) -> CompletedProcess[str]:
        cmd = [self.path, 'enable-autostart']
        if config:
            cmd.extend(['--config'])
            cmd.extend(config)
        if whkd: 
            cmd.extend(['--whkd'])
        if ahk: 
            cmd.extend(['--ahk'])
        if bar: 
            cmd.extend(['--bar'])
        if masir: 
            cmd.extend(['--masir'])
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

    def disable_autostart(self) -> CompletedProcess[str]:
        cmd = [self.path, 'disable-autostart']
        result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 


if __name__ == "__main__":
    tkomo = WKomorebic()
