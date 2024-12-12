"""
Pilot work by Cuong Pham
cuongquocpham151@gmail.com
"""

import sys
import numpy as np
import time
import threading
from queue import Queue

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication


from gui._menu import menu
from gui._select import config_trial, config_class, config_model
from gui._experiment import experiment, end_of_experiment
from config import *
from cortex.export import start_recording_experiment
from classifier.lsl_stream import start_predicted_result, LSL_STREAM, OFFLINE_STREAM
from classifier.infer import Module_Prediction
import utils


#--------------------------------#
## CHECK STREAMING STATUS
global lsl
if STREAM_ONLINE:
    lsl = LSL_STREAM()
    lsl.initialize_inlet()

else:
    lsl = OFFLINE_STREAM()


#--------------------------------#
# MENU -> SELECT TRIAL -> SELECT MODE -> IMPORT MODEL -> EXPERIMENT
class MENU(menu):
    def show_popup(self):             
        return utils.func_show_popup()
    
    def navigate_to_config_trial(self, **kwargs):
        s = CONFIG_TRIAL(**kwargs)
        widget.addWidget(s)
        widget.setCurrentWidget(s)


#--------------------------------#
class CONFIG_TRIAL(config_trial):
    def navigate_to_config_class(self, **kwargs):
        s = CONFIG_CLASS(**kwargs)
        widget.addWidget(s)
        widget.setCurrentWidget(s)

#--------------------------------#
class CONFIG_CLASS(config_class):
    def navigate_to_config_model(self, **kwargs):
        s = CONFIG_MODEL(**kwargs)
        widget.addWidget(s)
        widget.setCurrentWidget(s)



#--------------------------------#
class CONFIG_MODEL(config_model):
    def navigate_to_experiment(self, **kwargs):
        global record_eeg_thread, predict_thread

        if STREAM_ONLINE:

            # Init Thread
            record_eeg_thread = threading.Thread(
                target=start_recording_experiment, 
                kwargs=kwargs
            )
            # # Exit thread when the main program exits
            # record_eeg_thread.daemon = True  
            # # Start Thread
            # record_eeg_thread.start()


        ## MODEL PREDICTION
        mp = Module_Prediction(
            path_onnx=kwargs["file_model"], # onnx file
            fs=128,
            window=2.0,
            overlap=0.5,
        )

        # Init Thread Prediction
        predict_thread = threading.Thread(
            target=start_predicted_result,
            kwargs={
                "lsl": lsl,
                "ml_module": mp,
            }
        )
        # # Allow thread to exit when the main program exits
        # predict_thread.daemon = True  
        # # Start Thread Prediction
        # predict_thread.start()


        ##---- RUN EXPERIMENT ----##
        e = EXPERIMENT(**kwargs)
        widget.addWidget(e)
        widget.setCurrentWidget(e)



#--------------------------------#
class EXPERIMENT(experiment):

    # bat dau su dung
    def start_experiment(self):

        if STREAM_ONLINE:

            # Exit thread when the main program exits
            record_eeg_thread.daemon = True  
            # Start Thread
            record_eeg_thread.start()

            time.sleep(2)

            # Allow thread to exit when the main program exits
            predict_thread.daemon = True  
            # Start Thread Prediction
            predict_thread.start()

            while True:
                with open('./file.tmp', 'r') as f:
                    contents = f.read()
                if contents == '1':
                    break
    
        
        # CUONG
        for key in self.kwargs.keys(): 
            self.label_info[key].hide()

        self.btn_ex.hide()
        self.btn_report.show()
        self.btn_menu.show()
        self.trial_num_label.show()
        self.skipped_trial_num_label.show()
        self.render_timer()
        self.set_all_button_white()

    def back_to_home(self):
        s = MENU()
        widget.addWidget(s)
        widget.setCurrentWidget(s)

    def end_experiment(self):
        # stop all timer at the end
        self.timer.stop()
        self.timer_blur_instruction.stop()
        self.wait_display_instruction_timer.stop()
        self.button_bg_timer.stop()
        self.loading_spin_label_timer.stop()

        # export json file
        utils.export_json(self.recorded_trials)

        # redirect to EndOfExperiment
        end_of_experiment = END_OF_EXPERIMENT()
        widget.addWidget(end_of_experiment)
        widget.setCurrentWidget(end_of_experiment)



#--------------------------------#
class END_OF_EXPERIMENT(end_of_experiment):
    
    def back_to_home(self):
        s = MENU()
        widget.addWidget(s)
        widget.setCurrentWidget(s)

    def navigate_to_config_trial(self):
        s = CONFIG_TRIAL()
        widget.addWidget(s)
        widget.setCurrentWidget(s)
    
    def navigate_to_config_class(self, **kwargs):
        s = CONFIG_CLASS(**kwargs)
        widget.addWidget(s)
        widget.setCurrentWidget(s)
    
    def navigate_to_config_model(self, **kwargs):
        s = CONFIG_MODEL(**kwargs)
        widget.addWidget(s)
        widget.setCurrentWidget(s)

    def navigate_to_experiment(self, **kwargs):
        e = EXPERIMENT(**kwargs)
        widget.addWidget(e)
        widget.setCurrentWidget(e)



###########################
if __name__ == "__main__":

    ## Start APP
    app = QApplication(sys.argv)
    with open('src/style.qss', 'r') as fh:
        app.setStyleSheet(fh.read())

    s = MENU()
    
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(s)
    widget.setCurrentWidget(s)
    utils.func_set_geometry(widget)
    widget.setWindowTitle("BCI")
    widget.show()
    
    sys.exit(app.exec())
