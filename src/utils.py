from datetime import datetime
import json
from wrapt_timeout_decorator import *
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox



#----------------------------#
class SharedDataLabel:
    """ Share data labels """
    
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
    """ share data timer """
    
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
class SharedStartAccumulate:
    """ share data accumulate"""

    current_result = None
    @staticmethod
    def setCurrentResult(result):
        SharedStartAccumulate.current_result = result
        print(f"\n>>> [SharedStartAccumulate] setCurrentResult() ==> {result}")
        return result

    @staticmethod
    def getCurrentResult():
        current = SharedStartAccumulate.current_result
        # print(f"\n>>> [SharedDataTimer] getCurrentResult(): {current}")
        return current



#----------------------------#
def export_json(recorded_trials: list, custom_dir:str=None):
    """export json file"""

    # path
    current_datetime = datetime.now()
    dir_to_export = (f'./records') if custom_dir == None else custom_dir

    current_datetime_formatted = current_datetime.strftime("%H.%M.%S_%d-%m-%y")
    json_object = json.dumps(recorded_trials, indent=4)

    path_json_save = f'{dir_to_export}/{current_datetime_formatted}_LOG.json'

    try:
        with open(path_json_save, 'w+') as outfile:
            outfile.write(json_object)
        print("Saved: ", path_json_save)

    except Exception as e:
        raise Exception('Error exporting json file').with_traceback(e.__traceback__)


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
    """show warning popup"""

    msg = QMessageBox()
    msg.setWindowTitle("Warning")
    msg.setText("[Stream Failed]--> Click <start> in LabStreamingLayer")
    button = msg.exec()
    if button == QMessageBox.StandardButton.Ok:
        pass