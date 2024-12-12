import os
import random
import winsound # Windows only
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer, QTime, QDateTime
from PyQt6.QtWidgets import QMainWindow, QLabel
from gui._cursor import Cursor_Window
from config import *
import utils


arrow_random = None


# get x and y center in an area
def center_in_area(start_x, end_x, start_y, end_y, widget):
    x_position = start_x + int((end_x - start_x) / 2) - int(widget.width() / 2)
    y_position = start_y + int((end_y - start_y) / 2) - int(widget.height() / 2)
    return {'x': x_position, 'y': y_position}


######################################
class experiment(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

        utils.func_set_geometry(self)
        self.center()
        self.setProperty("class", "screen-background")
        # self.centralwidget = QtWidgets.QWidget(self) # move here

        ##
        self.protocol = self.kwargs["protocol"]
        self.num_class = PROTOCOL_MAPPING[self.protocol]["num_class"]
        self.num_arrow = PROTOCOL_MAPPING[self.protocol]["num_arrow"]
        self.list_button = PROTOCOL_MAPPING[self.protocol]["list_button"]
        self.dictButton = {}

        ##
        self.init_variables()
        self.create_start_button()
        self.create_corner_buttons()

        #CUONG
        self.show_info_kwarg()
        self.show_deploy_cursor()


    #------------------------------#
    def show_deploy_cursor(self): #CUONG
        self.window = Cursor_Window()
        self.window.show()

    #------------------------------#
    def move_cursor(self): #CUONG
        label = utils.SharedDataLabel.getCurrentResult()
        print(f"MOVE CURSOR (LABEL: {label})")

        # index = self.recent_trial[""]
        x, y = self.window.update_coordinate(label)
        self.window.object.setPos(x, y)
        self.display_cursor_timer.stop()

    #------------------------------#
    def show_info_kwarg(self): #CUONG
        self.label_info = {}
        for i, key in enumerate(self.kwargs.keys()):
            self.label_info[key] = QtWidgets.QLabel(self.centralwidget)
            self.label_info[key].setGeometry(
                QtCore.QRect(
                    0, 25*i, 1000, 50
                    ))
            
            self.label_info[key].setProperty("class", f"info-{key}")
            self.label_info[key].setFont(QtGui.QFont('Arial', 12)) 
            self.label_info[key].setText(
                f"{key} = {self.kwargs[key]}"
            )

    #------------------------------#
    # khoi tao cac bien
    def init_variables(self):

        # count number of trials/skipped trials
        self.count_trials = 0
        self.count_errored_trials = 0

        # define where to resize the number of trials labels
        self.count_labels_resized = False
        self.current_step = STEP_RELAXING

        # array of recorded trials
        self.recorded_trials = []
        self.recent_trial = {
            "index": 1,
            "start_rest": "",
            "end_rest": "",
            "start_cue": "",
            "end_cue": "",
            "start_MI": "",
            "end_MI": "",
            "start_result": "",
            "end_result": "",
            "errored": "No",
            "cue": "",
            "result": ""
        }
        self.relax_time_obj = {
            "from": "00:00",
            "to": ""
        }
        self.instruction_time_obj = {
            "from": "",
            "to": ""
        }
        self.think_time_obj = {
            "from": "",
            "to": ""
        }
        self.result_time_obj = {
            "from": "",
            "to": ""
        }
        self.pause_time_obj = {
            "from": "",
            "to": ""
        }
        self.actual_skip_time = ""

        # variables for pause function
        self.pause_remaining_time = 0
        self.last_active_timer = None
        self.is_paused = False
        self.is_started = False

        self.arrow_label = QtWidgets.QLabel(self)
        self.mouse_label = QtWidgets.QLabel(self)
        # self.break_label = QtWidgets.QLabel(self)

        self.loading_spin_label = QtWidgets.QLabel(self)
        self.loading_spin_label.setGeometry(
            self.horizontal_center_position(197), 
            self.vertical_center_positions(197),
            197, 197)
        self.spinner = QtGui.QMovie('./asset/loading.gif')
        self.spinner.start()

        # show instruction timer
        self.timer_blur_instruction = QtCore.QTimer(self)
        self.timer_blur_instruction.timeout.connect(self.blur_instruction)

        # set timer to^ mau`
        self.button_bg_timer = QtCore.QTimer(self)
        # set mau` cho tat ca cac nut và tăng bộ đếm số lần thử
        self.button_bg_timer.timeout.connect(self.set_all_button_white)
        self.button_bg_timer.timeout.connect(self.increase_count_trials)

        # wait display instruction
        self.wait_display_instruction_timer = QtCore.QTimer(self)
        self.wait_display_instruction_timer.timeout.connect(
            self.display_instruction)

        # instruction
        self.arrow_img = QtGui.QPixmap(NUMBER_ARROW_MAPPING[1] + '.png')
        self.mouse_img = QtGui.QPixmap('./asset/mouse.png')
        # self.break_img = QtGui.QPixmap('./asset/rest.png')

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # self.break_label.setPixmap(self.break_img)
        # self.break_label.resize(self.break_img.width(), 
        #                         self.break_img.height())
        # self.break_label.hide()

        # corner buttons
        for i in self.list_button:
            self.dictButton[i] = QtWidgets.QPushButton(self.centralwidget)

        # state button
        self.btn_ex = QtWidgets.QPushButton(self.centralwidget)
        self.btn_menu = QtWidgets.QPushButton(self.centralwidget)
        self.btn_report = QtWidgets.QPushButton(self.centralwidget)

        self.trial_num_label = QtWidgets.QLabel(self.centralwidget)
        self.trial_num_label.setProperty(
            "class", "trial-number-display")
        self.trial_num_label.setText(
            'DONE: ' + str(self.count_trials))
        self.trial_num_label.hide()

        self.skipped_trial_num_label = QtWidgets.QLabel(self.centralwidget)
        self.skipped_trial_num_label.setProperty(
            "class", "skipped-trial-number-display")
        self.skipped_trial_num_label.setText(
            'REPORTED: ' + str(self.count_errored_trials))
        self.skipped_trial_num_label.hide()

        # timer label
        self.experiment_timer_label = QLabel(self.centralwidget)
        self.experiment_timer_label.setGeometry(
            QtCore.QRect(
                self.horizontal_center_position(100), 
                0, 
                100, 
                100
            )
        )
        self.experiment_timer_label.setText("00:00")
        self.experiment_timer_label.setProperty("class", "experiment-timer")
        self.experiment_timer_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.experiment_timer_label.hide()

        # forecasting time
        self.loading_spin_label_timer = QtCore.QTimer(self)
        self.loading_spin_label_timer.timeout.connect(self.show_forecast)

        # display forecast time ??
        # self.display_forecast_time = QtCore.QTimer(self)

        #CUONG
        self.display_cursor_timer = QtCore.QTimer(self)
        self.display_cursor_timer.timeout.connect(self.move_cursor)
        # create a mapping dict {0: self.btn_right, 1: ...}
        self.number_to_button_mapping = {
            i: self.dictButton[v] for i,v in \
                enumerate(self.list_button)
        } 



    #------------------------------#
    # khoi tao va hien thi nut start
    def create_start_button(self):

        self.btn_report.setGeometry(
            QtCore.QRect(
                self.width() - 125 - MARGIN - self.btn_report.width(), 
                25, 
                125, 
                50
                ))
        self.btn_report.setProperty("class", "start-ex-button")
        self.btn_report.setIcon(QtGui.QIcon('./asset/report.png'))
        self.btn_report.setIconSize(QtCore.QSize(32, 32))
        self.btn_report.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_report.setText("REPORT")
        self.btn_report.hide()
        self.btn_report.clicked.connect(self.report_trial)

        self.btn_menu.setGeometry(
            QtCore.QRect(
                MARGIN, 
                25, 
                125, 
                50
                ))
        self.btn_menu.setProperty("class", "start-ex-button")
        self.btn_menu.setIcon(QtGui.QIcon('./asset/home.png'))
        self.btn_menu.setIconSize(QtCore.QSize(32, 32))
        self.btn_menu.setText("HOME")
        self.btn_menu.clicked.connect(self.back_to_home)
        self.btn_menu.hide()

        self.btn_ex.setGeometry(
            QtCore.QRect(
                int((self.width() - 100) / 2), 
                int((self.height() - 100) / 2), 
                100, 
                100
                ))
        self.btn_ex.setProperty("class", "start-ex-button")
        self.btn_ex.setIcon(QtGui.QIcon('./asset/play.png'))
        self.btn_ex.setIconSize(QtCore.QSize(64, 64))
        self.btn_ex.clicked.connect(self.start_experiment)
        self.btn_ex.show()

        self.is_started = True
    
    
    #------------------------------#
    # hien thi 8 nut 8 goc
    def create_corner_buttons(self):
        responsive_width = int(self.width() * 1 / 4)
        responsive_height = int(self.height() * 1 / 4)
        corner_width = int(self.width() * 1 / 8)
        corner_height = int(self.height() * 1 / 8)

        #----- 2-class -------#
        # left
        self.dictButton["btn_left"].setGeometry(
            QtCore.QRect(
                MARGIN, 
                self.vertical_center_positions(responsive_height), 
                THICKNESS, 
                responsive_height
                )
        )
        self.dictButton["btn_left"].setProperty(
            "class", "left-button"
        )

        # right
        self.dictButton["btn_right"].setGeometry(
            QtCore.QRect(
                self.width() - THICKNESS - MARGIN, 
                self.vertical_center_positions(responsive_height),
                THICKNESS, 
                responsive_height,
            )
        )
        self.dictButton["btn_right"].setProperty(
            "class", "right-button"
        )


        #----- 4-class -------#
        if self.num_class > 2:
            # top
            self.dictButton["btn_up"].setGeometry(
                QtCore.QRect(
                    self.horizontal_center_position(responsive_width), 
                    MARGIN, 
                    responsive_width, 
                    THICKNESS,
                )
            )
            self.dictButton["btn_up"].setProperty(
                "class", "top-button"
            )

            # bottom
            self.dictButton["btn_down"].setGeometry(
                QtCore.QRect(
                    self.horizontal_center_position(responsive_width), 
                    self.height() - THICKNESS - MARGIN,
                    responsive_width, 
                    THICKNESS
                )
            )
            self.dictButton["btn_down"].setProperty(
                "class", "top-button"
            )


            #----- 8-class -------#
            if self.num_class == 8:
                # top-right
                self.dictButton["btn_top_right"].setGeometry(
                    QtCore.QRect(
                        self.width() - MARGIN - corner_width, 
                        MARGIN, 
                        corner_width, 
                        corner_height
                    )
                )
                self.dictButton["btn_top_right"].setProperty(
                    "class", "top-button"
                )

                # bottom-right
                self.dictButton["btn_bot_right"].setGeometry(
                    QtCore.QRect(
                        self.width() - MARGIN - corner_width, 
                        self.height() - MARGIN - corner_height, 
                        corner_width,
                        corner_height
                    )
                )
                self.dictButton["btn_bot_right"].setProperty(
                    "class", "top-button"
                )

                # top-left
                self.dictButton["btn_top_left"].setGeometry(
                    QtCore.QRect(
                        MARGIN, 
                        MARGIN, 
                        corner_width, 
                        corner_height
                    )
                )
                self.dictButton["btn_top_left"].setProperty(
                    "class", "top-button"
                )

                # bottom-left
                self.dictButton["btn_bot_left"].setGeometry(
                    QtCore.QRect(
                        MARGIN, 
                        self.height() - MARGIN - corner_height, 
                        corner_width, 
                        corner_height
                    )
                )
                self.dictButton["btn_bot_left"].setProperty(
                    "class", "top-button"
                )


    #------------------------------#
    # hien thi bien con chuot giua man hinh
    def create_mouse_img(self):
        self.mouse_label.setPixmap(self.mouse_img)
        self.mouse_label.resize(
            self.mouse_img.width(), 
            self.mouse_img.height()
            )
        x_position = int((self.width() - self.mouse_img.width()) / 2)
        y_position = int((self.height() - self.mouse_img.height()) / 2)
        self.mouse_label.move(x_position, y_position)
        self.mouse_label.show()


    #------------------------------#
    # bat event thay doi size cua screen
    def resizeEvent(self, event):
        
        self.create_corner_buttons()

        self.btn_ex.move(
            int((self.width() - 100) / 2), 
            int((self.height() - 100) / 2)
            )
        self.btn_report.move(
            self.width() - 125 - MARGIN, 
            25
            )
        self.loading_spin_label.move(
            self.horizontal_center_position(197), 
            self.vertical_center_positions(197)
            )
        self.experiment_timer_label.setGeometry(
            QtCore.QRect(
                self.horizontal_center_position(100), 
                0, 
                100, 
                100
                ))
        self.trial_num_label.move(
            MARGIN, 
            self.height() - int(MARGIN * 0.75) + int(self.trial_num_label.height() / 2)
            )
        self.skipped_trial_num_label.move(
            int(MARGIN * 1.75) + self.skipped_trial_num_label.width(),
            self.height() - int(MARGIN * 0.75) + int(self.skipped_trial_num_label.height() / 2))

        if self.is_started == True:
            x_position = int((self.width() - self.mouse_label.width()) / 2)
            y_position = int((self.height() - self.mouse_label.height()) / 2)
            self.mouse_label.move(x_position, y_position)
            self.set_position_arrow()

        QtWidgets.QMainWindow.resizeEvent(self, event)


    #------------------------------#
    def center(self):
        # Get the geometry of the current window
        frameGm = self.frameGeometry()
        # Get the screen that the cursor is currently on
        screen = QtWidgets.QApplication.primaryScreen()
        # Get the center point of the screen
        centerPoint = screen.availableGeometry().center()
        # Move the window's geometry to center it
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())



    #------------------------------#
    # hien thi cac mui ten
    def display_instruction(self):

        # print(f"\n===trial: {self.count_trials}=\n")

        self.relax_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        self.set_relax_time_recent_trial()

        self.wait_display_instruction_timer.stop()
        self.instruction_time_obj["from"] = QDateTime.currentDateTime().toSecsSinceEpoch()

        # self.relax_label.hide()

        ## SHOW CUE
        self.create_mouse_img()
        global arrow_random
        arrow_random = random.randint(1, self.num_arrow)
        self.recent_trial["cue"] = arrow_random
        self.generate_arrow(arrow_random)

        ## cue waiting
        self.timer_blur_instruction.start(SHOW_INSTRUCTION_TIME)


    #------------------------------#
    def generate_arrow(self, rand:int, blur=False):
        """ khoi tao mui ten """
        if blur:
            self.arrow_img = QtGui.QPixmap(NUMBER_ARROW_MAPPING[rand] + '_.png')
        else:
            self.arrow_img = QtGui.QPixmap(NUMBER_ARROW_MAPPING[rand] + '.png')

        self.arrow_label.setPixmap(self.arrow_img)
        self.arrow_label.resize(self.arrow_img.width(), 
                                self.arrow_img.height())

        self.set_position_arrow()
        self.arrow_label.show()
        self.current_step = STEP_INSTRUCTION
    

    #------------------------------#
    def blur_instruction(self):
        """ blur """

        self.instruction_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        self.set_instruction_time_recent_trial()
        self.think_time_obj["from"] = QDateTime.currentDateTime().toSecsSinceEpoch()

        # beep
        self.mouse_label.clear()
        winsound.Beep(frequency=2000, duration=100)
        print("BEEP")

        # CUONG - ADD BLUR
        self.generate_arrow(arrow_random, blur=True)


        self.loading_spin_label.show()
        self.loading_spin_label.setMovie(self.spinner)

        # START TIME TO IMAGERY
        self.loading_spin_label_timer.start(FORECAST_TIME)
            
        self.current_step = STEP_THINKING
        self.timer_blur_instruction.stop()


    #------------------------------#
    # hien thi du doan (TODO: import du lieu tu model)
    def show_forecast(self):
        self.think_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        self.set_think_time_recent_trial()

        self.result_time_obj["from"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        
        # Erase mouse and arrow
        # self.mouse_label.clear()
        self.arrow_label.clear()
        
        self.loading_spin_label.clear()
        self.loading_spin_label.hide()
        self.loading_spin_label_timer.stop()

        self.current_step = STEP_RESULT
        self.get_predict_result()
        self.button_bg_timer.start(DISPLAY_FORECAST_TIME)

        #CUONG
        self.display_cursor_timer.start(100)
        # self.break_label.show()


    #------------------------------#
    # du doan ket qua
    def get_predict_result(self):

        # get current result
        label = utils.SharedDataLabel.getCurrentResult()
        print(f"COLOR THE PREDICTED BUTTON (LABEL: {label})")

        # hien thi ket qua du doan
        predicted_btn = self.number_to_button_mapping.get(label)

        # luu vao recent trial
        self.recent_trial["result"] = label

        # dat lai mau cho tat ca cac nut
        for button in self.number_to_button_mapping.values():
            button.setStyleSheet("background-color: white;")

        # doi mau nut duoc chon
        predicted_btn.setStyleSheet("background-color: #2acc97;")



    # # CUONG add break between trials
    # def show_break(self):
    #     self.result_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
    #     self.set_result_time_recent_trial()
    #     self.break_time_obj["from"] = QDateTime.currentDateTime().toSecsSinceEpoch()

    #     self.button_bg_timer.stop()
    #     self.current_step = STEP_BREAK

    #     x_position = int((self.width() - self.break_img.width()) / 2)
    #     y_position = int((self.height() - self.break_img.height()) / 2)
    #     self.break_label.move(x_position, y_position)
    #     self.break_label.show()
    #     self.break_label_timer.start(BREAK_TIME)


    #------------------------------#
    # set x-axis va y-axis cho arrow
    def set_position_arrow(self):

        global arrow_random
        x_position = 0
        y_position = 0

        if arrow_random == ARROW_RIGHT_INT:
            pos = center_in_area(
                int(self.width() / 2), 
                self.width() - MARGIN, 
                MARGIN, 
                self.height() - MARGIN,
                self.arrow_label)
        
        elif arrow_random == ARROW_LEFT_INT:
            pos = center_in_area(
                MARGIN, 
                int(self.width() / 2), 
                MARGIN, 
                self.height() - MARGIN, 
                self.arrow_label)

        elif arrow_random == ARROW_UP_INT:
            pos = center_in_area(
                MARGIN, 
                self.width() - MARGIN, 
                MARGIN, 
                int(self.height() / 2), 
                self.arrow_label)

        elif arrow_random == ARROW_DOWN_INT:
            pos = center_in_area(
                MARGIN, self.width() - MARGIN, 
                int(self.height() / 2), self.height() - MARGIN,
                self.arrow_label)

        elif arrow_random == ARROW_TOP_RIGHT_INT:
            pos = center_in_area(
                int(self.width() / 2), 
                self.width() - MARGIN, 
                MARGIN, 
                int(self.height() / 2),
                self.arrow_label)
            
        elif arrow_random == ARROW_TOP_LEFT_INT:
            pos = center_in_area(
                MARGIN, 
                int(self.width() / 2), 
                MARGIN, 
                int(self.height() / 2), 
                self.arrow_label)

        elif arrow_random == ARROW_BOT_RIGHT_INT:
            pos = center_in_area(
                int(self.width() / 2), 
                self.width() - MARGIN, 
                int(self.height() / 2),
                self.height() - MARGIN, 
                self.arrow_label)
            
        else:  # bottom left
            pos = center_in_area(
                MARGIN, 
                int(self.width() / 2), 
                int(self.height() / 2), 
                self.height() - MARGIN,
                self.arrow_label)
            
            
        x_position = pos['x']
        y_position = pos['y']
        self.arrow_label.move(x_position, y_position)


    #------------------------------#
    # set white background cho tat ca cac nut
    def set_all_button_white(self):

        for i,v in enumerate(self.list_button):
            self.dictButton[v].setStyleSheet("background-color: white;")


        self.button_bg_timer.stop()
        # self.break_label_timer.stop()

        self.result_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        # self.break_time_obj["to"] = QDateTime.currentDateTime().toSecsSinceEpoch()
        self.relax_time_obj["from"] = QDateTime.currentDateTime().toSecsSinceEpoch()

        if self.result_time_obj["from"] != "":
            self.set_result_time_recent_trial()
            self.append_recent_trial()
        # if self.break_time_obj["from"] != "":
        #     self.set_break_time_recent_trial()
        #     self.append_recent_trial()

        self.wait_display_instruction_timer.start(WAIT_SHOW_INSTRUCTION_TIME)
        self.current_step = STEP_RELAXING

        # x_position = int((self.width() - self.relax_img.width()) / 2)
        # y_position = int((self.height() - self.relax_img.height()) / 2)
        # self.break_label.move(x_position, y_position)
        # self.break_label.show()
        self.btn_report.setEnabled(True)
        self.btn_report.setStyleSheet("background-color: #2acc97")

    # lay y-axis chinh giua theo chieu doc
    def vertical_center_positions(self, height):
        return int((self.height() - height) / 2)

    # lay x-axis chinh giua theo chieu ngang
    def horizontal_center_position(self, width):
        return int((self.width() - width) / 2)

    def set_conditions_back_to_first_step_after_pause(self):
        self.pause_remaining_time = 0
        self.last_active_timer = None
        self.spinner.setPaused(False)
        self.is_paused = False

    # def back_to_home(self):
    #     menu = Menu()
    #     widget.addWidget(menu)
    #     widget.setCurrentWidget(menu)


    def reset_recent_trial(self):
        self.recent_trial = {
            "index": ((self.recorded_trials[len(self.recorded_trials) - 1])["index"] + 1),
            "start_rest": "",
            "end_rest": "",
            "start_cue": "",
            "end_cue": "",
            "start_MI": "",
            "end_MI": "",
            "start_result": "",
            "end_result": "",

            "start_break": "",
            "end_break": "",
            
            "errored": "No",
            "cue": "",
            "result": ""
        }

        self.relax_time_obj = {
            "from": QDateTime.currentDateTime().toSecsSinceEpoch(),
            "to": ""
        }
        self.instruction_time_obj = {
            "from": "",
            "to": ""
        }
        self.think_time_obj = {
            "from": "",
            "to": ""
        }
        self.result_time_obj = {
            "from": "",
            "to": ""
        }

        self.break_time_obj = {
            "from": "",
            "to": ""
        }

        self.pause_time_obj = {
            "from": "",
            "to": ""
        }
        self.actual_skip_time = ""


    def report_trial(self):
        self.count_errored_trials += 1
        self.btn_report.setEnabled(False)
        self.btn_report.setStyleSheet("background-color: #c7c7c7")
        self.set_trial_error()
        self.set_instruction_time_recent_trial()
        self.set_relax_time_recent_trial()
        self.set_think_time_recent_trial()
        self.set_result_time_recent_trial()

        # self.set_break_time_recent_trial() # CUONG

        if self.count_labels_resized == False and self.count_errored_trials >= 10:
            self.skipped_trial_num_label.resize(
                self.skipped_trial_num_label.width() + 50,
                self.skipped_trial_num_label.height()
                )
            self.trial_num_label.resize(
                self.trial_num_label.width() + 20, 
                self.trial_num_label.height()
                )
            self.count_labels_resized == True

        self.skipped_trial_num_label.setText(
            'REPORTED: ' + str(self.count_errored_trials))

    def set_relax_time_recent_trial(self):
        self.recent_trial["start_rest"] = self.relax_time_obj["from"]
        self.recent_trial["end_rest"] = self.relax_time_obj["to"]

    def set_instruction_time_recent_trial(self):
        self.recent_trial["start_cue"] = self.instruction_time_obj["from"]
        self.recent_trial["end_cue"] = self.instruction_time_obj["to"]

    def set_think_time_recent_trial(self):
        self.recent_trial["start_MI"] = self.think_time_obj["from"]
        self.recent_trial["end_MI"] = self.think_time_obj["to"]

    def set_result_time_recent_trial(self):
        self.recent_trial["start_result"] = self.result_time_obj["from"]
        self.recent_trial["end_result"] = self.result_time_obj["to"]

    def set_break_time_recent_trial(self):
        self.recent_trial["start_break"] = self.break_time_obj["from"]
        self.recent_trial["end_break"] = self.break_time_obj["to"]

    def set_trial_error(self):
        self.recent_trial["errored"] = "Yes"

    def append_recent_trial(self):
        self.recorded_trials.append(self.recent_trial)
        self.reset_recent_trial()

    def increase_count_trials(self):
        self.count_trials += 1

        if self.count_labels_resized == False and self.count_trials >= 10:
            self.skipped_trial_num_label.resize(
                self.skipped_trial_num_label.width() + 50,
                self.skipped_trial_num_label.height()
                )
            self.trial_num_label.resize(
                self.trial_num_label.width() + 20, 
                self.trial_num_label.height()
                )
            self.count_labels_resized == True

        self.trial_num_label.setText('DONE: ' + str(self.count_trials))
        self.trial_num_label.show()
        if self.count_trials == self.kwargs["n_trials"]:
            self.end_experiment()

    def render_timer(self):

        self.experiment_timer_label.show()
        
        self.current_experiment_time = QTime(0, 0)  # init time
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every second

        self.update_time()  # initial time display


    def update_time(self):
        self.current_experiment_time = self.current_experiment_time.addSecs(1)
        utils.SharedDataTimer.setCurrentResult(self.current_experiment_time)
        self.experiment_timer_label.setText(self.current_experiment_time.toString('mm:ss'))






##############################33
# SECTION end of experiment screen
class end_of_experiment(QMainWindow):
    def __init__(self):
        super().__init__()
        
        utils.func_set_geometry(self)        
        self.setProperty("class", "screen-background")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.create_labels()
        self.create_buttons()


    def create_labels(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText("FINISHED!")
        self.title.setProperty("class", "end-of-experiment-title")
        self.title.show()

        self.footer = QtWidgets.QLabel(self.centralwidget)
        self.footer.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit")
        self.footer.setProperty("class", "menu-footer")
        self.footer.show()

    def create_buttons(self):
        button_x = int((self.width() - BUTTON_WIDTH) / 2)
        button_y = int((self.height() - BUTTON_HEIGHT) / 2) - GAP

        self.btn_restart = QtWidgets.QPushButton(self.centralwidget)
        self.btn_restart.setGeometry(QtCore.QRect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        self.btn_restart.setProperty("class", "menu-button")
        self.btn_restart.setText('RESTART')
        self.btn_restart.setIcon(QtGui.QIcon('./asset/microscope_white.png'))
        self.btn_restart.setIconSize(QtCore.QSize(32, 32))
        self.btn_restart.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_restart.clicked.connect(self.navigate_to_config_trial)

        self.btn_home = QtWidgets.QPushButton(self.centralwidget)
        self.btn_home.setGeometry(QtCore.QRect(button_x, button_y + GAP, BUTTON_WIDTH, BUTTON_HEIGHT))
        self.btn_home.setProperty("class", "menu-button")
        self.btn_home.setText('HOME')
        self.btn_home.setIcon(QtGui.QIcon('./asset/home.png'))
        self.btn_home.setIconSize(QtCore.QSize(32, 32))
        self.btn_home.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_home.clicked.connect(self.back_to_home)

        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(
            QtCore.QRect(
                button_x, 
                button_y + BUTTON_HEIGHT + 2 * GAP, 
                BUTTON_WIDTH, 
                BUTTON_HEIGHT
            )
        )
        self.btn_quit.setProperty("class", "menu-button-quit")
        self.btn_quit.setText('EXIT')
        self.btn_quit.setIcon(QtGui.QIcon('./asset/door-exit-white.png'))
        self.btn_quit.setIconSize(QtCore.QSize(32, 32))
        self.btn_quit.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_quit.clicked.connect(QtCore.QCoreApplication.quit)


    def resizeEvent(self, event):
        self.title.move(
            int((self.width() - self.title.width()) / 2), 
            MARGIN
            )
        self.footer.move(
            int((self.width() - self.footer.width()) / 2), 
            self.height() - MARGIN - self.footer.height()
            )
        self.btn_restart.move(
            int((self.width() - BUTTON_WIDTH) / 2), 
            int((self.height() - BUTTON_HEIGHT) / 2) - 15
            )
        self.btn_home.move(
            int((self.width() - BUTTON_WIDTH) / 2), 
            int((self.height() - BUTTON_HEIGHT) / 2) + GAP
            )
        self.btn_quit.move(
            int((self.width() - BUTTON_WIDTH) / 2),
            int((self.height() - BUTTON_HEIGHT) / 2) + BUTTON_HEIGHT + GAP + 15
            )


    def back_to_home(self):
        pass

    def navigate_to_config_trial(self):
        pass

