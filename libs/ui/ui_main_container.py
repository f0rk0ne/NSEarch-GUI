from select import select
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QTabBar
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from webenginepage import WebPage

class MainContainer(QWidget):

    win = None
    tab_view = None

    def __init__(self, parent):
        super(MainContainer, self).__init__(parent)
        try:            
            self.win = parent
            self.setupUi()
        except Exception as e:
            parent.show_exception(e)

    def setupUi(self):
        self.setObjectName("main_container")
        self.setMinimumSize(QSize(300, 300))
        main_gridLayout = QGridLayout(self)
        main_gridLayout.setObjectName("main_gridlayout")
        self.tab_view = QTabWidget(self)
        self.tab_view.setObjectName("tab_view")
        self.tab_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_view.setTabsClosable(True)
        self.tab_view.customContextMenuRequested.connect(
            self.show_close
        )
        self.tab_view.tabBarClicked.connect(
            self.select_item
        )
        self.tab_view.tabCloseRequested.connect(
            self.close_script_tab
        )
        main_gridLayout.addWidget(self.tab_view, 0, 0, 1, 1)

    def remove_script_tabs(self):
        for tab in range(0, self.tab_view.count()):            
            self.tab_view.setCurrentIndex(tab)            
            self.tab_view.currentWidget().close()              
        self.tab_view.clear()
        self.create_home_tab()

    def resize_tab_count(self):
        if self.tab_view.count() > int(
            self.win.yaml_vars["tabCount"]
        ):
            startindex = self.tab_view.count() - self.win.yaml_vars["tabCount"]
            for tabindex in range(1,startindex):
                self.tab_view.setCurrentIndex(tabindex)
                self.tab_view.currentWidget().close()
                self.tab_view.setCurrentIndex(tabindex+1)
                self.tab_view.removeTab(tabindex)            

    def update_tab_theme(self):
        try:
            theme_name = self.win.utils.get_theme_name(
                self.win.yaml_vars["theme"]
            )
            if self.tab_view.count() >= 0:
                for tab in range(self.tab_view.count()):
                    self.tab_view.setCurrentIndex(tab)                    
                    self.tab_view.currentWidget().page().runJavaScript(
                        "setTheme('"+theme_name+"');"
                    )
        except Exception as e:
            self.win.show_exception(e)

    def get_web_view(self):
        web_view = QWebEngineView(self)
        web_view.setContextMenuPolicy(Qt.NoContextMenu)
        web_view.adjustSize()
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        web_view.setSizePolicy(sizePolicy)
        web_page = WebPage(self)
        web_page.setSettings()
        web_view.setPage(web_page)
        return web_view
    
    def create_home_tab(self):
        self.win.utils.print(self.win.welcome,True)
        html = self.win.utils.get_home_html(
            **self.get_home_info()
        )
        
        home_view = self.get_web_view()
        home_view.setHtml(html, QUrl("file:///"))

        self.tab_view.addTab(
            home_view,
            QIcon(
                f'{self.win.resources_path}nmap-logo-small.png'
            ),
            self.win.i18n.t("gui.home")
        )         
        self.tab_view.setCurrentIndex(0)
        self.tab_view.tabBar().setTabButton(
            0,
            QTabBar.RightSide,
            None
        )

    def get_home_info(self):
        return {
            "title": self.win.i18n.t("gui.app_title"),
            "path": self.win.path,
            "description": self.win.i18n.t("gui.app_description"),
            "version": self.win.i18n.t("gui.app_version"),
            "theme": self.win.utils.get_theme_name(
                        self.win.yaml_vars["theme"]
            ),
            "show_anim": self.win.yaml_vars["splashAnim"]
        }

    def create_script_tab(self, script):
        if not self.script_is_open(script):            
            html = self.win.utils.get_script_html(
                self.win.utils.get_theme_name(
                        self.win.yaml_vars["theme"]
                ),
                **self.win.dbm.get_script_by_name(
                    script
                )
            )
            if (self.win.yaml_vars["singleTab"] and
            self.tab_view.count() > 1):
                self.tab_view.setCurrentIndex(1)
                self.tab_view.setTabText(1, script)
                web_view = self.tab_view.currentWidget()
                web_view.page().setHtml(html)
            elif self.tab_view.count() <= self.win.yaml_vars["tabCount"]:
                script_view = self.get_web_view()
                script_view.setHtml(html)
                self.tab_view.addTab(
                    script_view,
                    QIcon(f'{self.win.resources_path}nmap-logo-small.png'),
                    script
                )
                self.tab_view.setCurrentIndex(self.tab_view.count()- 1)
            else:
                tab_index = self.tab_view.count()-1
                self.tab_view.setCurrentIndex(tab_index)
                self.tab_view.setTabText(tab_index, script)
                self.tab_view.currentWidget().page().setHtml(html)

    def script_is_open(self, script):
        tab_index = None
        is_open = False
        for t_index in range(1, self.tab_view.count()):            
            if script == self.tab_view.tabText(t_index):
                is_open = True
                tab_index = t_index
                pass
        if is_open:
            self.tab_view.setCurrentIndex(
                tab_index if tab_index != None else 1
            )
        return is_open

    @Slot()
    def select_item(self, index):
        if index != 0 and index != -1:
            script = self.tab_view.tabText(index)
            self.win.sc_dock.select_tab_script(script)
            self.win.fav_dock.select_tab_fav(script)

    @Slot(int)
    def show_close(self, pos):
        if self.tab_view.count() > 1:
            close_menu = QMenu(self.win)
            close_tab = QAction(
                QIcon(
                    f"{self.win.resources_path}close.png"
                ),
                self.win.i18n.t("gui.close_tab")
            )
            close_all = QAction(
                QIcon(
                    f"{self.win.resources_path}closeall.png"
                ),
                self.win.i18n.t("gui.close_all_tabs")
            )
            close_menu.addAction(close_tab)
            close_menu.addSeparator()
            close_menu.addAction(close_all)
            menu_clicked = close_menu.exec_(
                self.tab_view.mapToGlobal(pos)
            )
            if (close_tab == menu_clicked and
            self.tab_view.currentIndex() != 0):
                self.tab_view.currentWidget().close()
                self.tab_view.removeTab(self.tab_view.currentIndex())
            if close_all == menu_clicked:
                self.remove_script_tabs()

    @Slot()
    def close_script_tab(self, index):
        self.tab_view.currentWidget().close()
        self.tab_view.removeTab(index)
