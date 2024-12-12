import os
from datetime import datetime
import json
from pylsl import resolve_stream
from wrapt_timeout_decorator import *
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox



#----------------------------#
class SharedDataLabel:
    """ share data """
    
    current_result = None
    @staticmethod
    def setCurrentResult(result):
        SharedDataLabel.current_result = result
        print(f"\n>>> [SharedDataLabel] setCurrentResult() ==> {result}")
        return result

    @staticmethod
    def getCurrentResult():
        current = SharedDataLabel.current_result
        print(f"\n>>> [SharedDataLabel] getCurrentResult(): {current}")
        return current
    


#----------------------------#
class SharedDataTimer:
    """ share data """
    
    current_result = None
    @staticmethod
    def setCurrentResult(result):
        SharedDataTimer.current_result = result
        print(f"\n>>> [SharedDataTimer] setCurrentResult() ==> {result}")
        return result

    @staticmethod
    def getCurrentResult():
        current = SharedDataTimer.current_result
        # print(f"\n>>> [SharedDataTimer] getCurrentResult(): {current}")
        return current


#----------------------------#
def export_json(recorded_trials: list, custom_dir:str=None):
    """export json file"""

    # path
    current_datetime = datetime.now()
    home_dir = os.path.expanduser("~").replace('\\', '/')
    
    # check whether the directory exists, if not then create it
    def make_dir():
        if not os.path.exists(f'{home_dir}/bci'):
            os.makedirs(f'{home_dir}/bci')

    def get_dir():
        return home_dir
    
    # run 
    make_dir()

    dir_to_export = (f'{home_dir}/bci') if custom_dir == None else custom_dir

    current_datetime_formatted = current_datetime.strftime("%d_%m_%Y-%H_%M_%S")
    json_object = json.dumps(recorded_trials, indent=4)

    try:
        with open(f'{dir_to_export}/{current_datetime_formatted}.json', 'w+') as outfile:
            outfile.write(json_object)
    except Exception as e:
        raise Exception('Error exporting json file').with_traceback(e.__traceback__)


#----------------------------#
# # Check timeout for streaming status
# @timeout(3, use_signals=False)
# def _resolve_stream():
#     resolve_stream('type', 'EEG')


#----------------------------#
def func_set_geometry(s):
    """set geometry"""

    screen = QtGui.QGuiApplication.primaryScreen()
    s.setGeometry(50, 100, 
        screen.geometry().width()-50,
        screen.geometry().height()-100,
    )


#--------------------------------#
def func_show_popup():
    msg = QMessageBox()
    msg.setWindowTitle("Warning")
    msg.setText("[Stream Failed]--> Need to click <start> in EmotivPro LabStreamingLayer")
    button = msg.exec()
    if button == QMessageBox.StandardButton.Ok:
        pass