#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QMovie, QScreen
from PySide6.QtCore import Signal

class NSplash(QSplashScreen):

    counter = 0
    processFrame = Signal(int, name='processFrame')

    def __init__(self, anim, flags):
        QSplashScreen.__init__(self, QPixmap(), flags)
        self.setContentsMargins(5, 5, 15, 5)
        screen = QScreen(self).availableSize()        
        self.setGeometry(
            ((screen.width()-self.geometry().width())/2),
            ((screen.height()-self.geometry().height())/2),
            self.geometry().width(),
            self.geometry().height()
        )
        self.movie = QMovie(anim)
        self.movie.frameChanged.connect(self.nextFrame)
        self.movie.start()

    def nextFrame(self):
        self.counter += 1
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        self.processFrame.emit(self.counter)
