#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

class WebPage(QWebEnginePage):

    external_window = False

    def setSettings(self):        
        self.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            False
        )
        self.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True
        )
        self.settings().setAttribute(
            QWebEngineSettings.PdfViewerEnabled,
            False
        )
        self.settings().setAttribute(
            QWebEngineSettings.WebGLEnabled,
            False
        )
        self.settings().setAttribute(
            QWebEngineSettings.LocalStorageEnabled,
            False
        )
        self.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled,
            True
        )
        self.settings().setAttribute(
            QWebEngineSettings.PluginsEnabled,
            False
        )
        self.settings().setAttribute(
            QWebEngineSettings.ErrorPageEnabled,
            False
        )
    
    def acceptNavigationRequest(self, url=QUrl, type=QWebEnginePage.NavigationType, isMainFrame=bool):
        del isMainFrame
        if type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            if not url.isEmpty() and url.url().startswith("https"):                
                QDesktopServices.openUrl(url)
                return False
        return True
