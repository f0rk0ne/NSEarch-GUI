#!/usr/bin/python
#-*- coding: utf-8 -*- 
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import pyqtSignal

class NSplash(QSplashScreen):

    counter = 0
    processFrame = pyqtSignal( int, name='processFrame')

    def __init__(self, anim, flags):
        QSplashScreen.__init__(self, QPixmap(), flags )
        self.setContentsMargins( 5,5,15,5 )
        self.movie = QMovie(anim)
        self.movie.frameChanged.connect(self.nextFrame)
        self.movie.start()  

    def nextFrame(self):
        self.counter += 1
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        self.processFrame.emit(self.counter)