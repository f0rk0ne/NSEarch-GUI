#!/usr/bin/python
# -*- coding: utf-8 -*-
from signal import signal
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QRadioButton
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QPushButton

WIDTH_SIZE = 200
HEIGHT_SIZE = 80

class ConfDlg(QDialog):

    saveResult = Signal(dict, name='saveResult')
    win, config_vars = None, None
    active, inactive = None, None
    path, events = None, None
    lang_group, lang_es, lang_en = None, None, None
    search_on_group, search_on = None, None
    theme_group, theme_select = None, None
    splash_group, show_anim = None, None
    search_by_group, search_by = None, None
    vertical_title_group, v_title = None, None
    singletab_group, single_tab = None, None
    group_size = None
    themes = None    
    s_options = None    

    def __init__(self, parent, conf_vars):
        super(ConfDlg, self).__init__(parent)
        self.win = parent
        self.path = parent.resources_path
        self.config_vars = conf_vars
        self.themes = [
            self.win.i18n.t("gui.act_default"),
            self.win.i18n.t("gui.act_dark"),
            self.win.i18n.t("gui.act_light")
        ]
        self.s_options = [
            self.win.i18n.t("gui.act_name"),
            self.win.i18n.t("gui.act_author"),
            self.win.i18n.t("gui.act_category")
        ]
        self.group_size = QSize(
            WIDTH_SIZE,
            HEIGHT_SIZE
        )
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"Dialog")
        self.resize(472, 408)
        self.setMinimumSize(QSize(472, 0))
        self.setMaximumSize(QSize(500, 518))
        self.setWindowIcon(QIcon(f"{self.path}nmap-logo-small.png"))
        self.setWindowTitle(self.win.i18n.t("gui.st_configuration"))
        self.setSizeGripEnabled(False)
        self.init_layout()

    def init_layout(self):
        self.init_lang_groupbox()
        self.load_lang()
        grid_layout = QGridLayout(self)
        grid_layout.setObjectName(u"gridLayout")
        grid_layout.setHorizontalSpacing(30)
        grid_layout.setVerticalSpacing(20)
        grid_layout.setContentsMargins(20, 30, 20, 30)

        grid_layout.addWidget(self.lang_group, 0, 0, 1, 1)
        grid_layout.addWidget(self.theme_group, 0, 1, 1, 1)

        grid_layout.addWidget(self.search_on_group, 1, 0, 1, 1)
        grid_layout.addWidget(self.search_by_group, 1, 1, 1, 1)

        grid_layout.addWidget(self.splash_group, 2, 0, 1, 1)
        grid_layout.addWidget(self.vertical_title_group, 2, 1, 1, 1)

        grid_layout.addWidget(self.singletab_group, 3, 0, 1, 1)
        grid_layout.addWidget(self.tabcount_group, 3, 1, 1, 1)

        grid_layout.addWidget(self.btn_accept, 4, 0, 1, 1)
        grid_layout.addWidget(self.btn_cancel, 4, 1, 1, 1)


    def init_lang_groupbox(self):
        self.lang_group = QGroupBox(self)
        self.lang_group.setObjectName(u"lang_group")
        self.lang_group.setMinimumSize(self.group_size)
        self.lang_group.setMaximumSize(self.group_size)
        self.lang_group.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        lang_layout = QHBoxLayout(self.lang_group)
        lang_layout.setSpacing(15)
        lang_layout.setObjectName(u"lang_layout")
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.lang_es = QRadioButton(self.lang_group)
        self.lang_es.setObjectName(u"lang_es")
        self.lang_es.setText("Spanish")
        self.lang_es.setChecked(self.config_vars["lang"] == "es")

        self.lang_en = QRadioButton(self.lang_group)
        self.lang_en.setObjectName(u"lang_en")
        self.lang_en.setText("English")
        self.lang_en.setChecked(self.config_vars["lang"] == "en")

        lang_layout.addWidget(self.lang_es)
        lang_layout.addWidget(self.lang_en)
        self.lang_group.setLayout(lang_layout)
        self.init_theme_groupbox()

    def init_theme_groupbox(self):
        self.theme_group = QGroupBox(self)
        self.theme_group.setObjectName(u"theme_group")
        self.theme_group.setMinimumSize(self.group_size)
        self.theme_group.setMaximumSize(self.group_size)

        theme_layout = QHBoxLayout(self.theme_group)
        theme_layout.setObjectName(u"theme_layout")

        self.theme_select = QComboBox(self.theme_group)
        self.theme_select.setMinimumSize(QSize(150, 30))
        self.theme_select.addItem("Default")
        self.theme_select.addItem("Dark")
        self.theme_select.addItem("Light")
        self.theme_select.setObjectName(u"theme_select")
        self.theme_select.setCurrentIndex(self.config_vars["theme"]-1)

        theme_layout.addWidget(self.theme_select)
        self.theme_group.setLayout(theme_layout)
        self.init_searchkey_group()

    def init_searchkey_group(self):
        self.active = self.win.i18n.t("gui.active")
        self.inactive = self.win.i18n.t("gui.inactive")
        self.search_on_group = QGroupBox(self)
        self.search_on_group.setObjectName(u"search_on_group")
        self.search_on_group.setMinimumSize(self.group_size)
        self.search_on_group.setMaximumSize(self.group_size)
        self.search_on_group.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        searchkey_layout = QHBoxLayout(self.search_on_group)
        searchkey_layout.setObjectName(u"searchkey_layout")
        searchkey_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.search_on = QRadioButton(self.search_on_group)
        self.search_on.setObjectName(u"search_on")
        self.search_on.setChecked(self.config_vars["searchOnKey"])
        self.search_on.setText(
            self.active
            if self.config_vars["searchOnKey"]
            else self.inactive
        )
        self.search_on.clicked[bool].connect(self.update_text)

        searchkey_layout.addWidget(self.search_on)
        self.search_on_group.setLayout(searchkey_layout)
        self.init_searchby_group()

    def init_searchby_group(self):
        self.search_by_group = QGroupBox(self)
        self.search_by_group.setObjectName(u"search_by_group")
        self.search_by_group.setMinimumSize(self.group_size)
        self.search_by_group.setMaximumSize(self.group_size)

        searchby_layout = QHBoxLayout(self.search_by_group)
        searchby_layout.setObjectName(u"searchby_layout")

        self.search_by = QComboBox(self.search_by_group)
        self.search_by.setMinimumSize(QSize(150, 30))
        self.search_by.setObjectName(u"search_by")
        self.search_by.addItems(
            [
                "Name",
                "Author",
                "Category"
            ]
        )
        self.search_by.setCurrentIndex(self.config_vars["searchOpt"]-1)

        searchby_layout.addWidget(self.search_by)
        self.search_by_group.setLayout(searchby_layout)
        self.init_show_anim_group()

    def init_show_anim_group(self):
        self.show_txt = self.win.i18n.t("gui.show")
        self.hide_txt = self.win.i18n.t("gui.hide")
        self.splash_group = QGroupBox(self)
        self.splash_group.setObjectName(u"splash_group")
        self.splash_group.setMinimumSize(QSize(200, 80))
        self.splash_group.setMaximumSize(QSize(200, 80))

        showanim_layout = QHBoxLayout(self.splash_group)
        showanim_layout.setObjectName(u"showanim_layout")
        showanim_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.show_anim = QRadioButton(self.splash_group)
        self.show_anim.setObjectName(u"show_anim")
        self.show_anim.setChecked(bool(self.config_vars["splashAnim"]))
        self.show_anim.setText(
            self.show_txt
            if self.config_vars["splashAnim"]
            else self.hide_txt
        )
        self.show_anim.clicked[bool].connect(self.update_anim_text)

        showanim_layout.addWidget(self.show_anim)
        self.splash_group.setLayout(showanim_layout)
        self.init_verticalmenu_group()

    def init_verticalmenu_group(self):
        self.vertical_title_group = QGroupBox(self)
        self.vertical_title_group.setObjectName(u"vertical_title_group")
        self.vertical_title_group.setMinimumSize(self.group_size)
        self.vertical_title_group.setMaximumSize(self.group_size)

        verticalmenu_layout = QHBoxLayout(self.vertical_title_group)
        verticalmenu_layout.setObjectName(u"vertical_title_group")
        verticalmenu_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.v_title = QRadioButton(self.vertical_title_group)
        self.v_title.setObjectName(u"v_title")
        self.v_title.setChecked(bool(self.config_vars["verticalTitle"]))
        self.v_title.setText(
            self.active
            if self.config_vars["verticalTitle"]
            else self.inactive
        )
        self.v_title.clicked["bool"].connect(self.update_text)

        verticalmenu_layout.addWidget(self.v_title)
        self.vertical_title_group.setLayout(verticalmenu_layout)
        self.init_singletab_group()
    
    def init_singletab_group(self):
        self.singletab_group = QGroupBox(self)
        self.singletab_group.setObjectName(u"singletab_group")
        self.singletab_group.setMaximumSize(self.group_size)
        self.singletab_group.setMinimumSize(self.group_size)

        singletab_layout = QHBoxLayout(self.singletab_group)
        singletab_layout.setObjectName(u"singletab_layout")
        singletab_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.single_tab = QRadioButton(self.singletab_group)
        self.single_tab.setObjectName(u"single_tab")
        self.single_tab.setChecked(self.config_vars["singleTab"])
        self.single_tab.clicked["bool"].connect(self.update_text)

        self.single_tab.setText(
            self.active 
            if self.config_vars["singleTab"]
            else self.inactive
        )

        singletab_layout.addWidget(self.single_tab)
        self.singletab_group.setLayout(singletab_layout)
        self.init_tabcount_group()

    def init_tabcount_group(self):
        count_values = ["5","10","20","30"]
        self.tabcount_group = QGroupBox(self)
        self.tabcount_group.setObjectName(u"tabcount_group")
        self.tabcount_group.setMaximumSize(self.group_size)
        self.tabcount_group.setMinimumSize(self.group_size)

        tabcount_layout = QHBoxLayout(self.tabcount_group)
        tabcount_layout.setObjectName(u"tabcount_layout")
        tabcount_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.tab_count = QComboBox(self.tabcount_group)
        self.tab_count.setObjectName(u"tab_count")
        self.tab_count.setMinimumSize(QSize(50, 30))
        self.tab_count.addItems(count_values)
        self.tab_count.setCurrentIndex(
            self.tab_count.findText(
                str(self.config_vars["tabCount"])
                ,Qt.MatchFlag.MatchContains
            )
        )
    
        tabcount_layout.addWidget(self.tab_count)
        self.tabcount_group.setLayout(tabcount_layout)
        self.init_buttons()

    def init_buttons(self):
        self.btn_accept = QPushButton(self)
        self.btn_accept.setObjectName(u"btn_accept")
        self.btn_accept.setMinimumSize(QSize(200, 38))
        self.btn_accept.setMaximumSize(QSize(200, 38))
        self.btn_accept.clicked[bool].connect(self.save)

        self.btn_cancel = QPushButton(self)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(200, 38))
        self.btn_cancel.setMaximumSize(QSize(200, 38))
        self.btn_cancel.clicked.connect(self.cancel)

    def load_lang(self):
        self.lang_group.setTitle(
            self.win.i18n.t("gui.menu_language")
        )
        self.search_on_group.setTitle(
            self.win.i18n.t("gui.act_search_on_key")
        )
        self.theme_group.setTitle(
            self.win.i18n.t("gui.menu_theme")
        )
        self.search_by_group.setTitle(
            self.win.i18n.t("gui.menu_search_opts")
        )
        self.splash_group.setTitle(
            self.win.i18n.t("gui.st_anim")
        )
        self.vertical_title_group.setTitle(
            self.win.i18n.t("gui.act_vertical_title")
        )
        self.singletab_group.setTitle(
            self.win.i18n.t("gui.act_single_tab")
        )
        self.tabcount_group.setTitle(
            self.win.i18n.t("gui.act_tab_count")
        )

        self.btn_accept.setText(self.win.i18n.t("gui.accept"))
        self.btn_cancel.setText(self.win.i18n.t("gui.cancel"))
        self.lang_es.setText(self.win.i18n.t("gui.act_spanish"))
        self.lang_en.setText(self.win.i18n.t("gui.act_english"))

        for a, b in enumerate(self.themes):
            self.theme_select.setItemText(a, b)

        for c, d in enumerate(self.s_options):
            self.search_by.setItemText(c, d)

    @Slot(bool)
    def update_text(self, checked):
        if self.sender() == self.search_on:
            self.search_on.setText(
                self.active if checked else self.inactive
            )
        elif self.sender() == self.v_title:
            self.v_title.setText(
                self.active if checked else self.inactive
            )
        elif self.sender() == self.single_tab:
            self.single_tab.setText(
                self.active if checked else self.inactive
            )

    @Slot(bool)
    def update_anim_text(self, checked):
        self.show_anim.setText(
            self.show_txt
            if checked
            else self.hide_txt
        )

    @Slot(bool)
    def save(self):
        self.config_vars["lang"] = 'es' if self.lang_es.isChecked() else 'en'
        self.config_vars["theme"] = self.theme_select.currentIndex()+1
        self.config_vars["searchOnKey"] = int(self.search_on.isChecked())
        self.config_vars["searchOpt"] = self.search_by.currentIndex()+1
        self.config_vars["splashAnim"] = int(self.show_anim.isChecked())
        self.config_vars["verticalTitle"] = int(self.v_title.isChecked())
        
        single_tab_ = int(self.single_tab.isChecked())
        reload_tabs = single_tab_ != self.config_vars["singleTab"]
        self.config_vars["singleTab"] = single_tab_

        tab_count_ = int(self.tab_count.currentText())
        resize_tabcount = tab_count_ != self.config_vars["tabCount"]
        self.config_vars["tabCount"] = tab_count_

        if reload_tabs and self.win.main_widget.tab_view.count() > 2:
            self.win.main_widget.remove_script_tabs()
        if resize_tabcount:
            self.win.main_widget.resize_tab_count()
        
        self.saveResult.emit(
            self.config_vars
        )
        self.close()

    @Slot()
    def cancel(self):
        self.close()
