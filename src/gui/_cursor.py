import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, 
    QGraphicsScene, 
    QGraphicsPixmapItem,
    QGraphicsView, 
    QGraphicsEllipseItem, 
    QLabel
    )
from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPen, QPixmap, QBrush, QColor


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000
CURSOR_SPEED = 100



class CustomImageItem(QGraphicsPixmapItem):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path

        # Load the image
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)

    # # Override boundingRect to ensure the image resizes proportionally
    # def boundingRect(self) -> QRectF:
    #     if not self.pixmap:
    #         return QRectF()
    #     return QRectF(0, 0, self.pixmap.width(), self.pixmap.height())
    


class GridScene(QGraphicsScene):
    def __init__(self, width, height, grid_size, pen=QPen()):
        super().__init__(0, 0, width, height)
        self.grid_size = grid_size
        self.pen = pen

    def drawGrid(self):
        width = int(self.width())
        height = int(self.height())
        # Draw vertical grid lines
        for x in range(0, width, self.grid_size):
            self.addLine(x, 0, x, height, self.pen)
        # Draw horizontal grid lines
        for y in range(0, height, self.grid_size):
            self.addLine(0, y, width, y, self.pen)


class Cursor_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.scene = QGraphicsScene()
        # self.setWindowTitle("Object Movement")
        # self.setGeometry(300, 300, 600, 400)
        # self.drawGrid()

        self.scene = GridScene(
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            grid_size=50
        )
        self.setWindowTitle("Object Movement")
        self.scene.drawGrid()

        # set view
        self.view = QGraphicsView(self.scene)

        ## object item
        coord_x_center = int(WINDOW_WIDTH/2)
        coord_y_center = int(WINDOW_HEIGHT/2)
        self.object = QGraphicsEllipseItem(coord_x_center, coord_y_center, 50, 50)
        self.object.setBrush(QBrush(QColor('blue')))
        ## mouse
        # self.object = CustomImageItem('./asset/mouse.png') 
        # self.object.setPos(coord_x_center, coord_y_center)
        
        # add object to scene
        self.scene.addItem(self.object)
        # set view to display
        self.setCentralWidget(self.view)

        # # Start the animation timer
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.move_cursor)
        # self.timer.start(500)
        


    def constraint_cursor(self, x, y):
        if (x < 0): 
            x1 = 0
        elif (x > WINDOW_WIDTH): 
            x1 = WINDOW_WIDTH
        else: 
            x1 = x

        if (y < 0): 
            y1 = 0
        elif (y > WINDOW_HEIGHT): 
            y1 = WINDOW_HEIGHT
        else: 
            y1 = y

        return (x1, y1)


    def update_coordinate(self, label:int):
        x = self.object.pos().x()
        y = self.object.pos().y()

        if label == 1: # RIGHT
            return self.constraint_cursor(x + CURSOR_SPEED, y)
        elif label == 2: # LEFT
            return self.constraint_cursor(x - CURSOR_SPEED, y)
        elif label == 3: # UP
            return self.constraint_cursor(x, y + CURSOR_SPEED)
        elif label == 4: # DOWN
            return self.constraint_cursor(x, y - CURSOR_SPEED)


    # def move_cursor(self):
    #     x, y = self.update_coordinate(label=random.randint(1,4))
    #     self.object.setPos(x, y)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Cursor_Window()
    window.show()
    sys.exit(app.exec_())