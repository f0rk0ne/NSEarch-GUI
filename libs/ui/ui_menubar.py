from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QDockWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QRect, QObject, Signal
from PySide6.QtCore import QThread
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction
import os

class NMenuBar(QMenuBar):

    win = None
    menu_app = None
    m_quit = None
    menu_options = None
    menu_language = None
    m_spanish, m_english = None, None
    menu_theme = None
    m_default, m_dark, m_light = None, None, None
    m_searchkey = None
    m_splash = None
    menu_search_opts = None
    m_name, m_author, m_category = None, None, None
    m_vertical_title = None
    menu_tabs = None
    m_single_tab = None
    menu_tab_count = None
    m_five, m_ten = None, None
    m_twenty, m_thirty = None, None
    tabs = None
    menu_windows = None
    m_scriptdock, m_favoritedock = None, None
    menu_about = None
    m_about, m_about_qt, m_updatedb = None, None, None
    '''menus = [
        {"control": self.menu_app,"tr_key": "gui.menu_app"}
        {}
    ]'''

    def __init__(self, parent, sdock, fdock):
        super(NMenuBar, self).__init__(parent)
        try:
            self.win = parent        
            self.m_scriptdock = sdock
            self.m_favoritedock = fdock
            self.init_menus()
            self.init_menu_checkeable()
            self.load_lang()
        except Exception as e:
            parent.show_exception(e)

    def init_menus(self):
        self.setStyleSheet(
            "font-family:ArchitectsDaughter;"
        )
        self.setObjectName(u"menubar")
        self.setGeometry(QRect(0, 0, 860, 24))
                
        self.init_menuapp()
        self.addMenu(self.menu_app)

        self.init_menuopts()
        self.addMenu(self.menu_options)

        self.init_menu_tabs()        
        self.addMenu(self.menu_tabs)

        self.init_menuwin()
        self.addMenu(self.menu_windows)

        self.init_menu_about()
        self.addMenu(self.menu_about)

    def init_menuapp(self):
        self.menu_app = QMenu(u"&App", self)
        self.menu_app.setObjectName(u"menu_app")

        self.m_configuration = QAction(
            "Configuration",
            self.win
        )
        self.m_configuration.setObjectName(u"m_configuration")
        self.m_configuration.setShortcut(u"Ctrl+p")
        self.m_configuration.triggered.connect(
            self.show_config
        )
        self.menu_app.addAction(self.m_configuration)

        self.m_quit = QAction(u"Quit", self.win)
        self.m_quit.setObjectName(u"m_quit")
        self.m_quit.setShortcut(u"Ctrl+Q")        
        self.m_quit.triggered.connect(QApplication.quit)        
        self.menu_app.addAction(self.m_quit)

    def init_menuopts(self):
        self.init_submenus_opts()
        self.menu_options = QMenu(u"O&ptions", self)
        self.menu_options.setObjectName(u"menu_options")        

        self.create_menu_lang()
        self.menu_options.addAction(self.menu_language.menuAction())
        self.menu_options.addSeparator()

        self.create_menu_theme()
        self.menu_options.addAction(self.menu_theme.menuAction())
        self.menu_options.addSeparator()

        self.menu_options.addAction(self.m_searchkey)
        self.menu_options.addSeparator()

        self.create_menu_searchopts()
        self.menu_options.addAction(self.menu_search_opts.menuAction())        
        self.menu_options.addSeparator()
        self.menu_options.addAction(self.m_splash)
        self.menu_options.addSeparator()
        self.menu_options.addAction(self.m_vertical_title)
        self.menu_options.addSeparator()        

    def create_menu_lang(self):
        self.init_submenu_lang()
        self.menu_language = QMenu(
            "Language",
            self.menu_options
        )
        self.menu_language.setObjectName(u"menu_language")       
        self.menu_language.addAction(self.m_spanish)
        self.menu_language.addSeparator()
        self.menu_language.addAction(self.m_english)

    def init_submenu_lang(self):
        self.m_spanish = QAction(u"Spanish", self.win)
        self.m_spanish.setObjectName(u"m_spanish")
        self.m_spanish.setCheckable(True)        
        self.m_spanish.triggered.connect(self.select_lang)

        self.m_english = QAction(u"English", self.win)
        self.m_english.setObjectName(u"m_english")
        self.m_english.setCheckable(True)
        self.m_english.triggered.connect(self.select_lang)

    def create_menu_theme(self):
        self.menu_theme = QMenu(u"Theme", self.menu_options)
        self.menu_theme.setObjectName(u"menu_theme")        
        self.init_submenu_theme()

        self.menu_theme.addAction(self.m_default)
        self.menu_theme.addSeparator()
        self.menu_theme.addAction(self.m_dark)
        self.menu_theme.addSeparator()
        self.menu_theme.addAction(self.m_light)

    def init_submenu_theme(self):
        self.m_default = QAction(u"Default", self.win)
        self.m_default.setObjectName(u"m_default")
        self.m_default.setCheckable(True)
        self.m_default.triggered.connect(self.select_theme)

        self.m_dark = QAction(u"Dark", self.win)
        self.m_dark.setObjectName(u"m_dark")
        self.m_dark.setCheckable(True)
        self.m_dark.triggered.connect(self.select_theme)

        self.m_light = QAction(u"Light", self.win)
        self.m_light.setObjectName(u"m_light")
        self.m_light.setCheckable(True)
        self.m_light.triggered.connect(self.select_theme)

    def init_submenus_opts(self):
        self.m_searchkey = QAction(
            "Search On Key Pressed", self.win
        )
        self.m_searchkey.setObjectName(u"m_searchkey")
        self.m_searchkey.setCheckable(True)
        self.m_searchkey.triggered["bool"].connect(
            self.select_key_on
        )
        self.m_splash = QAction(u"Splash Animation", self.win)
        self.m_splash.setObjectName(u"m_splash")
        self.m_splash.setCheckable(True)
        self.m_splash.triggered["bool"].connect(
            self.toggle_splash_anim
        )

        self.m_vertical_title = QAction(
            "Vertical Title",
            self.win
        )
        self.m_vertical_title.setObjectName(u"m_vertical_title")
        self.m_vertical_title.setCheckable(True)
        self.m_vertical_title.triggered["bool"].connect(
            self.set_vertical_title
        )

    def create_menu_searchopts(self):        
        self.menu_search_opts = QMenu(
            "Search Options",
            self.menu_options
        )
        self.init_submenus_searchopts()
        self.menu_search_opts.setObjectName(u"menu_search_opts")
        self.menu_search_opts.addAction(self.m_name)
        self.menu_search_opts.addSeparator()
        self.menu_search_opts.addAction(self.m_author)
        self.menu_search_opts.addSeparator()
        self.menu_search_opts.addAction(self.m_category)

    def init_submenus_searchopts(self):
        self.m_name = QAction(u"Name", self.win)
        self.m_name.setObjectName(u"m_name")
        self.m_name.setCheckable(True)
        self.m_name.triggered.connect(self.select_searchby)

        self.m_author = QAction(u"Author", self.win)
        self.m_author.setObjectName(u"m_author")
        self.m_author.setCheckable(True)
        self.m_author.triggered.connect(self.select_searchby)

        self.m_category = QAction(u"Category", self.win)
        self.m_category.setObjectName(u"m_category")
        self.m_category.setCheckable(True)
        self.m_category.triggered.connect(self.select_searchby)

    def init_menu_tabs(self):
        self.menu_tabs = QMenu("&Tabs", self)
        self.menu_tabs.setObjectName("menu_tabs")

        self.m_single_tab = QAction(u"Single Tab", self.win)
        self.m_single_tab.setObjectName(u"m_single_tab")
        self.m_single_tab.setCheckable(True)
        self.m_single_tab.triggered['bool'].connect(
            self.set_single_tab
        )

        self.create_menu_tabcount()
        self.menu_tabs.addAction(
            self.m_single_tab
        )
        self.menu_tabs.addSeparator()
        self.menu_tabs.addAction(
            self.menu_tab_count.menuAction()
        )

    def create_menu_tabcount(self):
        self.menu_tab_count = QMenu(
            u"Tab Count",
            self.menu_tabs
        )
        self.menu_tab_count.setObjectName(u"menu_tab_count")
        self.init_submenus_tabcount()

        self.menu_tab_count.addAction(self.m_five)
        self.menu_tab_count.addSeparator()
        self.menu_tab_count.addAction(self.m_ten)
        self.menu_tab_count.addSeparator()
        self.menu_tab_count.addAction(self.m_twenty)
        self.menu_tab_count.addSeparator()
        self.menu_tab_count.addAction(self.m_thirty)

    def init_submenus_tabcount(self):
        self.m_five = QAction(u"5", self.win)
        self.m_five.setObjectName(u"m_five")
        self.m_five.setText(u"5")        
        self.m_five.setCheckable(True)
        self.m_five.triggered.connect(self.set_tabcount)            

        self.m_ten = QAction(u"10", self.win)
        self.m_ten.setObjectName(u"m_ten")
        self.m_ten.setText(u"10")        
        self.m_ten.setCheckable(True)
        self.m_ten.triggered.connect(self.set_tabcount)

        self.m_twenty = QAction(u"20", self.win)
        self.m_twenty.setObjectName(u"m_twenty")
        self.m_twenty.setText(u"20")        
        self.m_twenty.setCheckable(True)
        self.m_twenty.triggered.connect(self.set_tabcount)

        self.m_thirty = QAction(u"30", self.win)
        self.m_thirty.setObjectName(u"m_thirty")
        self.m_thirty.setText(u"30")        
        self.m_thirty.setCheckable(True)
        self.m_thirty.triggered.connect(self.set_tabcount)
        self.tabs = [
            self.m_five, self.m_ten,
            self.m_twenty, self.m_thirty
        ]

    def init_menuwin(self):
        self.menu_windows = QMenu(u"&Windows", self)
        self.menu_windows.setObjectName(u"menu_windows")        
        self.menu_windows.addAction(self.m_scriptdock)
        self.menu_windows.addSeparator()
        self.menu_windows.addAction(self.m_favoritedock)

    def init_menu_about(self):
        self.init_submenus_about()
        self.menu_about = QMenu(u"A&bout", self)
        self.menu_about.setObjectName(u"menu_about")
        
        self.menu_about.addAction(self.m_about)
        self.menu_about.addSeparator()
        self.menu_about.addAction(self.m_about_qt)
        self.menu_about.addSeparator()
        self.menu_about.addAction(self.m_updatedb)

    def init_submenus_about(self):
        self.m_about = QAction(u"Developer", self.win)
        self.m_about.setObjectName(u"m_about")        
        self.m_about.triggered.connect(
            self.init_author_window
        )        
        
        self.m_about_qt = QAction(u"About Qt", self.win)
        self.m_about_qt.setObjectName(u"m_about_qt")        
        self.m_about_qt.setMenuRole(QAction.MenuRole.AboutQtRole)
        self.m_about_qt.triggered.connect(
            QApplication.aboutQt
        )

        self.m_updatedb = QAction(u"Update DB", self.win)
        self.m_updatedb.setObjectName(u"m_updatedb")
        self.m_updatedb.triggered.connect(
            self.check_database
        )

    def load_lang(self):        
        self.menu_app.setTitle(         
            self.win.i18n.t(u"gui.menu_app")
        )
        self.m_configuration.setText(         
            self.win.i18n.t(u"gui.act_configuration")
        )
        self.m_quit.setText(         
            self.win.i18n.t(u"gui.act_quit")
        )
        self.menu_options.setTitle(
            self.win.i18n.t(u"gui.menu_options")
        )
        self.menu_language.setTitle(
            self.win.i18n.t(u"gui.menu_language")
        )
        self.m_spanish.setText(
            self.win.i18n.t(u"gui.act_spanish")
        )
        self.m_english.setText(
            self.win.i18n.t(u"gui.act_english")
        )
        self.menu_theme.setTitle(
            self.win.i18n.t(u"gui.menu_theme")
        )
        self.m_default.setText(
            self.win.i18n.t(u"gui.act_default")
        )
        self.m_dark.setText(
            self.win.i18n.t(u"gui.act_dark")
        )
        self.m_light.setText(
            self.win.i18n.t(u"gui.act_light")
        )
        self.m_searchkey.setText(
            self.win.i18n.t(u"gui.act_search_on_key")
        )
        self.menu_search_opts.setTitle(
            self.win.i18n.t(u"gui.menu_search_opts")
        )
        self.m_name.setText(
            self.win.i18n.t(u"gui.act_name")
        )
        self.m_author.setText(
            self.win.i18n.t(u"gui.act_author")
        )
        self.m_category.setText(
            self.win.i18n.t(u"gui.act_category")
        )
        self.menu_tabs.setTitle(        
            self.win.i18n.t(u"gui.menu_tabs")
        )
        self.m_single_tab.setText(
            self.win.i18n.t(u"gui.act_single_tab")
        )
        self.menu_tab_count.setTitle(
            self.win.i18n.t(u"gui.act_tab_count")
        )
        self.menu_windows.setTitle(
            self.win.i18n.t(u"gui.menu_windows")
        )
        self.m_scriptdock.setText(
            self.win.i18n.t(u"gui.act_scripts")
        )
        self.m_favoritedock.setText(
            self.win.i18n.t(u"gui.act_favorite")
        )
        self.menu_about.setTitle(
            self.win.i18n.t(u"gui.menu_about")
        )
        self.m_about.setText(
            self.win.i18n.t(u"gui.act_about")
        )
        self.m_about_qt.setText(
            self.win.i18n.t(u"gui.act_about_qt")
        )
        self.m_updatedb.setText(
            self.win.i18n.t(u"gui.update_db")
        )
        self.m_vertical_title.setText(
            self.win.i18n.t(u"gui.act_vertical_title")
        )        
        self.load_menu_statustip()
        
    def load_menu_statustip(self):
        self.m_configuration.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_configuration")}'
        )
        self.m_quit.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_quit")}'
        )
        self.m_spanish.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_spanish")}'
        )
        self.m_english.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_english")}'
        )
        self.m_default.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_default")}'
        )
        self.m_dark.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_dark")}'
        )
        self.m_light.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_light")}'
        )
        self.m_searchkey.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_search_on")}'
        )
        self.m_name.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_name")}'
        )
        self.m_author.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_author")}'
        )
        self.m_category.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_category")}'
        )
        self.m_scriptdock.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_scripts")}'
        )
        self.m_favoritedock.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_favorite")}'
        )
        self.m_about.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_about_app")}'
        )
        self.m_about_qt.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_about_qt")}'
        )
        self.m_splash.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_anim")}'
        )
        self.m_vertical_title.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_vertical_title")}'
        )
        self.m_single_tab.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_single_tab")}'
        )
        self.m_five.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_tab_count", count=5)}'
        ) 
        self.m_ten.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_tab_count", count=10)}'
        ) 
        self.m_twenty.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_tab_count", count=20)}'
        ) 
        self.m_thirty.setStatusTip(
            f'  {self.win.i18n.t(u"gui.st_tab_count", count=30)}'
        ) 

    def load_icons(self, theme):
        self.m_configuration.setIcon(
            QIcon(f"{theme}config.png")
        )
        self.m_quit.setIcon(
            QIcon(f"{theme}exit.png")
        )
        self.m_about.setIcon(
            QIcon(f"{theme}people.png")
        )
        self.m_about_qt.setIcon(
            QIcon(f"{theme}qt.png")
        )
        self.menu_language.setIcon(
            QIcon(f"{theme}lang.png")
        )
        self.menu_theme.setIcon(
            QIcon(f"{theme}theme.png")
        )
        self.menu_search_opts.setIcon(
            QIcon(f"{theme}searchopt.png")
        )

    def init_menu_checkeable(self):
        self.m_spanish.setChecked(
            self.win.yaml_vars["lang"] == 'es'
        )
        self.m_english.setChecked(
            self.win.yaml_vars["lang"] == 'en'
        )
        self.m_searchkey.setChecked(
            self.win.yaml_vars["searchOnKey"]
        )
        self.m_default.setChecked(
            self.win.yaml_vars["theme"] == 1
        )
        self.m_dark.setChecked(
            self.win.yaml_vars["theme"] == 2
        )
        self.m_light.setChecked(
            self.win.yaml_vars["theme"] == 3
        )
        self.m_name.setChecked(
            self.win.yaml_vars["searchOpt"] == 1
        )
        self.m_author.setChecked(
            self.win.yaml_vars["searchOpt"] == 2
        )
        self.m_category.setChecked(
            self.win.yaml_vars["searchOpt"] == 3
        )
        self.m_splash.setChecked(
            self.win.yaml_vars["splashAnim"]
        )
        self.m_vertical_title.setChecked(
            self.win.yaml_vars["verticalTitle"]
        )
        self.m_single_tab.setChecked(
            self.win.yaml_vars["singleTab"]
        )
        self.m_five.setChecked(
            self.win.yaml_vars["tabCount"] == 5
        )
        self.m_ten.setChecked(
            self.win.yaml_vars["tabCount"] == 10
        )
        self.m_twenty.setChecked(
            self.win.yaml_vars["tabCount"] == 20
        )
        self.m_thirty.setChecked(
            self.win.yaml_vars["tabCount"] == 30
        )
        self.set_dock_features()

    def set_dock_features(self):
        if self.win.yaml_vars["verticalTitle"]:
            self.win.fav_dock.setFeatures(
                QDockWidget.DockWidgetVerticalTitleBar|
                QDockWidget.DockWidgetClosable|
                QDockWidget.DockWidgetMovable
            )
            self.win.sc_dock.setFeatures(
                QDockWidget.DockWidgetVerticalTitleBar|
                QDockWidget.DockWidgetClosable|
                QDockWidget.DockWidgetMovable
            )
        else:
            self.win.fav_dock.setFeatures(
                QDockWidget.DockWidgetClosable|
                QDockWidget.DockWidgetMovable
            )
            self.win.sc_dock.setFeatures(
                QDockWidget.DockWidgetClosable|
                QDockWidget.DockWidgetMovable
            )
    
    @Slot()
    def show_config(self):
        from libs.config_dlg import ConfDlg        
        conf_vars = {
            "lang": self.win.yaml_vars["lang"],
            "searchOnKey": self.win.yaml_vars["searchOnKey"],
            "searchOpt": self.win.yaml_vars["searchOpt"],
            "theme": self.win.yaml_vars["theme"],
            "splashAnim": self.win.yaml_vars["splashAnim"],
            "verticalTitle": self.win.yaml_vars["verticalTitle"],
            "singleTab": self.win.yaml_vars["singleTab"],
            "tabCount": self.win.yaml_vars["tabCount"]
        }
        config = ConfDlg(self.win, conf_vars)
        config.saveResult.connect(self.conf_accept)
        config.exec()

    @Slot(dict)
    def conf_accept(self, data):
        changes, change_lang, change_theme = False, False, False
        change_lang = data["lang"] != self.win.yaml_vars["lang"]
        change_theme = data["theme"] != self.win.yaml_vars["theme"]
        
        for key in data.keys():
            if data[key] != self.win.yaml_vars[key]:                
                changes = True
                self.win.yaml_vars[key] = data[key]

        if changes:
            if change_lang:
                self.win.reload_translations(False)
            if change_theme:
                self.win.set_theme()
            self.win.update_yaml_file()
            self.win.sc_dock.init_search_by_option()
            self.init_menu_checkeable()

    @Slot()
    def select_lang(self):
        if self.sender() == self.m_spanish:
            if self.m_spanish.isChecked():
                self.win.yaml_vars["lang"] = "es"
                self.m_english.setChecked(False)
                self.win.reload_translations()
            else:
                self.m_spanish.setChecked(True)
        if self.sender() == self.m_english:
            if self.m_english.isChecked():
                self.win.yaml_vars["lang"] = "en"
                self.m_spanish.setChecked(False)
                self.win.reload_translations()
            else:
                self.m_english.setChecked(True)

    @Slot(bool)
    def select_key_on(self, checked):
        self.win.yaml_vars["searchOnKey"] = int(checked)
        self.win.update_yaml_file()
    
    @Slot()
    def select_theme(self, opt):
        theme_ = None
        if self.sender() == self.m_default:
            if self.m_default.isChecked():
                theme_ = 1
            else:
                self.m_default.setChecked(True)
        if self.sender() == self.m_dark:
            if self.m_dark.isChecked():
                theme_ = 2
            else:
                self.m_dark.setChecked(True)
        if self.sender() == self.m_light:
            if self.m_light.isChecked():
                theme_ = 3
            else:
                self.m_light.setChecked(True)
        if self.win.yaml_vars["theme"] != theme_:
            self.win.yaml_vars["theme"] = theme_
            self.win.update_yaml_file()            
            self.win.set_theme()
            self.win.main_widget.update_tab_theme()
            self.init_menu_checkeable()

    @Slot(bool)
    def toggle_splash_anim(self, checked):
        self.win.yaml_vars["splashAnim"] = int(checked)
        self.win.update_yaml_file()

    @Slot()
    def select_searchby(self):
        search_opt = None        
        if self.sender() == self.m_name:
            if self.m_name.isChecked():
                search_opt = 1
            else:
                self.m_name.setChecked(True)
        if self.sender() == self.m_author:
            if self.m_author.isChecked():
                search_opt = 2
            else:
                self.m_author.setChecked(True)
        if self.sender() == self.m_category:
            if self.m_category.isChecked():
                search_opt = 3
            else:
                self.m_category.setChecked(True)
        if self.win.yaml_vars["searchOpt"] != search_opt:
            self.win.yaml_vars["searchOpt"] = search_opt
            self.win.update_yaml_file()
            self.win.sc_dock.init_search_by_option()
            self.init_menu_checkeable()

    @Slot(bool)    
    def set_vertical_title(self, checked):
        self.win.yaml_vars["verticalTitle"] = int(checked)
        self.win.update_yaml_file()
        self.set_dock_features()

    @Slot(bool)
    def set_single_tab(self, checked):
        self.win.yaml_vars['singleTab'] = int(checked)
        self.win.update_yaml_file()
        if self.win.main_widget.tab_view.count() > 2:
            self.win.main_widget.remove_script_tabs()

    @Slot(bool)
    def set_tabcount(self):
        if isinstance(self.sender(), QAction):
            if self.sender().isChecked():
                self.win.yaml_vars["tabCount"] = int(
                    self.sender().text()
                )
                for mcount in self.tabs:
                    if self.sender() != mcount:
                        mcount.setChecked(False)
                self.win.update_yaml_file()
                self.win.main_widget.resize_tab_count()
            else:
                self.sender().setChecked(True)
 
    @Slot()
    def init_author_window(self):
        from libs.about_dlg import AbtDlg
        abt = AbtDlg(self.win)
        abt.exec()

    @Slot()
    def check_database(self):
        try:
            if os.path.exists(self.win.dbm.dbname):                
                thread = QThread()
                iscon = isCon()
                iscon.setUtils(self.win.utils)                
                iscon.moveToThread(thread)
                
                thread.started.connect(iscon.doWork)
                thread.finished.connect(thread.quit)
                iscon.resultReady.connect(self.result_con)
                thread.start()
                thread.exec_()
            else:
                self.init_download_dlg()
        except Exception as e:
            self.win.show_exception(e)

    def result_con(self, result):
        if result:
            if self.win.utils.check_db_update(
                self.win.utils.get_checksum()
            ):
                self.init_download_dlg()
            else:
                QMessageBox.information(
                    self,
                    self.win.i18n.t("setup.database"),
                    self.win.i18n.t("setup.db_is_update"),
                    QMessageBox.StandardButton.Ok
                )
        else:
            QMessageBox.information(
                self,
                self.win.i18n.t("setup.database"),
                self.win.i18n.t("setup.internet_error"),
                QMessageBox.StandardButton.Ok
            )

    def init_download_dlg(self):
        from libs.download_dlg import DownloadDlg
        download_dlg = DownloadDlg(self.win)
        download_dlg.finishDownload.connect(self.database_updated)     

    @Slot()
    def database_updated(self, is_updated, error):
        self.sender().close()
        if is_updated:
            QMessageBox.information(
                self,
                self.win.i18n.t("setup.database"),
                self.win.i18n.t("setup.downloaded"),
                QMessageBox.StandardButton.Ok
            )
            self.win.sc_dock.load_scripts()
        else:
            QMessageBox.information(
                self,
                "Error",
                error,
                QMessageBox.StandardButton.Ok
            )

class isCon(QObject):
    utils = None
    resultReady = Signal(int, name="resultReady")

    def setUtils(self, utils):        
        self.utils = utils

    def doWork(self):                      
        result = self.utils.is_con()        
        self.resultReady.emit(result)