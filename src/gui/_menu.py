"""

"""
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout
from config import *
from utils import func_set_geometry



class menu(QMainWindow):
    """
    Section HOME SCREEN
    """
    def __init__(self):
        super().__init__()

        func_set_geometry(self)
        self.setProperty("class", "screen-background")
        self.centralwidget = QtWidgets.QWidget(self)
              
        self.create_labels()
        self.create_buttons()
        self.setCentralWidget(self.centralwidget)


    #------------------------------#
    def create_buttons(self):
        button_x = int((self.width() - BUTTON_WIDTH) / 2)
        button_y = int((self.height() - BUTTON_HEIGHT) / 2) - GAP

        self.btn_ex = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ex.setGeometry(
            QtCore.QRect(
                button_x, 
                button_y, 
                BUTTON_WIDTH, 
                BUTTON_HEIGHT
                ))
        self.btn_ex.setProperty("class", "menu-button")
        self.btn_ex.setText('EXPERIMENT')
        self.btn_ex.setIcon(QtGui.QIcon('./asset/microscope_white.png'))
        self.btn_ex.setIconSize(QtCore.QSize(32, 32))
        self.btn_ex.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_ex.clicked.connect(
            self.navigate_to_config_trial()
        )

        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(
            QtCore.QRect(
                button_x, 
                button_y + GAP, 
                BUTTON_WIDTH, 
                BUTTON_HEIGHT
                ))
        self.btn_quit.setProperty("class", "menu-button-quit")
        self.btn_quit.setText('EXIT')
        self.btn_quit.setIcon(QtGui.QIcon('./asset/door-exit-white.png'))
        self.btn_quit.setIconSize(QtCore.QSize(32, 32))
        self.btn_quit.setLayoutDirection(QtCore.Qt.LayoutDirection(1))
        self.btn_quit.clicked.connect(
            QtCore.QCoreApplication.quit
        )


    #------------------------------#
    def create_labels(self):
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText("BCI UI TOOL")
        self.title.setProperty("class", "menu-title")
        self.title.show()

        self.footer = QtWidgets.QLabel(self.centralwidget)
        self.footer.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit")
        self.footer.setProperty("class", "menu-footer")
        self.footer.show()


    #------------------------------#
    def resizeEvent(self, event):
        button_x = int((self.width() - BUTTON_WIDTH) / 2)
        button_y = int((self.height() - BUTTON_HEIGHT) / 2) - GAP

        self.title.move(
            int((self.width() - self.title.width()) / 2), 
            MARGIN
            )
        self.footer.move(
            int((self.width() - self.footer.width()) / 2), 
            self.height() - MARGIN - self.footer.height()
            )
        self.btn_ex.move(
            button_x, 
            button_y
            )
        self.btn_quit.move(
            button_x, 
            button_y + int(GAP + 10)
            )

        QtWidgets.QMainWindow.resizeEvent(self, event)

    
    #------------------------------#
    def navigate_to_config_trial(self):
        pass


