import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import pygame as pg
import pygame
from os import path

pygame.init()
pg.init()


class Text_class:
    def __init__(self, x, y, text, color1, color2):
        self.item = 'text'
        self.x = x
        self.y = y
        self.text = text
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.setFont(QFont('Helvetica', 40))
        x = self.x
        y = self.y

        i = 0
        most = 0

        for harf in self.text:
            if harf != "\n":
                painter.drawText(x, y, harf)
                x += 35
                i += 1

                if i > most:
                    most = i
            else:
                i = 0
                x = self.x
                y += 60

        painter.setBrush(QtCore.Qt.transparent)
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(self.x, self.y - 55, most * 35, (self.text.count('\n') + 1) * 60)


class BrushPoint:
    def __init__(self, x, y, color1, color2):
        self.item = 'brush'
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color1)
        painter.drawEllipse(self.x - 5, self.y - 5, 9, 9)


class Line:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'line'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Circle:
    def __init__(self, cx, cy, x, y, color1, color2, CheckSquareColor):
        self.item = 'circle'
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.CheckSquareColor = CheckSquareColor

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        radius = int(((self.cx - self.x) ** 2 + (self.cy - self.y) ** 2) ** 0.5)
        painter.drawEllipse(self.cx - radius, self.cy - radius, radius * 2, radius * 2)


class Rectangle:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'rect'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawRect(self.sx, self.sy, self.ex - self.sx, self.ey - self.sy)


class RoundedRect:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'rounders'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawRoundedRect(self.sx, self.sy, self.ex - self.sx, self.ey - self.sy, 30.0, 15.0)


class Oval:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'oval'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawRoundedRect(self.sx, self.sy, self.ex - self.sx, self.ey - self.sy, 360.0, 360.0)


class Arc:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'arc'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawArc(self.sx, self.sy, self.ex - self.sx, (self.ey - self.sy) * 4, 30 * 16, 120 * 16)


class Chord:
    def __init__(self, sx, sy, ex, ey, color1, color2):
        self.item = 'chord'
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color1 = color1
        self.color2 = color2

    def draw(self, painter):
        painter.setBrush(QBrush(self.color1))
        painter.setPen(self.color2)
        painter.drawChord(self.sx, self.sy, (self.ex - self.sx), int((self.ey - self.sy) * 4), 30 * 16, 120 * 16)


class Canvas(QWidget):
    def __init__(self, _window):
        super(Canvas, self).__init__()

        self.window = _window
        self.file_save = "новый файл1.png"
        self.window.setWindowTitle("LibertyPain v2.0 - " + self.file_save)
        self.objects = []
        self.instrument = 'brush'
        self.color1 = QColor(0, 0, 0)
        self.color2 = QColor(255, 0, 0)
        self.CheckSquareColor = QColor(0, 0, 0)
        self.mus = pg.mixer.Sound('mus.mp3')

        self.memory = []

        top, left, width, height = 0, 0, 1920, 1080
        self.setGeometry(top, left, width, height)

        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_ARGB32)
        self.image.fill(QtCore.Qt.white)
        self.imageDraw = QtGui.QImage(1920, 1080, QtGui.QImage.Format_ARGB32)
        self.imageDraw.fill(QtCore.Qt.white)

        self.add_to_memory()

        self.drawing = False
        self.brushSize = 5
        self._clear_size = 10
        self.brushColor = QtGui.QColor(QtCore.Qt.black)
        self.lastPoint = QtCore.QPoint()

    def paintEvent(self, event):
        canvasPainter = QtGui.QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        canvasPainter.drawImage(self.imageDraw.rect(), self.imageDraw, self.imageDraw.rect())

        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):
        self.Changed()
        self.drawing = True

        if self.instrument == 'brush':
            self.lastPoint = event.pos()

        elif self.instrument == 'line':
            self.objects.append(Line(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'circle':
            self.objects.append(Circle(event.x(), event.y(), event.x(), event.y(), QtCore.Qt.transparent, self.color2,
                                       self.CheckSquareColor))
            self.update()
        elif self.instrument == 'rect':
            self.objects.append(Rectangle(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'rounders':
            self.objects.append(RoundedRect(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'oval':
            self.objects.append(Oval(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'arc':
            self.objects.append(Arc(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'chord':
            self.objects.append(Chord(event.x(), event.y(), event.x(), event.y(), self.color1, self.color2))
            self.update()
        elif self.instrument == 'text':
            self.objects.append(Text_class(event.x(), event.y(), '', self.color1, self.color2))
            self.update()
        elif self.instrument == 'eraser':
            self.lastPoint = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        self.drawing = True
        if self.instrument == 'brush':
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.color1, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            painter.end()
            self.lastPoint = event.pos()
            self.update()

        elif self.instrument == 'eraser':
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))

            r = QtCore.QRect(QtCore.QPoint(), self._clear_size * QtCore.QSize())
            r.moveCenter(event.pos())
            painter.save()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            painter.eraseRect(r)
            painter.restore()

            painter.end()
            self.lastPoint = event.pos()
            self.update()

        elif self.instrument == 'line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'circle':
            self.objects[-1].x = event.x()
            self.objects[-1].y = event.y()
            self.update()
        elif self.instrument == 'rect':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'rounders':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'oval':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'arc':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'chord':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False
        self.add_to_memory()

    def setCursorEraser(self):
        pixmap = QtGui.QPixmap(QtCore.QSize(1, 1) * self._clear_size)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 4))
        painter.drawRect(pixmap.rect())
        painter.end()
        cursor = QtGui.QCursor(pixmap)

        QtWidgets.QApplication.setOverrideCursor(cursor)

    def setCursorNormal(self):
        QtWidgets.QApplication.restoreOverrideCursor()

    def Changed(self):
        if len(self.objects) > 0:
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.objects[-1].color2, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))
            painter.setBrush(self.objects[-1].color1)

            if self.objects[-1].item == "text":
                painter.setFont(QFont('Helvetica', 40))

                x = self.objects[-1].x
                y = self.objects[-1].y

                for harf in self.objects[-1].text:
                    if harf != "\n":
                        painter.drawText(x, y, harf)
                        x += 35
                    else:
                        x = self.objects[-1].x
                        y += 60

            elif self.objects[-1].item == "line":
                painter.drawLine(self.objects[-1].sx, self.objects[-1].sy, self.objects[-1].ex, self.objects[-1].ey)

            elif self.objects[-1].item == "circle":
                radius = int(((self.objects[-1].cx - self.objects[-1].x) ** 2 + (
                            self.objects[-1].cy - self.objects[-1].y) ** 2) ** 0.5)
                painter.drawEllipse(self.objects[-1].cx - radius, self.objects[-1].cy - radius, radius * 2, radius * 2)

            elif self.objects[-1].item == "rect":
                painter.drawRect(self.objects[-1].sx, self.objects[-1].sy, self.objects[-1].ex - self.objects[-1].sx,
                                 self.objects[-1].ey - self.objects[-1].sy)

            elif self.objects[-1].item == "rounders":
                painter.drawRoundedRect(self.objects[-1].sx, self.objects[-1].sy,
                                        self.objects[-1].ex - self.objects[-1].sx,
                                        self.objects[-1].ey - self.objects[-1].sy, 30.0, 15.0)

            elif self.objects[-1].item == "oval":
                painter.drawRoundedRect(self.objects[-1].sx, self.objects[-1].sy,
                                        self.objects[-1].ex - self.objects[-1].sx,
                                        self.objects[-1].ey - self.objects[-1].sy, 360.0, 360.0)

            elif self.objects[-1].item == "arc":
                painter.drawArc(self.objects[-1].sx, self.objects[-1].sy, self.objects[-1].ex - self.objects[-1].sx,
                                (self.objects[-1].ey - self.objects[-1].sy) * 4, 30 * 16, 120 * 16)

            elif self.objects[-1].item == "chord":
                painter.drawChord(self.objects[-1].sx, self.objects[-1].sy, (self.objects[-1].ex - self.objects[-1].sx),
                                  int((self.objects[-1].ey - self.objects[-1].sy) * 4), 30 * 16, 120 * 16)

            painter.end()
            self.objects.pop(-1)

            self.add_to_memory()

            self.update()

    def add_to_memory(self):
        if len(self.memory) == 50:
            pix = QPixmap.fromImage(self.imageDraw)
            self.memory[-1] = pix
        else:
            pix = QPixmap.fromImage(self.imageDraw)
            self.memory.append(pix)

    def setEraser(self):
        self.setCursorEraser()
        self.Changed()
        self.instrument = 'eraser'

    def setText(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'text'

    def setBrush(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'brush'

    def setLine(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'line'

    def setCircle(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'circle'

    def setRect(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'rect'

    def setRoundedRect(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'rounders'

    def setOval(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'oval'

    def setArc(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'arc'

    def setChord(self):
        self.setCursorNormal()
        self.Changed()
        self.instrument = 'chord'

    def setColIn(self):
        self.color1 = QColorDialog.getColor()

    def setCol2(self):
        self.color2 = QColorDialog.getColor()

    def Music_on(self):
        self.mus.play()

    def Music_off(self):
        self.mus.stop()

    def setClear(self):
        self.add_to_memory()
        self.objects.clear()

        self.imageDraw.fill(QtCore.Qt.transparent)

        self.update()

    def save_file(self):
        if path.exists(self.file_save):
            filePath = self.file_save
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;Все файлы(*.*) ")

        if filePath == "":
            return

        self.imageDraw.save(filePath)

        self.file_save = filePath
        self.window.setWindowTitle("LibertyPain v2.0 - " + self.file_save)

    def save_file_what(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;Все файлы(*.*) ")

        if filePath == "":
            return

        self.imageDraw.save(filePath)

        self.file_save = filePath
        self.window.setWindowTitle("LibertyPain v2.0 - " + self.file_save)

    def open(self):
        self.imageDraw.fill(QtCore.Qt.transparent)
        self.memory.clear()

        imagePath, _ = QFileDialog.getOpenFileName()

        self.file_save = imagePath
        self.window.setWindowTitle("LibertyPain v2.0 - " + self.file_save)

        painter = QPainter(self.imageDraw)
        pixmap = QPixmap(imagePath)
        painter.drawPixmap(self.imageDraw.rect(), pixmap)
        painter.end()

    def back(self):
        if len(self.memory) > 1:
            self.memory.pop(-1)
            painter = QPainter(self.imageDraw)
            painter.drawPixmap(self.imageDraw.rect(), self.memory[-1])
            painter.end()

            self.update()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        uic.loadUi('window.ui', self)

        self.setWindowTitle("LibertyPain v2.0")
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        self.capsLck = False

        self.setWindowIcon(QIcon('image.png'))

        self.action_eraser.triggered.connect(self.centralWidget().setEraser)
        self.action_text.triggered.connect(self.centralWidget().setText)
        self.action_brush.triggered.connect(self.centralWidget().setBrush)
        self.action_line.triggered.connect(self.centralWidget().setLine)
        self.action_circle.triggered.connect(self.centralWidget().setCircle)
        self.action_rect.triggered.connect(self.centralWidget().setRect)
        self.action_rectangle.triggered.connect(self.centralWidget().setRoundedRect)
        self.action_oval.triggered.connect(self.centralWidget().setOval)
        self.action_arc.triggered.connect(self.centralWidget().setArc)
        self.action_chord.triggered.connect(self.centralWidget().setChord)
        self.action_color_inside.triggered.connect(self.centralWidget().setColIn)
        self.action__color_outside.triggered.connect(self.centralWidget().setCol2)
        self.action_music_on.triggered.connect(self.centralWidget().Music_on)
        self.action_music_off.triggered.connect(self.centralWidget().Music_off)
        self.action_clear.triggered.connect(self.centralWidget().setClear)
        self.action_dosya_kaydet.triggered.connect(self.centralWidget().save_file)
        self.action_dosya_farkli_kaydet.triggered.connect(self.centralWidget().save_file_what)
        self.action_dosya_ac.triggered.connect(self.centralWidget().open)
        self.action_geri_al.triggered.connect(self.centralWidget().back)

    def keyPressEvent(self, e):
        if self.canvas.objects[-1].item == "text":
            i = e.key()
            letter = ''
            if i == 32:
                letter = ' '
            if e.key() == QtCore.Qt.Key_Return:
                letter = "\n"
            if (1040 <= i and i <= 1105) or (65 <= i and i <= 90):
                if self.capsLck:
                    letter = chr(i)
                else:
                    letter = chr(i + 32)
            if letter != '':
                self.canvas.objects[-1].text += letter
                self.canvas.update()
            if e.key() == QtCore.Qt.Key_Backspace:
                if len(self.canvas.objects[-1].text) == 1:
                    self.canvas.objects.pop(-1)
                    self.canvas.update()
                else:
                    self.canvas.objects[-1].text = self.canvas.objects[-1].text[:-1]
                    self.canvas.update()
            if e.key() == QtCore.Qt.Key_CapsLock:
                if self.capsLck:
                    self.capsLck = False
                else:
                    self.capsLck = True

        if e.key() == QtCore.Qt.Key_Escape:
            if len(self.canvas.objects) > 0 and self.canvas.drawing:
                self.canvas.objects.pop(-1)
                self.canvas.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())