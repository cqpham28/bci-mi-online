from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from config import *
from utils import func_set_geometry
    


##################################
class config_trial(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        
        func_set_geometry(self)
        self.setProperty("class", "screen-background")
        self.centralwidget = QtWidgets.QWidget(self)
        
        ##
        self.create_label()
        self.create_option()
        self.setCentralWidget(self.centralwidget)

    #------------------------------#
    def create_label(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText("Input the numbers of trials")
        self.title.setProperty("class", "menu-title")
        self.title.show()

    #------------------------------#
    def create_option(self):
        box_x = int((self.width() - SELECT_BOX_WIDTH) / 2)
        box_y = int((self.height() - SELECT_BOX_HEIGHT) / 2)

        # line-edit
        self.le = QtWidgets.QLineEdit(self.centralwidget)
        self.le.setGeometry(
            QtCore.QRect(
                box_x,
                box_y,
                SELECT_BOX_WIDTH, 
                SELECT_BOX_HEIGHT
                ))
        self.le.setValidator(QtGui.QIntValidator())
        self.le.setMaxLength(2)
        self.le.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.le.setFont(QtGui.QFont("Arial",40))
        self.le.setStyleSheet("QLineEdit"
                                "{"
                                "background : green;"
                                "}") 
        self.le.setText(str(DEFAULT_TRIAL))

        self.option_x = QtWidgets.QPushButton(self.centralwidget)
        self.option_x.setGeometry(
            QtCore.QRect(
                int((self.width() - BUTTON_WIDTH) / 2), 
                box_y + SELECT_BOX_HEIGHT + GAP, 
                BUTTON_WIDTH, 
                BUTTON_HEIGHT,
                ))
        self.option_x.setProperty("class", "trial-option")
        self.option_x.setText('Confirm')
        self.option_x.clicked.connect(
            lambda: self.navigate_to_config_class(
                **self.kwargs,
                n_trials=int(self.le.text()),
                )
        )

    #------------------------------#
    def resizeEvent(self, event):
        self.title.move(
            int((self.width() - self.title.width()) / 2), 
            MARGIN
            )
        # self.le.move(
        #     int((self.width() - SELECT_BOX_WIDTH) / 2) - BOX_GAP,
        #     int((self.height() - SELECT_BOX_HEIGHT) / 2)
        #     )
        QtWidgets.QMainWindow.resizeEvent(self, event)


    #------------------------------#
    def navigate_to_config_class(self, **kwargs):
        pass



##########################
class config_class(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

        func_set_geometry(self)
        self.setProperty("class", "screen-background")
        self.centralwidget = QtWidgets.QWidget(self)

        ## label
        self.create_label()

        ## option
        button_x = int((self.width() - SELECT_BOX_WIDTH) / 2)
        button_y = int((self.height() - SELECT_BOX_HEIGHT) / 2)
        self.create_option("2-class", button_x-2*BOX_GAP, button_y)
        self.create_option("4-class", button_x, button_y)
        self.create_option("8-class*", button_x+2*BOX_GAP, button_y)

        self.setCentralWidget(self.centralwidget)


    #------------------------------#
    def create_label(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText("Select Class-Mode")
        self.title.setProperty("class", "menu-title")
        self.title.show()


    #------------------------------#
    def create_option(self, qrect_text:str, qrect_x:int, qrect_y:int):
        self.option = QtWidgets.QPushButton(self.centralwidget)
        self.option.setGeometry(
            QtCore.QRect(
                qrect_x, 
                qrect_y, 
                SELECT_BOX_WIDTH, 
                SELECT_BOX_HEIGHT,
                ))
        self.option.setProperty("class", "trial-option")
        self.option.setText(qrect_text)
        self.option.clicked.connect(
            lambda: self.navigate_to_config_model(
                **self.kwargs,
                protocol = qrect_text
                )
        )

    #------------------------------#
    def resizeEvent(self, event):
        self.title.move(
            int((self.width() - self.title.width()) / 2), 
            MARGIN
            )
        QtWidgets.QMainWindow.resizeEvent(self, event)


    #------------------------------#
    def navigate_to_config_model(self, **kwargs):
        pass




##########################
class config_model(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

        func_set_geometry(self)
        self.setProperty("class", "screen-background")
        self.centralwidget = QtWidgets.QWidget(self)

        ## 
        self.create_label()
        self.create_button()
        self.setCentralWidget(self.centralwidget)
    
    #------------------------------#
    def create_label(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText("Import Model")
        self.title.setProperty("class", "menu-title")
        self.title.show()


    #------------------------------#
    def create_button(self):
  
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(
            QtCore.QRect(
                int((self.width() - BUTTON_WIDTH) / 2),
                int((self.height() - BUTTON_HEIGHT) / 2) - GAP,
                BUTTON_WIDTH, 
                BUTTON_HEIGHT
                ))
        self.btn.setProperty("class", "menu-button")
        self.btn.setText("Open File")
        self.btn.clicked.connect(self.openFileNameDialog)


    #------------------------------#
    def openFileNameDialog(self):

        options = QFileDialog.Option.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "",\
                "All Files (*);;ONNX Files (*.onnx)", 
            options=options
        )
        if fileName:
            self.navigate_to_experiment(
                **self.kwargs,
                file_model = fileName,
            )


    #------------------------------#
    def resizeEvent(self, event):
        self.title.move(
            int((self.width() - self.title.width()) / 2), 
            MARGIN
            )
        self.btn.move(
            int((self.width() - BUTTON_WIDTH) / 2),
            int((self.height() - BUTTON_HEIGHT) / 2) - GAP,
            )
        QtWidgets.QMainWindow.resizeEvent(self, event)


    #------------------------------#
    def navigate_to_experiment(self, **kwargs):
        pass