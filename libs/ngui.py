#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QLocale
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QApplication
from traceback import print_exc
import splash
import dbmodule
import utils
import os
import time
import sys
sys.path.append("../libs")

try:
    form, base = uic.loadUiType("ui/mainwindow.ui")
except Exception as e:
    print_exc() & exit(0)


class NGui(base, form):

    path = f"/{os.path.abspath(sys.argv[0])[1:-len('nsearch.py')]}"
    scripts_list = dict()
    fav_list, author_list, theme = dict(), dict(), 0
    search_opt, search_onkey, lang = 0, 0, ""
    last_scr_search, last_fav_search = "", ""
    last_scr_result, last_fav_result = "", ""
    total_scripts, scripts_found = 0, 0
    search_opt_cp, show_anim = 0, 0
    resources_path = f'{path}resources/'
    css_files = ['default', 'dark', 'light']
    script_text, gui_dock_fav = "  Script", "gui.dock_favorites"
    gui_script_cat = "gui.scripts_category"
    gui_script_not = "gui.script_not_found"
    gui_scripts_found = "gui.scripts_found"
    status_left, status_right = None, None
    m_name, m_author, m_category = None, None, None
    s_name, s_author, s_category = None, None, None
    fav_treeview, scr_treeview = None, None
    splash, progressbar, script_validator = None, None, None
    search_text, search_btn, clear_btn = None, None, None
    fsearch_text, fsearch_btn = None, None
    fclear_btn, style_path = None, f"{resources_path}qcss/"    
    conf_vars_updated = False
    window_icon = None
    author_txt = ""
    welcome = ""
    tooltip = None
    utils = None

    def __init__(self):
        super(base, self).__init__()
        self.conf_vars_updated = self.load_yaml_vars()
        self.utils = utils.Utils()
        self.setupUi(self)
        self.init_UI()

    # init gui params and controls
    def init_UI(self):
        try:
            self.load_language()
            settings = QSettings()            
            if "windowstate" in settings.childKeys():
                self.restoreState(settings.value("windowstate"))
            if "geometry" in settings.childKeys():
                self.restoreGeometry(settings.value("geometry"))
            else:
                fg = self.frameGeometry()
                ct = QDesktopWidget().availableGeometry().center()
                fg.moveCenter(ct)
                self.move(fg.topLeft())
            self.init_splash()
            self.search_text.setFocus()
        except Exception as e:
            self.show_exception(e)
            exit()

    # init splash
    def init_splash(self):
        splash_img = self.resources_path
        splash_img += self.utils.get_splash_img(self.show_anim)
        self.splash = splash.NSplash(splash_img, Qt.WindowStaysOnTopHint)
        self.progressbar = QProgressBar(self.splash)
        self.progressbar.setMaximum(92)
        self.progressbar.setGeometry(
            25, self.splash.height() - 60,
            self.splash.width()-50, 20
        )
        if self.show_anim:
            self.splash.processFrame.connect(self.show_splash_messages)
            self.splash.show()
        else:
            self.splash.show()
            for a in range(0, 91, 18):
                self.show_splash_messages(a)
                time.sleep(.5)
        QApplication.processEvents()

    # show splash messages
    def show_splash_messages(self, counter):
        if counter == 18:
            self.splash.showMessage(
                dbmodule.i18n.t("gui.splash_conf_vars"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            if self.conf_vars_updated:
                self.splash.showMessage(
                    dbmodule.i18n.t("gui.splash_upd_conf_file"),
                    Qt.AlignHCenter | Qt.AlignBottom,
                    Qt.black
                )
        elif counter == 36:
            self.total_scripts = dbmodule.get_total_scripts()
            self.scripts_found = self.total_scripts
            self.scripts_list = dbmodule.get_data()
            self.author_list = dbmodule.get_author_data()
            self.splash.showMessage(
                dbmodule.i18n.t("gui.splash_script_data"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            self.load_text_translations()
        elif counter == 54:
            self.splash.showMessage(
                dbmodule.i18n.t("gui.splash_load_font"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            font_family = "ArchitectsDaughter-Regular.ttf"
            font_name = f"{self.resources_path}{font_family}"
            if not os.path.exists(font_name):
                QMessageBox.information(
                    self,
                    "Font",
                    dbmodule.i18n.t("gui.splash_font_not_found"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
                exit()
            if QFontDatabase.addApplicationFont(font_name) == -1:
                QMessageBox.information(
                    self,
                    "Font",
                    dbmodule.i18n.t("gui.splash_font_error"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
        elif counter == 72:
            self.splash.showMessage(
                dbmodule.i18n.t("gui.splash_init_gui"),
                Qt.AlignHCenter | Qt.AlignBottom,
                Qt.black
            )
            self.progressbar.setValue(counter)
        elif counter == 90:
            self.progressbar.close()
            self.splash.finish(self)
            self.show()
            self.set_theme()
            self.init_menu(True)
            return False
        self.progressbar.setValue(counter)

    # load i18n language
    def load_language(self, load_text=False):
        if len(dbmodule.i18n.get("load_path")) == 0:
            dbmodule.i18n.load_path.append("i18n")
        dbmodule.i18n.set("locale", self.lang)
        dbmodule.i18n.set("fallback", "en" if self.lang == "es" else "es")
        self.load_translations()
        if load_text:
            self.load_text_translations()

    # load gui translations
    def load_translations(self):
        self.welcome = dbmodule.i18n.t(
            "gui.welcome", user=os.getenv("USER")
        )
        self.load_menu_translastions()
        self.load_scripts_text()
        self.load_favorites_text()        

    # load menu text
    def load_menu_translastions(self):
        self.author_txt = dbmodule.i18n.t("gui.act_author")
        self.menu_app.setTitle(dbmodule.i18n.t("gui.menu_app"))
        self.m_configuration.setText(dbmodule.i18n.t("gui.act_configuration"))
        self.m_quit.setText(dbmodule.i18n.t("gui.act_quit"))
        self.menu_options.setTitle(dbmodule.i18n.t("gui.menu_options"))
        self.menu_language.setTitle(dbmodule.i18n.t("gui.menu_language"))
        self.m_spanish.setText(dbmodule.i18n.t("gui.act_spanish"))
        self.m_english.setText(dbmodule.i18n.t("gui.act_english"))
        self.menu_theme.setTitle(dbmodule.i18n.t("gui.menu_theme"))
        self.m_default.setText(dbmodule.i18n.t("gui.act_default"))
        self.m_dark.setText(dbmodule.i18n.t("gui.act_dark"))
        self.m_light.setText(dbmodule.i18n.t("gui.act_light"))
        self.m_searchkey.setText(dbmodule.i18n.t("gui.act_search_on_key"))
        self.menu_search_opts.setTitle(dbmodule.i18n.t("gui.menu_search_opts"))
        self.m_name.setText(dbmodule.i18n.t("gui.act_name"))
        self.m_author.setText(self.author_txt)
        self.m_category.setText(dbmodule.i18n.t("gui.act_category"))
        self.menu_windows.setTitle(dbmodule.i18n.t("gui.menu_windows"))
        self.m_scriptdock.setText(dbmodule.i18n.t("gui.act_scripts"))
        self.m_favoritedock.setText(dbmodule.i18n.t("gui.act_favorite"))
        self.menu_about.setTitle(dbmodule.i18n.t("gui.menu_about"))
        self.m_about.setText(dbmodule.i18n.t("gui.act_developer"))
        self.m_about_qt.setText(dbmodule.i18n.t("gui.act_about_qt"))
        self.load_menu_data()

    # set menu info data
    def load_menu_data(self):
        self.m_configuration.setStatusTip(
            dbmodule.i18n.t("gui.st_configuration"))
        self.m_quit.setStatusTip(dbmodule.i18n.t("gui.st_quit"))
        self.m_spanish.setStatusTip(dbmodule.i18n.t("gui.st_spanish"))
        self.m_english.setStatusTip(dbmodule.i18n.t("gui.st_english"))
        self.m_default.setStatusTip(dbmodule.i18n.t("gui.st_default"))
        self.m_dark.setStatusTip(dbmodule.i18n.t("gui.st_dark"))
        self.m_light.setStatusTip(dbmodule.i18n.t("gui.st_light"))
        self.m_searchkey.setStatusTip(dbmodule.i18n.t("gui.st_search_on"))
        self.m_name.setStatusTip(dbmodule.i18n.t("gui.st_name"))
        self.m_author.setStatusTip(dbmodule.i18n.t("gui.st_author"))
        self.m_category.setStatusTip(dbmodule.i18n.t("gui.st_category"))
        self.m_scriptdock.setStatusTip(dbmodule.i18n.t("gui.st_scripts"))
        self.m_favoritedock.setStatusTip(dbmodule.i18n.t("gui.st_favorite"))
        self.m_about.setStatusTip(dbmodule.i18n.t("gui.st_developer"))
        self.m_about_qt.setStatusTip(dbmodule.i18n.t("gui.st_about_qt"))
        self.m_splash.setStatusTip(dbmodule.i18n.t("gui.st_anim"))
        self.main_container.setStatusTip(self.welcome)

    # set scripts dockwidget translations
    def load_scripts_text(self):
        self.scriptdock.setWindowTitle(
            dbmodule.i18n.t("gui.dock_scripts")
        )
        self.search_text.setPlaceholderText(
            dbmodule.i18n.t( "gui.search_placeholder" )
        )
        self.search_text.setStatusTip(
            dbmodule.i18n.t("gui.st_search")
        )
        self.search_btn.setStatusTip(
            dbmodule.i18n.t("gui.st_search_scripts")
        )
        self.clear_btn.setStatusTip(
            dbmodule.i18n.t("gui.st_clear_script_search")
        )
        self.s_name.setText(dbmodule.i18n.t("gui.act_name"))
        self.s_name.setStatusTip(dbmodule.i18n.t("gui.st_name"))
        self.s_author.setText(self.author_txt)
        self.s_author.setStatusTip(dbmodule.i18n.t("gui.st_author"))
        self.s_category.setText(dbmodule.i18n.t("gui.act_category"))
        self.s_category.setStatusTip(dbmodule.i18n.t("gui.st_category"))        

# set favorites dockwidget translations
    def load_favorites_text(self):
        self.favoritedock.setWindowTitle(dbmodule.i18n.t(self.gui_dock_fav))
        self.fsearch_text.setPlaceholderText(
            dbmodule.i18n.t(
                "gui.search_placeholder"
            )
        )
        self.fsearch_text.setStatusTip(dbmodule.i18n.t("gui.st_search"))
        self.fsearch_btn.setStatusTip(
            dbmodule.i18n.t("gui.st_search_favorite"))
        self.fclear_btn.setStatusTip(
            dbmodule.i18n.t("gui.st_clear_fav_search"))

    # load language translations
    def load_text_translations(self):
        self.total_text = dbmodule.i18n.t(
            "gui.total_scripts",
            total=self.total_scripts
        )
        self.utils.print(self.welcome)
        self.total_fav_text = dbmodule.i18n.t(
            "gui.total_favorites",
            total=len(self.fav_list)
        )
        if self.status_right != None:
            self.status_right.setText(self.total_text)
        if self.status_left != None:
            self.status_left.setText(self.welcome)

    # load theme
    def set_theme(self):
        try:
            theme_file = f"{self.style_path}{self.css_files[self.theme-1]}.css"
            app.setStyleSheet("")
            if os.path.exists(theme_file):
                css_file = open(theme_file, 'r')
                css_content = css_file.read().replace(
                    '\n', ''
                ).replace('{file}', self.resources_path)
                app.setStyleSheet(css_content)
                css_file.close()
            self.load_icons()
            app.style().unpolish(self)
            app.style().polish(self)
        except Exception as e:
            self.utils.print_traceback(e)

    # load window icons
    def load_icons(self):
        icon_path = f"{self.resources_path}{self.css_files[self.theme-1]}/"
        self.window_icon = f"{self.resources_path}nmap-logo-small.png"
        self.setWindowIcon(
            QIcon(
                self.window_icon
            )
        )
        self.m_configuration.setIcon(
            QIcon(f"{icon_path}config.png")
        )
        self.m_quit.setIcon(
            QIcon(f"{icon_path}exit.png"))
        self.m_about.setIcon(
            QIcon(f"{icon_path}people.png")
        )
        self.m_about_qt.setIcon(
            QIcon(f"{icon_path}qt.png")
        )
        self.menu_language.setIcon(
            QIcon(f"{icon_path}lang.png")
        )
        self.menu_theme.setIcon(
            QIcon(f"{icon_path}theme.png")
        )
        self.menu_search_opts.setIcon(
            QIcon(f"{icon_path}searchopt.png")
        )
        self.search_btn.setIcon(
            QIcon(f"{self.resources_path}glass.png")
        )
        self.clear_btn.setIcon(
            QIcon(f"{self.resources_path}brush.png")
        )
        self.fsearch_btn.setIcon(
            QIcon(f"{self.resources_path}glass.png")
        )
        self.fclear_btn.setIcon(
            QIcon(f"{self.resources_path}brush.png")
        )

    # load config file vars
    def load_yaml_vars(self):
        to_update = False
        if 'lang' not in dbmodule.item['config'].keys():
            self.lang = QLocale.system().name()
            to_update = True
        else:
            self.lang = dbmodule.item['config']['lang']
        if 'searchOpt' in dbmodule.item['config'].keys():
            self.search_opt = dbmodule.item['config']['searchOpt']
            self.search_opt_cp = self.search_opt
        else:
            self.search_opt = 1
            self.search_opt_cp = self.search_opt
            to_update = True
        if 'searchOnKey' in dbmodule.item['config'].keys():
            self.search_onkey = dbmodule.item['config']['searchOnKey']
        else:
            self.search_onkey = 1
            to_update = True
        if 'theme' in dbmodule.item['config'].keys():
            self.theme = dbmodule.item['config']['theme']
        else:
            self.theme = 1
            to_update = True
        if 'splashAnim' in dbmodule.item['config'].keys():
            self.show_anim = dbmodule.item['config']['splashAnim']
        else:
            self.show_anim = 1
            to_update = True
        if to_update:
            self.update_yaml_file()
            return True
        else:
            return False

    # update config file vars
    def update_yaml_file(self):
        self.utils.create_config_file(
            self.search_onkey, self.search_opt,
            self.theme, self.show_anim, self.lang
        )        

    # init menubar items
    def init_menu(self, init_gui=False):
        self.m_spanish.setChecked(self.lang == 'es')
        self.m_english.setChecked(self.lang == 'en')
        self.m_searchkey.setChecked(self.search_onkey)
        self.m_default.setChecked(self.theme == 1)
        self.m_dark.setChecked(self.theme == 2)
        self.m_light.setChecked(self.theme == 3)
        self.m_name.setChecked(self.search_opt == 1)
        self.m_author.setChecked(self.search_opt == 2)
        self.m_category.setChecked(self.search_opt == 3)
        self.s_name.setChecked(self.search_opt == 1)
        self.s_author.setChecked(self.search_opt == 2)
        self.s_category.setChecked(self.search_opt == 3)
        self.m_splash.setChecked(self.show_anim)
        if init_gui:
            self.menuBar().setStyleSheet("font-family:ArchitectsDaughter;")
            self.init_GUI()

    # init gui components
    def init_GUI(self):
        self.status_left = QLabel(self.welcome)
        self.status_right = QLabel(self.total_text)
        self.status_left.setAlignment(Qt.AlignLeft)
        self.status_right.setAlignment(Qt.AlignRight)
        self.statusBar().setContentsMargins(10, 3, 10, 3)
        self.statusBar().addWidget(self.status_left)
        self.statusBar().addPermanentWidget(self.status_right)
        self.scr_treeview.setModel(QStandardItemModel(0, 1, self))
        self.load_scripts_options()
        self.load_favorites_options()
        self.fav_treeview.selectionModel().currentChanged.connect(
            self.favorite_selected
        )
        self.scr_treeview.selectionModel().currentChanged.connect(
            self.script_selected
        )
        self.s_name.clicked.connect(lambda: self.set_search_opt(1))
        self.s_author.clicked.connect(lambda: self.set_search_opt(2))
        self.s_category.clicked.connect(lambda: self.set_search_opt(3))
        self.create_home_tab()

    # create search script controls
    def load_scripts_options(self):
        self.script_validator = QRegExpValidator()
        self.script_validator.setRegExp(self.get_regexp())
        self.search_text.setValidator(self.script_validator)
        self.load_scripts()

    # create favorites search controls
    def load_favorites_options(self):
        self.fsearch_text.setValidator(
            QRegExpValidator(QRegExp("[A-Za-z0-9\-]{0,100}")))
        self.fav_treeview.sortByColumn(0, Qt.AscendingOrder)
        self.load_favorites_data()
        self.load_favorites()

    # return regular expressions
    def get_regexp(self):
        if self.search_opt == 1:
            return QRegExp("[A-Za-z0-9\-]{0,100}")
        elif self.search_opt == 2:
            return QRegExp("[A-Za-z0-9\s]{0,100}")
        elif self.search_opt == 3:
            return QRegExp("[A-Za-z0-9]{0,100}")

    # remove all scripts tabs
    def remove_script_tabs(self):
        self.tab_view.clear()
        self.create_home_tab()

    # load favorites data in dict
    def load_favorites_data(self):
        self.fav_list = dbmodule.get_favorites()
        tmp = {}
        for index in self.fav_list:
            fav = self.fav_list[index]
            tmp[str(fav["name"])] = fav["ranking"]
        self.fav_list = tmp

    # load favorites data in treeview
    def load_favorites(self):
        fmodel = self.fav_treeview.model()
        if fmodel == None:
            fmodel = QStandardItemModel(0, 1, self)
        else:
            fmodel.clear()
        if len(self.fav_list) > 0:
            for name in sorted(self.fav_list.keys()):
                fav = QStandardItem(name)
                if name in self.author_list.keys():
                    fav.setData(
                        dbmodule.i18n.t(
                            "gui.fav_info",
                            script=name,
                            author=self.author_list[name]
                        ), Qt.StatusTipRole)
                fav.setEditable(False)
                fav.setSizeHint(QSize(160, 25))
                fav_icon = QStandardItem(
                    self.get_favorite_img(
                        self.fav_list[name]
                    ),
                    dbmodule.get_ranking_text(
                        self.fav_list[name]
                    )
                )
                fav_icon.setSizeHint(QSize(60, 25))
                fmodel.appendRow([fav, fav_icon])
                fmodel.setHorizontalHeaderLabels([self.script_text, "Ranking"])
        else:
            fmodel.setHorizontalHeaderLabels([self.script_text, "Ranking"])
        self.fav_treeview.setModel(fmodel)
        self.fav_treeview.setColumnWidth(0, 160)
        self.fav_treeview.setColumnWidth(1, 60)

    # get favorite image
    def get_favorite_img(self, ranking):
        if ranking == 0:
            return QIcon(f"{self.resources_path}normal.png")
        if ranking == 1:
            return QIcon(f"{self.resources_path}great.png")
        if ranking == 2:
            return QIcon(f"{self.resources_path}super-great.png")

    # load scripts data in treeview
    def load_scripts(self):
        model = self.scr_treeview.model()
        model.clear()
        for cat_key in sorted(self.scripts_list):
            category = QStandardItem(cat_key)
            category.setData(
                dbmodule.i18n.t(
                    self.gui_script_cat,
                    count=len(self.scripts_list[cat_key]),
                    category=cat_key
                ),
                Qt.StatusTipRole
            )
            category.setEditable(False)
            category.setSelectable(False)
            for name in sorted(self.scripts_list[cat_key]):
                script = QStandardItem(name)
                script.setData(
                    f"{self.author_txt}: {self.author_list[name]}",
                    Qt.StatusTipRole
                )
                script.setEditable(False)
                category.appendRow(script)
            model.appendRow(category)
        model.setHorizontalHeaderLabels(
            [f"  {dbmodule.i18n.t('gui.categories')}"]
        )

    # Show dialog with configuration values
    def show_config(self):
        from libs.config_dlg import ConfDlg
        config = ConfDlg(self)
        config.initControls(
            (self.lang, self.search_onkey,
            self.search_opt, self.theme, self.show_anim),
            self.window_icon
        )
        config.saveResult.connect(self.conf_accept)
        config.exec_()

    # save configuration values
    def conf_accept(self, data):
        lang_, search_onkey_, search_opt_, theme_, show_anim_ = data
        update_conf = False
        if self.lang != lang_:
            self.lang = lang_
            self.reload_translations()
            update_conf = True
        if self.search_onkey != search_onkey_:
            self.search_onkey = int(search_onkey_)
            self.m_searchkey.setChecked(self.search_onkey)
            update_conf = True
        if self.search_opt != search_opt_:
            self.search_opt = search_opt_
            self.init_menu()
            update_conf = True
        if self.theme != theme_:
            self.theme = int(theme_)
            self.set_theme()
            self.init_menu()
            update_conf = True
        if self.show_anim != show_anim_:
            self.show_anim = int(show_anim_)
            self.init_menu()
            update_conf = True
        if update_conf:
            self.update_yaml_file()
            self.script_validator.setRegExp(self.get_regexp())

    # set focus in qlinedit on tab selected
    def favorites_tab_selected(self):
        current_index = self.sender().tabText(self.sender().currentIndex())
        if dbmodule.i18n.t(self.gui_dock_fav) == current_index:
            self.fsearch_text.setFocus()
            self.status_right.setText(self.total_fav_text)
            if self.last_fav_result != "":
                self.status_left.setText(self.last_fav_result)
            else:
                self.status_left.setText(self.welcome)
        elif dbmodule.i18n.t(self.gui_script_cat) == current_index:
            self.search_text.setFocus()
            self.status_right.setText(self.total_text)
            if self.last_scr_result != "":
                self.status_left.setText(self.last_scr_result)
            else:
                self.status_left.setText(self.welcome)

    # show contextmenu with close tab actions
    def show_close(self, pos):
        if self.tab_view.count() > 1:
            close_menu = QMenu()
            close_tab = QAction(
                QIcon(
                    f"{self.resources_path}close.png"
                ),
                dbmodule.i18n.t("gui.close_tab")
            )
            close_all = QAction(
                QIcon(
                    f"{self.resources_path}closeall.png"
                ),
                dbmodule.i18n.t("gui.close_all_tabs")
            )
            close_menu.addAction(close_tab)
            close_menu.addSeparator()
            close_menu.addAction(close_all)
            menu_clicked = close_menu.exec_(self.tab_view.mapToGlobal(pos))
            if close_tab == menu_clicked and self.tab_view.currentIndex() != 0:
                self.tab_view.removeTab(self.tab_view.currentIndex())
            if close_all == menu_clicked:
                self.remove_script_tabs()

    # select script or favorite item when tabbar clicked
    def select_item(self, index):
        if index != 0 and index != -1:
            script = self.tab_view.tabText(index)
            self.select_tab_script(script)
            self.select_tab_fav(script)

    # select script tab when script item clicked
    def select_tab_script(self, script):
        for t_index in range(0, self.scr_treeview.model().rowCount()):
            scr_item = self.scr_treeview.model().item(t_index, 0)
            if scr_item != None and scr_item.hasChildren():
                for c_index in range(0, scr_item.rowCount()):
                    chl_item = scr_item.child(c_index, 0)
                    if script in chl_item.text():
                        self.scr_treeview.setCurrentIndex(chl_item.index())
                        break

    # select script tab when favorite item clicked
    def select_tab_fav(self, script):
        for f_index in range(0, self.fav_treeview.model().rowCount()):
            fav_item = self.fav_treeview.model().item(f_index, 0)
            if script in fav_item.text():
                self.fav_treeview.setCurrentIndex(fav_item.index())
                break

    # show script data when a favorite is selected
    def favorite_selected(self, current, previous):
        if self.fav_treeview.model().rowCount() > 1:
            script = self.fav_treeview.model().itemFromIndex(current).text()\
                if current.column() == 0 else\
                self.fav_treeview.model().item(current.row(), 0).text()
            if script in self.fav_list.keys():
                self.create_script_tab(script)

    # show script data when a script is selected
    def script_selected(self, current, previous):
        script = self.scr_treeview.model().itemFromIndex(current)
        if script.parent() != None:
            self.create_script_tab(script.text())

    # create home tab
    def create_home_tab(self):
        home_view = self.get_web_view()
        title = dbmodule.i18n.t("gui.app_title")
        description = dbmodule.i18n.t("gui.app_description")
        version = dbmodule.i18n.t("gui.app_version")
        home_view.setHtml(
            self.utils.get_home_html(
                title,
                self.path,
                description, version,
                self.utils.get_theme_name(
                    self.theme
                ),
                self.show_anim
            )
        )
        self.tab_view.addTab(
            home_view,
            QIcon(
                f'{self.resources_path}nmap-logo-small.png'
            ),
            dbmodule.i18n.t("gui.home")
        )
        self.tab_view.setCurrentIndex(0)
        self.tab_view.tabBar().setTabButton(0, QTabBar.RightSide, None)

    # create script tab view
    def create_script_tab(self, script):
        tab_index = None
        is_open = False
        for index in range(0, self.tab_view.count()):
            t_index = self.tab_view.count() - index
            if script == self.tab_view.tabText(t_index):
                is_open = True
                tab_index = t_index
        if is_open:
            self.tab_view.setCurrentIndex(
                tab_index if tab_index != None else 1
            )
        else:
            script_path = f"{dbmodule.scripts_path}{script}.nse"
            if not os.path.exists(script_path):
                QMessageBox.information(
                    self,
                    "Error",
                    dbmodule.i18n.t(self.gui_script_not),
                    QMessageBox.Ok
                )
                return False
            description, usage, author, script_license,\
                categories = self.utils.get_script_data(
                    script_path
                )
            script_license = script_license.replace(
                "https://nmap.org/book/man-legal.html",
                "<a href='https://nmap.org/book/man-legal.html'\
                title='Nmap License'>\
                https://nmap.org/book/man-legal.html\
                </a>"
            )
            description = "".join([
                f"<p>{a}</p>"
                for a in description.splitlines()
            ])
            usage = "".join([
                f"<p>{b}</p>"
                for b in usage.splitlines()
                if b != "" and (
                    b.startswith("--")
                    or b.startswith("---")
                )
            ])
            if usage != "":
                usage = self.utils.get_script_usage(usage)
            script_view = self.get_web_view()
            script_view.setHtml(
                self.utils.get_script_html
                (
                    script, author,
                    script_license, categories,
                    description, usage,
                    self.utils.get_theme_name(self.theme)
                )
            )
            self.tab_view.addTab(
                script_view,
                QIcon(f'{self.resources_path}nmap-logo-small.png'),
                script
            )
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            script_view.page().linkClicked.connect(
                self.open_license_link
            )

    # get webview instance
    def get_web_view(self):
        web_view = QWebView()
        web_view.setContextMenuPolicy(Qt.NoContextMenu)
        web_view.page().setLinkDelegationPolicy(
            QWebPage.DelegateAllLinks
        )
        web_view.page().settings().setAttribute(
            QWebSettings.JavascriptEnabled,
            False
        )
        web_view.page().settings().setAttribute(
            QWebSettings.JavaEnabled,
            False
        )
        web_view.page().settings().setAttribute(
            QWebSettings.PrivateBrowsingEnabled,
            True
        )
        web_view.page().settings().setAttribute(
            QWebSettings.XSSAuditingEnabled,
            True
        )
        web_view.page().settings().setAttribute(
            QWebSettings.LocalContentCanAccessFileUrls,
            False
        )
        web_view.page().settings().setAttribute(
            QWebSettings.LocalContentCanAccessRemoteUrls,
            False
        )
        web_view.page().settings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled,
            False
        )
        return web_view

    # open license link in browser
    def open_license_link(self, url):
        if not url.isEmpty() and url.url() ==\
                "https://nmap.org/book/man-legal.html":
            QDesktopServices.openUrl(url)

    # remove script tab
    def close_script_tab(self, index):
        self.tab_view.removeTab(index)

    # search scripts when a key is pressed
    def search_key_pressed(self):
        if self.search_onkey:
            self.search()

    # search scripts when enter key is pressed
    def search_enter_pressed(self):
        self.search()

    # search scripts when search button is pressed
    def init_search(self):
        self.search()

    # search scripts
    def search(self):
        pattern = str(self.search_text.text()).lower()
        if len(pattern) >= 2 and self.last_scr_search != pattern:
            if self.search_opt == 1:
                self.show_search_results(
                    self.get_search_results(pattern)
                )
            elif self.search_opt == 2:
                self.show_author_results(
                    self.get_author_results(pattern)
                )
            elif self.search_opt == 3:
                self.show_category_results(
                    self.get_category_results(pattern)
                )
        else:
            self.reset_search_results(pattern)

    # get search by name results
    def get_search_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self.scripts_found = 0
        for key in self.scripts_list.keys():
            for name in self.scripts_list[key]:
                if pattern in name:
                    if key in results.keys():
                        results[key].append(name)
                    else:
                        tmp = []
                        tmp.append(name)
                        results[key] = tmp
        if len(results) == 0:
            self.search_not_found()
            return False
        return results

    # show search by name results
    def show_search_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in sorted(results.keys()):
                category = QStandardItem(cat_key)
                category.setData(
                    dbmodule.i18n.t(
                        self.gui_script_cat,
                        count=len(results[cat_key]),
                        category=cat_key
                    ), Qt.StatusTipRole
                )
                category.setEditable(False)
                category.setSelectable(False)
                for name in sorted(results[cat_key]):
                    self.scripts_found += 1
                    script = QStandardItem(name)
                    script.setData(
                        self.author_txt +
                        f": {self.author_list[name]}",
                        Qt.StatusTipRole
                    )
                    script.setEditable(False)
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {dbmodule.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = dbmodule.i18n.t(
                self.gui_scripts_found, count=self.scripts_found)
            self.status_left.setText(self.last_scr_result)

    # get search by author results
    def get_author_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self. scripts_found = 0
        for key in sorted(self.scripts_list):
            for script in self.scripts_list[key]:
                if pattern.lower() in self.author_list[script].lower():
                    if key in results.keys():
                        results[key].append(script)
                    else:
                        tmp = []
                        tmp.append(script)
                        results[key] = tmp
        if len(results) == 0:
            self.search_not_found()
            return False
        return results

    # show search by author results
    def show_author_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in sorted(results.keys()):
                category = QStandardItem(cat_key)
                category.setData(
                    dbmodule.i18n.t(
                        self.gui_script_cat,
                        count=len(results[cat_key]),
                        category=cat_key
                    ),
                    Qt.StatusTipRole
                )
                category.setEditable(False)
                category.setSelectable(False)
                for name in sorted(results[cat_key]):
                    self.scripts_found += 1
                    script = QStandardItem(name)
                    script.setEditable(False)
                    script.setData(
                        f"{self.author_txt}: {self.author_list[name]}",
                        Qt.StatusTipRole
                    )
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {dbmodule.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = dbmodule.i18n.t(
                self.gui_scripts_found,
                count=self.scripts_found
            )
            self.status_left.setText(self.last_scr_result)

    # get search by content results
    def get_category_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self.scripts_found = 0
        for key in self.scripts_list.keys():
            if pattern.lower() in key:
                results[key] = self.scripts_list[key]
        if len(results) == 0:
            self.search_not_found()
            return False
        return results

    # show search by content results
    def show_category_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in results.keys():
                category = QStandardItem(cat_key)
                category.setData(
                    dbmodule.i18n.t(
                        self.gui_script_cat,
                        count=len(self.scripts_list[cat_key]),
                        category=cat_key
                    ),
                    Qt.StatusTipRole
                )
                category.setEditable(False)
                for name in sorted(results[cat_key]):
                    self.scripts_found += 1
                    script = QStandardItem(name)
                    script.setData(
                        f": {self.author_list[name]}",
                        Qt.StatusTipRole
                    )
                    script.setEditable(False)
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {dbmodule.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = dbmodule.i18n.t(
                self.gui_scripts_found,
                count=self.scripts_found
            )
            self.status_left.setText(self.last_scr_result)

    # show not found text
    def search_not_found(self):
        model = self.scr_treeview.model()
        model.clear()
        result = QStandardItem(dbmodule.i18n.t(self.gui_script_not))
        result.setData(
            dbmodule.i18n.t(self.gui_script_not),
            Qt.StatusTipRole
        )
        result.setEditable(False)
        result.setSelectable(False)
        model.appendRow(result)
        self.scr_treeview.setModel(model)
        self.scr_treeview.model().setHorizontalHeaderLabels(
            [f"  {dbmodule.i18n.t('gui.search_results')}"]
        )
        self.last_scr_result = dbmodule.i18n.t(self.gui_script_not)
        self.status_left.setText(self.last_scr_result)

    # reset search results
    def reset_search_results(self, pattern):
        self.last_scr_search = pattern
        if self.scripts_found != self.total_scripts and\
                len(self.last_scr_search) < 2:
            self.scripts_found = self.total_scripts
            self.load_scripts()
            self.last_scr_search = ""
            self.last_scr_result = ""
            self.status_left.setText(self.welcome)

    # search favorites when search button is pressed
    def init_fav_search(self):
        self.search_fav()

    # search favorites when enter key is pressed
    def fav_enter_pressed(self):
        self.search_fav()

    # search favorites when a ley is pressed
    def fav_key_pressed(self):
        if self.search_onkey:
            self.search_fav()

    # search favorites
    def search_fav(self):
        pattern = self.fsearch_text.text()
        if len(pattern) >= 2 and self.last_fav_search != pattern\
                and len(self.fav_list) > 0:
            results = {}
            self.last_fav_search = pattern
            fav_found = 0
            for fav_key in self.fav_list.keys():
                if pattern in fav_key:
                    fav_found += 1
                    results[fav_key] = self.fav_list[fav_key]
            self.show_fav_results(results, fav_found)
        else:
            self.last_fav_search = pattern
            if self.fav_treeview.model().rowCount() < len(self.fav_list)\
                    and len(self.last_fav_search) < 2:
                self.load_favorites()
                self.last_fav_search = ""
                self.last_fav_result = ""
                self.status_left.setText(self.welcome)

    # show favorite search results
    def show_fav_results(self, results, fav_count):
        fmodel = self.fav_treeview.model()
        if len(results) > 0:
            fmodel.clear()
            for fav in results.keys():
                fav_name = QStandardItem(str(fav))
                fav_name.setEditable(False)
                fav_name.setSizeHint(QSize(160, 25))
                fav_name.setData(dbmodule.i18n.t(
                    "gui.fav_info",
                    script=fav,
                    author=self.author_list[fav]
                ), Qt.StatusTipRole)
                fav_icon = QStandardItem(self.get_favorite_img(
                    results[fav]), dbmodule.get_ranking_text(results[fav]))
                fav_icon.setEditable(False)
                fav_icon.setSizeHint(QSize(60, 25))
                fmodel.appendRow([fav_name, fav_icon])
            self.fav_treeview.setModel(fmodel)
            self.fav_treeview.model().setHorizontalHeaderLabels(
                [self.script_text, "Ranking"])
            self.fav_treeview.setColumnWidth(0, 160)
            self.fav_treeview.setColumnWidth(1, 60)
            self.last_fav_result = dbmodule.i18n.t(
                "gui.fav_found",
                count=fav_count
            )
            self.status_left.setText(self.last_fav_result)
        else:
            fmodel.clear()
            result = QStandardItem(dbmodule.i18n.t("gui.fav_not_found"))
            result.setEditable(False)
            result.setSelectable(False)
            fmodel.appendRow(result)
            self.fav_treeview.setModel(fmodel)
            self.fav_treeview.model().setHorizontalHeaderLabels(
                [f"  {dbmodule.i18n.t('gui.search_results')}"])
            self.fav_treeview.setColumnWidth(0, 247)
            self.fav_treeview.setColumnWidth(1, 60)
            self.last_fav_result = dbmodule.i18n.t("gui.fav_not_found")
            self.status_left.setText(self.last_fav_result)

    # clear script qlineedit text and reload data in treeview
    def clear_search(self):
        if self.search_text.text() != "":
            self.search_text.setText("")
        self.last_scr_result = ""
        self.status_left.setText(self.welcome)
        self.load_scripts()

    # clear favorites qlinedit text and reload data in treeview
    def clear_fav_search(self):
        if self.fsearch_text.text() != "":
            self.fsearch_text.setText("")
        self.last_fav_result = ""
        self.status_left.setText(self.welcome)
        self.load_favorites()

    # show contextmenu with actions to add favorite
    # or collapse and expand all items
    def show_add_fav(self, pos):
        try:
            if self.scr_treeview.currentIndex().isValid():
                script = self.scr_treeview.model().itemFromIndex(
                    self.scr_treeview.currentIndex())
                if script.parent() != None:
                    self.exec_add_fav(script, pos)
                else:
                    if script.text() != dbmodule.i18n.t(self.gui_script_not):
                        self.exec_category_opts(pos)
        except Exception as e:
            self.utils.print_traceback(e)

    # show add favorite context menu
    def exec_add_fav(self, script, pos):
        add_fav = QMenu(self)
        add_menu = QAction(
            QIcon(
                f"{self.resources_path}plus.png"
            ),
            dbmodule.i18n.t("gui.add_fav")
        )
        add_fav.addAction(add_menu)
        click_btn = add_fav.exec_(
            self.sender().viewport().mapToGlobal(pos)
        )
        if add_menu == click_btn:
            from libs.fav_dlg import FavDlg
            ranking_dlg = FavDlg(self)
            ranking_dlg.set_images(self.resources_path, self.window_icon)            
            ranking_dlg.set_label_script(script.text(), 0)
            ranking_dlg.saveRanking.connect(self.add_favorite)
            ranking_dlg.exec_()

    # show collapse and expand category context menu
    def exec_category_opts(self, pos):
        tree_menu = QMenu(self)
        collapse_menu = QAction(
            QIcon(
                f"{self.resources_path}minus.png"),
            dbmodule.i18n.t("gui.collapse_all"
                            )
        )
        expand_menu = QAction(
            QIcon(
                f"{self.resources_path}plus.png"),
            dbmodule.i18n.t("gui.expand_all"
                            )
        )
        tree_menu.addAction(collapse_menu)
        tree_menu.addSeparator()
        tree_menu.addAction(expand_menu)
        click_btn = tree_menu.exec_(
            self.scr_treeview.viewport().mapToGlobal(pos)
        )
        if collapse_menu == click_btn:
            self.scr_treeview.collapseAll()
        if expand_menu == click_btn:
            self.scr_treeview.expandAll()

    # add favorite
    def add_favorite(self, script, ranking):
        try:
            result, msg = self.create_gui_fav(
                name=script,
                ranking=ranking
            )
            if result:
                fav_name = QStandardItem(script)
                fav_name.setEditable(False)
                fav_name.setSizeHint(QSize(240, 25))
                fav_icon = QStandardItem(
                    self.get_favorite_img(ranking),
                    dbmodule.get_ranking_text(ranking)
                )
                fav_icon.setSizeHint(QSize(20, 25))
                self.fav_treeview.model().appendRow([fav_name, fav_icon])
                if script not in self.fav_list.keys():
                    self.fav_list[script] = ranking
                self.clear_fav_search()
                QMessageBox.information(
                    self,
                    dbmodule.i18n.t(self.gui_dock_fav),
                    msg,
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
            else:
                self.show_exception(msg)
        except Exception as e:
            self.show_exception(e)

    # show contextmenu with actions to
    # update, delete and delete all favorites
    def show_fav_opts(self, pos):
        try:
            if self.fav_treeview.currentIndex().isValid():
                script = self.fav_treeview.model().itemFromIndex(
                    self.fav_treeview.currentIndex())\
                    if self.fav_treeview.currentIndex().column() == 0\
                    else\
                    self.fav_treeview.model().item(
                        self.fav_treeview.currentIndex().row(), 0
                )
                if script.text() in self.fav_list.keys():
                    show_menu = QMenu(self)
                    del_fav_act = QAction(
                        QIcon(
                            f"{self.resources_path}minus.png"
                        ),
                        dbmodule.i18n.t("gui.del_fav")
                    )
                    del_fav_act.setObjectName("del_fav")
                    del_all_fav_act = QAction(
                        QIcon(
                            f"{self.resources_path}minus.png"
                        ),
                        dbmodule.i18n.t("gui.del_all_favs")
                    )
                    del_all_fav_act.setObjectName("del_all_fav")
                    mod_fav_act = QAction(
                        QIcon(
                            f"{self.resources_path}update.png"
                        ),
                        dbmodule.i18n.t("gui.update_ranking")
                    )
                    mod_fav_act.setObjectName("mod_fav")
                    show_menu.addAction(mod_fav_act)
                    show_menu.addSeparator()
                    show_menu.addAction(del_fav_act)
                    show_menu.addSeparator()
                    show_menu.addAction(del_all_fav_act)
                    click_btn = show_menu.exec_(
                        self.sender()
                        .viewport().mapToGlobal(pos)
                    )
                    self.exec_fav_menu(click_btn, script)
        except Exception as e:
            self.show_exception(e)

    # execute favorite menu events
    def exec_fav_menu(self, click_btn, script):
        if click_btn != None:
            if "del_fav" == click_btn.objectName():
                self.del_fav(script)
            if "mod_fav" == click_btn.objectName():
                self.mod_fav(script)
            if "del_all_fav" == click_btn.objectName():
                self.del_all_fav(script)

    # delete favorite from context menu
    def del_fav(self, script):
        if self.delete_gui_fav(name=script.text()):
            self.fav_list.pop(script.text())
            self.fav_treeview.model().removeRows(
                script.index().row(),
                1,
                QModelIndex()
            )

    # update favorite from context menu
    def mod_fav(self, script):
        if script.text() not in self.fav_list.values():
            self.load_favorites_data()
            ranking = self.fav_list[script.text()]
            self.create_fav_dlg(script.text(), ranking)

    # delete all favorites from context menu
    def del_all_fav(self, script):
        if len(self.fav_treeview.selectionModel().selectedIndexes()) > 0:
            if self.delete_all_fav():
                self.fav_treeview.model().clear()
                self.fav_treeview.model().setHorizontalHeaderLabels(
                    [self.script_text, "Ranking"]
                )
                self.fav_treeview.setColumnWidth(0, 247)
                self.fav_treeview.setColumnWidth(1, 60)
                self.fav_list = dict()

    # create update favorite dialog
    def create_fav_dlg(self, script, ranking):
        from libs.fav_dlg import FavDlg
        fav_dlg = FavDlg(self)
        fav_dlg.set_images(self.resources_path, self.window_icon)
        fav_dlg.set_label_script(script=script, ranking=ranking)
        fav_dlg.saveRanking.connect(self.update_favorite)
        fav_dlg.exec_()

    # update favorite
    def update_favorite(self, script, ranking):
        try:
            if self.fav_treeview.currentIndex().column() == 0:
                sc_item = self.fav_treeview.model().itemFromIndex(
                    self.fav_treeview.currentIndex()
                )
            else:
                sc_item = self.fav_treeview.model().item(
                    self.fav_treeview.currentIndex().row(),
                    0
                )
            if self.fav_list[script] != ranking:
                result, msg = self.update_gui_fav(
                    name=script,
                    ranking=ranking
                )
                if result:
                    self.fav_list[script] = ranking
                    item_img = self.fav_treeview.model().item(
                        sc_item.row(),
                        1
                    )
                    item_img.setText(dbmodule.get_ranking_text(ranking))
                    item_img.setIcon(self.get_favorite_img(ranking))
                    self.status_left.setText(
                        dbmodule.i18n.t(self.gui_dock_fav))
                    QMessageBox.information(
                        self,
                        dbmodule.i18n.t(self.gui_dock_fav),
                        msg, QMessageBox.Ok,
                        QMessageBox.Ok
                    )
                else:
                    self.show_exception(msg)
            else:
                QMessageBox.information(
                    self,
                    "Ranking",
                    dbmodule.i18n.t("gui.different_ranking"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
        except Exception as e:
            self.show_exception(e)

    # establish search option
    def set_search_opt(self, opt):
        if opt == 1:
            self.search_opt = 1
            self.last_scr_search = ""
            self.script_validator.setRegExp(self.get_regexp())
        if opt == 2:
            self.search_opt = 2
            self.last_scr_search = ""
            self.script_validator.setRegExp(self.get_regexp())
        if opt == 3:
            self.search_opt = 3
            self.last_scr_search = ""
            self.script_validator.setRegExp(self.get_regexp())

    # select language from menu
    def select_lang(self):
        lang_ = None
        if self.sender() == self.m_spanish:
            if self.m_spanish.isChecked():
                lang_ = 'es'
            else:
                self.m_spanish.setChecked(True)
        if self.sender() == self.m_english:
            if self.m_english.isChecked():
                lang_ = 'en'
            else:
                self.m_english.setChecked(True)
        if self.lang != lang_:
            self.lang = lang_
            self.reload_translations()

    # reload gui translations
    def reload_translations(self):
        self.load_language(True)
        self.remove_script_tabs()
        self.load_scripts()
        self.load_favorites()
        self.load_text_translations()
        self.update_yaml_file()
        self.init_menu()

    # toggle splash animation
    def toggle_splash_anim(self, checked):
        checked = int(checked)
        if self.show_anim != checked:
            self.show_anim = checked
            self.update_yaml_file()

    # select theme from menu
    def select_theme(self):
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
        if self.theme != theme_ and theme_ != None:
            self.theme = theme_
            self.set_theme()
            self.update_tab_theme()
            self.update_yaml_file()
            self.init_menu()

    # update tabs theme
    def update_tab_theme(self):
        theme_name = self.utils.get_theme_name(self.theme)
        if self.tab_view.count() >= 0:
            for tab in range(self.tab_view.count()):
                self.tab_view.setCurrentIndex(tab)
                self.tab_view.currentWidget()\
                    .page().settings().setAttribute(
                    QWebSettings.JavascriptEnabled,
                    True
                )
                self.tab_view.currentWidget()\
                    .page().currentFrame().evaluateJavaScript(
                    f"document.querySelector('html').setAttribute(\
                    'id', '{theme_name}')"
                )
                self.tab_view.currentWidget()\
                    .page().settings().setAttribute(
                    QWebSettings.JavascriptEnabled,
                    False
                )

    # active/deactive search on key pressed from menu
    def select_key_on(self, checked):
        checked = int(checked)
        if self.search_onkey != checked:
            self.search_onkey = checked
            self.update_yaml_file()

    # select search by from menu
    def select_searchby(self):
        search_opt_ = None
        if self.sender() == self.m_name:
            if self.m_name.isChecked():
                search_opt_ = 1
            else:
                self.m_name.setChecked(True)
        if self.sender() == self.m_author:
            if self.m_author.isChecked():
                search_opt_ = 2
            else:
                self.m_author.setChecked(True)
        if self.sender() == self.m_category:
            if self.m_category.isChecked():
                search_opt_ = 3
            else:
                self.m_category.setChecked(True)
        if self.search_opt != search_opt_:
            self.search_opt = search_opt_
            self.update_yaml_file()
            self.init_menu()

    # show author dialog
    def init_author_window(self):
        from libs.about_dlg import AbtDlg
        abt = AbtDlg(self)
        abt.setLogo(self.window_icon)
        abt.exec_()

    # show qt version
    def init_qt_version(self):
        QMessageBox.aboutQt(self, dbmodule.i18n.t("gui.act_about_qt"))

    # open links from developer dialog
    def open_link(self, url):
        link = QUrl(url)
        if not link.isEmpty():
            QDesktopServices.openUrl(link)

    # show or hide dockwidgets
    def dock_visibility(self, visible):
        if self.sender() == self.scriptdock:
            self.scriptdock.setVisible(visible)
            self.m_scriptdock.setChecked(visible)
        if self.sender() == self.favoritedock:
            self.favoritedock.setVisible(visible)
            self.m_favoritedock.setChecked(visible)

    ''' Database Functions '''
    # create favorite

    def create_gui_fav(self, **kwargs):
        db = None
        try:
            db, cursor = dbmodule.get_connect()
            cursor.execute(
                "INSERT INTO favorites (name, ranking) VALUES (?, ?);",
                (kwargs["name"], kwargs["ranking"])
            )
            db.commit()
            if cursor.rowcount == 1:
                return (True, dbmodule.i18n.t("gui.fav_add"))
        except Exception as e:
            if "UNIQUE" in e.args[0]:
                return (False, dbmodule.i18n.t("gui.fav_already_added"))
            else:
                self.utils.print_traceback(e)
                return (False, "Error : " + e.args[0])
        finally:
            if db:
                db.close()

    # delete favorite
    def delete_gui_fav(self, **kwargs):
        db = None
        try:
            db, cursor = dbmodule.get_connect()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE name=?;",
                (kwargs["name"],)
            )
            db.commit()
            if cursor.rowcount == 1:
                QMessageBox.information(
                    self,
                    dbmodule.i18n.t(self.gui_dock_fav),
                    dbmodule.i18n.t("gui.fav_deleted"),
                    QMessageBox.Ok, QMessageBox.Ok
                )
                return True
        except Exception as e:
            self.show_exception(e)
        finally:
            if db:
                db.close()

    # delete all favorites
    def delete_all_fav(self):
        db = None
        try:
            db, cursor = dbmodule.get_connect()
            cursor = db.cursor()
            cursor.execute("DELETE FROM favorites;")
            db.commit()
            if cursor.rowcount >= 1:
                QMessageBox.information(
                    self,
                    dbmodule.i18n.t(self.gui_dock_fav),
                    dbmodule.i18n.t("gui.favs_deleted"),
                    QMessageBox.Ok, QMessageBox.Ok
                )
                return True
        except Exception as e:
            self.show_exception(e)
        finally:
            if db:
                db.close()

    # update favorite ranking
    def update_gui_fav(self, **kwargs):
        db = None
        try:
            db, cursor = dbmodule.get_connect()
            cursor.execute(
                "UPDATE favorites set ranking=? WHERE name=?;",
                (kwargs["ranking"], kwargs["name"])
            )
            db.commit()
            if cursor.rowcount == 1:
                cursor.close()
            return (True, dbmodule.i18n.t("gui.fav_updated"))
        except Exception as e:
            self.show_exception(e)
            return (False, "Error : " + e.args[0])
        finally:
            if db:
                db.close()

    # close event
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowstate', self.saveState())
        event.accept()

    # show dock widgets
    def show_dock(self, show):
        if self.sender() == self.m_scriptdock:
            self.scriptdock.setVisible(show)
            self.m_scriptdock.setChecked(show)
        if self.sender() == self.m_favoritedock:
            self.favoritedock.setVisible(show)
            self.m_favoritedock.setChecked(show)

    # show exception
    def show_exception(self, e):
        self.utils.print_traceback(e)
        msg = e.args[0] if type(e) == Exception else e
        QMessageBox.information(
            self,
            dbmodule.i18n.t("gui.exception"),
            str(msg), QMessageBox.Ok,
            QMessageBox.Ok
        )


if __name__ == "libs.ngui":
    global app
    app = QApplication(sys.argv)
    ngui = NGui()
    app.setStyle('Fusion')
    sys.exit(app.exec_())
