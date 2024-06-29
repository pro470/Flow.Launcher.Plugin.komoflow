import os
import sys

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from plugin import komoflow, utils

if __name__ == "__main__":
    utils.connect_komorebi(komoflow.plugin.komorebic, komoflow.plugin.pipename)
    komoflow.plugin.run()
