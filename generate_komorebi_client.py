import subprocess
import re


def run_help_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def extract_commands(help_output) -> list:
    lines = help_output.splitlines()
    commands = []
    for line in lines:
        if line.startswith('  ') and not line.startswith('   '):  # Check for exactly two spaces
            command = line.strip().split()[0]
            commands.append(command)
        if line.strip() == 'Options:':  # Stop processing after encountering "Options:"
            break
    return commands


def extract_commands_and_arguments(help_output):
    lines = help_output.splitlines()
    commands = []
    current_command = None
    arguments = {}
    options = {}

    for line in lines:
        line = line.strip()

        # Check for command line
        if line.startswith('Usage:'):
            current_command = line.split()[2]
            commands.append(current_command)
            arguments[current_command] = []
            options[current_command] = []

        # Check for arguments
        if '<' in line and line.startswith('Usage:'):
            argument_names = re.findall(r'<(.*?)>', line)
            for argument_name in argument_names:
                arguments[current_command].append(argument_name)

        if '--' in line:
            option_name = re.search(r'--([\w-]+)', line).group(1)
            option_name = option_name.replace("-", "_")
            option_arguments = re.findall(r'<(.*?)>', line)
            options[current_command].append({option_name: option_arguments})

    return commands, arguments, options


def generate_script(commands, arguments, options):
    script_content = '''from subprocess import run, CompletedProcess 
from typing import Iterable, Optional, Any
 

class WKomorebic:
    def __init__(self) -> None:
        self.path = 'komorebic.exe'
        pass
        
'''

    for command in commands:
        if command != 'help':
            method_name = command.replace('-', '_')
            method_arguments = ', ' + ', '.join(arguments[command][command]) if arguments[command][command] else ''
            options_lists = options[command][command]
            option_parameter = []
            option_if = []
            for option_dict in options_lists:
                option_names = list(option_dict.keys())
                option_arguments = option_dict[option_names[0]]
                if option_arguments:
                    for _ in option_arguments:
                        option_parameter.append(f"{option_names[0]}: Optional[Iterable[Any]] = None")
                        option_if.append(f'''if {option_names[0]}:
            cmd.extend(['--{option_names[0].replace("_", "-")}'])
            cmd.extend({option_names[0]})''')
                else:
                    if option_names[0] != 'help':
                        option_parameter.append(f"{option_names[0]}: bool = False")
                        option_if.append(f'''if {option_names[0]}: 
            cmd.extend(['--{option_names[0].replace("_", "-")}'])''')

            rr = ', ' + ', '.join(option_parameter) if option_parameter else ''
            ff = '\n        '.join(option_if) + '\n        ' if option_if else ''
            script_content += f'''    def {method_name}(self{method_arguments}{rr}) -> CompletedProcess[str]:
        cmd = [self.path, '{command}'{method_arguments}]
        {ff}result: CompletedProcess[str] = run(args=cmd, 
                                            shell=True, 
                                            capture_output=True,
                                            text=True) 
        return result 

'''

    script_content += '''
if __name__ == "__main__":
    tkomo = WKomorebic()
'''

    with open('plugin/komorebic_client.py', 'w') as script_file:
        script_file.write(script_content)


def main():
    initial_help_output = run_help_command('komorebic --help')

    command_list = extract_commands(initial_help_output)
    arguments_dict = {}
    options_dict = {}

    for command in command_list:
        command_help_output = run_help_command(f'komorebic {command} --help')
        _, arguments_dict[command], options_dict[command] = extract_commands_and_arguments(command_help_output)

    generate_script(command_list, arguments_dict, options_dict)


if __name__ == "__main__":
    main()
