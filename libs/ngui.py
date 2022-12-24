#!/usr/bin/python
# -*- coding: utf-8 -*-
from importlib.resources import path
import sys

from yaml import load
sys.path.append("../libs")
import time
import os
import utils
import dbmodule
import splash
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QScreen
from PySide6.QtGui import QIcon
from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QCloseEvent, QDesktopServices
from PySide6.QtCore import Slot
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtCore import QSettings
from PySide6.QtNetwork import QNetworkInformation
from ui.ui_menubar import NMenuBar
from ui.ui_main_container import MainContainer
from ui.ui_favorite_dock import FavoriteDock
from ui.ui_script_dock import ScriptDock

projectpath = f"/{os.path.abspath(sys.argv[0])[1:-len('nsearch.py')]}"
fontpath = f"{projectpath}resources/ArchitectsDaughter-Regular.ttf"
fontloaded = None

class NGui(QMainWindow):

    path = projectpath
    resources_path = f'{path}resources/'
    style_path = f"{resources_path}qcss/"
    dbm = dbmodule
    window_icon = None
    i18n = None
    scripts_list = dict()
    fav_list = dict()
    author_list = dict()
    last_fav_search, last_fav_result = "", ""
    total_scripts, scripts_found = 0, 0
    yaml_vars = None
    gui_script_not = "gui.script_not_found"
    nmenubar = None
    main_widget, tab_view = None, None
    sc_dock, fav_dock = None, None
    status_left, status_right = None, None
    splash, progressbar = None, None    
    welcome, utils = "", None
    settings = None    
    css_files = [
        'default',
        'dark',
        'light'
    ]

    def __init__(self):
        super(NGui, self).__init__()
        self.dbm = dbmodule
        self.i18n = self.dbm.i18n
        self.yaml_vars = self.dbm.yaml_vars
        self.utils = utils.Utils()        
        self.settings = QSettings("NSEarch-GUI", "nsearch")        
        self.init_splash()

    # restore gui state
    def init_UI(self):
        try:
            if "windowstate" in self.settings.childKeys():
                if self.settings.value("windowstate"):                    
                    self.restoreState(
                        QByteArray(self.settings.value("windowstate"))
                    )
            if "geometry" in self.settings.childKeys():
                if self.settings.value("geometry"):                    
                    self.restoreGeometry(
                        QByteArray(self.settings.value("geometry"))
                    )
            else:
                fg = self.frameGeometry()
                ct = QScreen().availableGeometry().center()                
                fg.moveCenter(ct)
                self.move(fg.topLeft())                        
        except Exception as e:
            self.show_exception(e)
            exit()

    # init splash
    def init_splash(self):
        try:
            splash_img = self.resources_path
            splash_img += self.utils.get_splash_img(
                self.yaml_vars["splashAnim"]
            )
            self.splash = splash.NSplash(
                splash_img,
                Qt.WindowStaysOnTopHint
            )        
            self.progressbar = QProgressBar(self.splash)
            self.progressbar.setMaximum(90)
            self.progressbar.setGeometry(
                25, 
                self.splash.height() - 60,
                self.splash.width() - 50,
                20
            )        
            if self.yaml_vars["splashAnim"]:
                self.splash.processFrame.connect(
                    self.show_splash_messages
                )
                self.splash.show()
            else:
                self.splash.show()
                for a in range(0, 91, 1):
                    self.show_splash_messages(a)
                    time.sleep(.03)
            app.processEvents()
        except Exception as e:
            self.show_exception(e)

    # show splash messages
    @Slot(int)
    def show_splash_messages(self, counter):
        if counter == 1:
            self.splash.showMessage(
                self.i18n.t("gui.splash_starting"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )     
        if counter == 10:
            self.splash.showMessage(
                self.i18n.t("gui.splash_script_data"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            self.init_dictionaries()
        elif counter == 40:
            self.splash.showMessage(
                self.i18n.t("gui.splash_load_font"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            self.init_font()            
        elif counter == 70:
            self.splash.showMessage(
                self.i18n.t("gui.splash_init_gui"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            self.init_controls()
        elif counter == 90:
            self.progressbar.setValue(counter)            
            self.progressbar.close()
            self.splash.finish(self)
            self.init_UI()
            self.show()
            return False
        self.progressbar.setValue(counter)

    # init dictionaries
    def init_dictionaries(self):
        self.total_scripts = self.dbm.get_total_scripts()
        self.scripts_found = self.total_scripts
        self.scripts_list = self.dbm.get_data()
        self.author_list = self.dbm.get_author_data()
        self.load_favorites_data()

    # init font
    def init_font(self):
        if fontloaded == -1:
            font_family = "ArchitectsDaughter-Regular.ttf"
            font_name = f"{self.resources_path}{font_family}"
            if not os.path.exists(font_name):
                QMessageBox.information(
                    self,
                    "Font",
                    self.i18n.t("gui.splash_font_not_found"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
                exit()
            if QFontDatabase.addApplicationFont(font_name) == -1:
                QMessageBox.information(
                    self,
                    "Font",
                    self.i18n.t("gui.splash_font_error"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )

    # init GUI controls
    def init_controls(self):
        self.setWindowTitle(
            self.i18n.t("gui.app_name")
        )
        self.author_txt = self.i18n.t("gui.act_author")
        self.sc_dock = ScriptDock(self)
        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            self.sc_dock
        )

        self.fav_dock = FavoriteDock(self)
        self.addDockWidget(
            Qt.RightDockWidgetArea,
            self.fav_dock
        )

        self.main_widget = MainContainer(self)
        self.setCentralWidget(self.main_widget)
        self.nmenubar = NMenuBar(
            self,
            self.sc_dock.toggleViewAction(),
            self.fav_dock.toggleViewAction()
        )
        self.setMenuBar(self.nmenubar)
        self.load_text_translations()
        self.init_GUI()
        self.set_theme()        

    # load i18n language
    def load_language(self, load_text=False):
        if len(self.i18n.get("load_path")) == 0:
            self.i18n.load_path.append("i18n")
        self.i18n.set("locale", self.yaml_vars["lang"])
        self.i18n.set(
            "fallback",
            "en" if self.yaml_vars["lang"] == "es" else "es"
        )
        self.load_translations()
        if load_text:
            self.load_text_translations()

    # load gui translations
    def load_translations(self):       
        self.main_widget.setStatusTip(self.welcome)
        self.nmenubar.load_lang()
        self.sc_dock.load_lang()
        self.fav_dock.load_lang()

    # load language translations
    def load_text_translations(self):
        self.welcome = self.i18n.t(
            "gui.welcome",
            user=os.getenv("USER")
        )
        self.total_text = self.i18n.t(
            "gui.total_scripts",
            total=self.total_scripts
        )        
        self.total_fav_text = self.i18n.t(
            "gui.total_favorites",
            total=len(self.fav_list)
        )
        if self.status_right != None:
            self.status_right.setText(
                self.total_text
            )
        if self.status_left != None:
            self.status_left.setText(
                self.welcome
            )

    # load theme
    def set_theme(self):
        try:
            theme = self.css_files[self.yaml_vars["theme"]-1]
            theme_file = f"{self.style_path}{theme}.css"
            self.setStyleSheet("")
            if os.path.exists(theme_file):
                css_file = open(theme_file, 'r')
                css_content = css_file.read().replace(
                    '\n', ''
                ).replace(
                    '{file}', self.resources_path
                )
                self.setStyleSheet(css_content)
                css_file.close()
            self.load_icons()
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()            
        except Exception as e:
            self.utils.print_traceback(e)

    # load window icons
    def load_icons(self):
        theme = self.css_files[self.yaml_vars["theme"]-1]
        icon_path = f"{self.resources_path}{theme}/"
        self.nmenubar.load_icons(icon_path)

    # update config file vars
    def update_yaml_file(self):
        self.utils.create_config_file(
            self.yaml_vars["searchOnKey"], self.yaml_vars["searchOpt"],
            self.yaml_vars["theme"], self.yaml_vars["splashAnim"],
            self.yaml_vars["lang"], self.yaml_vars["verticalTitle"],
            self.yaml_vars["singleTab"], self.yaml_vars["tabCount"]
        )
        self.yaml_vars = self.utils.get_yaml_vars()

    # init gui components
    def init_GUI(self):
        self.window_icon = f"{self.resources_path}icon.png"
        self.setIconSize(QSize(64, 64))
        self.setWindowIcon(
            QIcon(self.window_icon)
        )
        self.status_left = QLabel(self.welcome)
        self.status_right = QLabel(self.total_text)
        self.status_left.setAlignment(Qt.AlignLeft)        
        self.status_left.setContentsMargins(10,3,0,5)
        self.status_right.setAlignment(Qt.AlignRight)
        self.statusBar().setContentsMargins(3, 3, 0, 0)
        self.statusBar().addWidget(self.status_left)
        self.statusBar().addPermanentWidget(self.status_right)               
        self.main_widget.create_home_tab()

    # load favorites data in dict
    def load_favorites_data(self):
        self.fav_list = self.dbm.get_favorites()
        tmp = {}
        for index in self.fav_list:
            fav = self.fav_list[index]
            tmp[str(fav["name"])] = fav["ranking"]
        self.fav_list = tmp

    # get favorite image
    def get_favorite_img(self, ranking):
        if ranking == 0:
            return QIcon(f"{self.resources_path}normal.png")
        if ranking == 1:
            return QIcon(f"{self.resources_path}great.png")
        if ranking == 2:
            return QIcon(f"{self.resources_path}super-great.png")

    # reload gui translations
    def reload_translations(self, update=True):
        self.load_language(True)
        self.main_widget.remove_script_tabs()
        self.sc_dock.load_scripts()
        self.fav_dock.load_favorites()
        self.load_text_translations()
        if update:
            self.update_yaml_file()        
  
    # close event
    @Slot(QCloseEvent)
    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowstate', self.saveState())
        event.accept()

    # show exception
    def show_exception(self, e):
        self.utils.print_traceback(e)
        msg = e.args[0] if type(e) == Exception else e
        QMessageBox.information(
            self,
            self.i18n.t("gui.exception"),
            str(msg), QMessageBox.Ok,
            QMessageBox.Ok
        )

    # open webbrowser
    def open_url(self, url):
        qurl = None
        if isinstance(url, str):
            qurl = QUrl(url)        
        if not qurl.isEmpty() and qurl.url():
            QDesktopServices.openUrl(qurl)

if __name__ == "libs.ngui":
    global app
    app = QApplication(sys.argv)
    if os.path.exists(fontpath):
        fontloaded = QFontDatabase.addApplicationFont(fontpath)        
    else:
        print(dbmodule.i18n.t("gui.font not found"))
    ngui = NGui()
    app.setStyle('Fusion')
    app.setApplicationName("NSEarch_Gui")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("NSEarch_Gui")
    sys.exit(app.exec())