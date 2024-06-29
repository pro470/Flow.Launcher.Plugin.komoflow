import subprocess
import re

def run_help_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def extract_commands(help_output):
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
        print(f''' '{line}' ''')

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





    return commands, arguments

def generate_script(commands, arguments):
    script_content = '''import subprocess

class WKomorebic:
    def __init__(self) -> None:
        self.path = 'komorebic.exe'
        pass
        
'''

    for command in commands:
        if command != 'help':
            method_name = command.replace('-', '_')
            if len(arguments[command][command]) != 0:       
                method_arguments = ', '.join(arguments[command][command])
                script_content += f'''    def {method_name}(self, {method_arguments}):
        subprocess.run(args=[self.path, '{command}', {method_arguments}], shell=True)

'''
            else:
                script_content += f'''    def {method_name}(self):
        subprocess.run(args=[self.path, '{command}'], shell=True)

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

    for command in command_list:
        command_help_output = run_help_command(f'komorebic {command} --help')
        _, arguments_dict[command] = extract_commands_and_arguments(command_help_output)

    generate_script(command_list, arguments_dict)

if __name__ == "__main__":
    main()
