from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QAction
from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QDockWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QWidget 
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton 
from PySide6.QtWidgets import QRadioButton
from PySide6.QtWidgets import QTreeView
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox
from sqlite3 import IntegrityError

class scriptDock(QDockWidget):

    MainWindow = None
    sc_layout = None
    scr_treeview = None
    s_name = None
    s_author = None
    s_category = None
    search_text = None
    search_btn = None
    clear_btn = None
    last_scr_search, last_scr_result = "", ""
    gui_script_cat = "gui.scripts_category"
    gui_scripts_found = "gui.scripts_found"
    author_txt = ""

    def __init__(self, parent):
        super().__init__(parent)
        try:
            self.win = parent        
            self.author_txt = self.win.i18n.t(
                "gui.act_author"
            )
            self.setupUi()
            self.init_search_by_option()        
            self.scr_treeview.setModel(
                QStandardItemModel(0, 1, self)
            )
            self.load_scripts()
            self.scr_treeview.selectionModel().currentChanged.connect(
                self.script_selected
            )
            self.load_lang()
        except Exception as e:
            parent.show_exception(e)

    def setupUi(self):
        self.setObjectName("scriptdock")
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth()
        )
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(273, 320))
        self.setMaximumSize(QSize(330, 524287))        
        self.setFloating(False)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable|
            QDockWidget.DockWidgetFeature.DockWidgetMovable|
            QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar
        )
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea
        )
        self.setWindowTitle("Scripts")
        self.init_layout()
    
    def init_layout(self):
        self.sc_layout = QWidget()
        self.sc_layout.setObjectName("sc_layout")

        self.gridLayout = QGridLayout(self.sc_layout)
        self.gridLayout.setObjectName("gridLayout")

        self.init_search_controls()
        self.gridLayout.addWidget(self.search_text, 0, 0, 1, 1)     
        self.gridLayout.addWidget(self.search_btn, 0, 1, 1, 1)      
        self.gridLayout.addWidget(self.clear_btn, 0, 2, 1, 1)

        self.gridLayout.addLayout(self.get_searchby_layout(), 1, 0, 1, 3)
        self.init_treeview()
        self.gridLayout.addWidget(self.scr_treeview, 2, 0, 1, 3)
        self.setWidget(self.sc_layout)
        self.init_regexp()

    def get_searchby_layout(self):
        search_opt_layout = QHBoxLayout()
        search_opt_layout.setObjectName("search_opt_layout")

        self.s_name = QRadioButton("Name", self.sc_layout)
        self.s_name.setObjectName("s_name")
        self.s_name.clicked.connect(self.set_search_opt)
        search_opt_layout.addWidget(self.s_name)

        self.s_author = QRadioButton("Author", self.sc_layout)
        self.s_author.setObjectName("s_author")
        self.s_author.clicked.connect(self.set_search_opt)
        search_opt_layout.addWidget(self.s_author)

        self.s_category = QRadioButton("Category", self.sc_layout)
        self.s_category.setObjectName("s_category")
        self.s_category.clicked.connect(self.set_search_opt)
        search_opt_layout.addWidget(self.s_category)
        return search_opt_layout

    def init_treeview(self):
        self.scr_treeview = QTreeView(self.sc_layout)
        self.scr_treeview.setObjectName("scr_treeview")
        self.scr_treeview.setMinimumSize(QSize(200, 250))
        self.scr_treeview.setMouseTracking(True)
        self.scr_treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.scr_treeview.setIconSize(QSize(55, 22))
        self.scr_treeview.setIndentation(10)
        self.scr_treeview.customContextMenuRequested.connect(
            self.show_add_fav
        )

    def init_search_controls(self):
        self.search_text = QLineEdit(self.sc_layout)
        self.search_text.setObjectName("search_text")
        self.search_text.setMinimumSize(QSize(0, 40))
        self.search_text.editingFinished.connect(
            self.search_enter_pressed
        )
        self.search_text.textEdited.connect(
            self.search_key_pressed
        )

        self.search_btn = QPushButton(self.sc_layout)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setMinimumSize(QSize(40, 40))
        self.search_btn.setMaximumSize(QSize(30, 16777215))
        self.search_btn.clicked.connect(
            self.init_search
        )
        sicon = QIcon()
        sicon.addFile(
            f"{self.win.resources_path}glass.png", 
            QSize(24, 24),
            QIcon.Normal,
            QIcon.Off
        )
        self.search_btn.setIcon(sicon)
        self.search_btn.setIconSize(QSize(24, 24))

        self.clear_btn = QPushButton(self.sc_layout)
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.setMinimumSize(QSize(40, 40))
        self.clear_btn.setMaximumSize(QSize(30, 16777215))
        self.clear_btn.clicked.connect(
            self.clear_search
        )
        cicon = QIcon()
        cicon.addFile(
            f"{self.win.resources_path}brush.png",
            QSize(24, 24),
            QIcon.Normal,
            QIcon.Off
        )
        self.clear_btn.setIcon(cicon)
        self.clear_btn.setIconSize(QSize(24, 24))

    def load_lang(self):
        self.setWindowTitle(
            self.win.i18n.t("gui.dock_scripts")
        )
        self.search_text.setPlaceholderText(
            self.win.i18n.t("gui.search_placeholder")
        )
        self.s_name.setText(
            self.win.i18n.t("gui.act_name")
        )        
        self.s_author.setText(
            self.win.i18n.t("gui.act_author")
        )        
        self.s_category.setText(
            self.win.i18n.t("gui.act_category")
        )  
        self.load_status()      

    def load_status(self):
        self.search_text.setStatusTip(
            f'  {self.win.i18n.t("gui.st_search")}'
        )
        self.search_btn.setStatusTip(
            f'  {self.win.i18n.t("gui.st_search_scripts")}'
        )
        self.clear_btn.setStatusTip(
            f'  {self.win.i18n.t("gui.st_clear_script_search")}'
        )
        self.s_name.setStatusTip(
            f'  {self.win.i18n.t("gui.st_name")}'
        )
        self.s_author.setStatusTip(
            f'  {self.win.i18n.t("gui.st_author")}'
        )
        self.s_category.setStatusTip(
            f'  {self.win.i18n.t("gui.st_category")}'
        )

    def init_search_by_option(self):
        self.s_name.setChecked(
            self.win.yaml_vars["searchOpt"] == 1
        )
        self.s_author.setChecked(
            self.win.yaml_vars["searchOpt"] == 2
        )
        self.s_category.setChecked(
            self.win.yaml_vars["searchOpt"] == 3
        )

    def init_regexp(self):
        reg_exp = None        
        if self.win.yaml_vars["searchOpt"] == 1:
            reg_exp = QRegularExpression("[A-Za-z0-9\-]{0,100}")
        elif self.win.yaml_vars["searchOpt"] == 2:
            reg_exp = QRegularExpression("[A-Za-z0-9\s]{0,100}")
        elif self.win.yaml_vars["searchOpt"] == 3:
            reg_exp = QRegularExpression("[A-Za-z0-9]{0,100}")
        self.search_text.setValidator(
            QRegularExpressionValidator(reg_exp)
        )

    def load_scripts(self):
        model = self.scr_treeview.model()
        model.clear()
        for cat_key in sorted(
            self.win.scripts_list
        ):
            category = QStandardItem(cat_key)
            category.setData(
                f'''  {self.win.i18n.t(
                    "gui.scripts_category",
                    count=len(self.win.scripts_list[cat_key]),
                    category=cat_key
                )}''',
                Qt.StatusTipRole
            )
            category.setEditable(False)
            category.setSelectable(False)
            for name in sorted(
                self.win.scripts_list[cat_key]
            ):
                script = QStandardItem(name)
                author = self.win.author_list[name]
                script.setData(
                    f"  {self.win.author_txt}: {author}",
                    Qt.StatusTipRole
                )
                script.setEditable(False)
                category.appendRow(script)
            model.appendRow(category)
        model.setHorizontalHeaderLabels(
            [f"  {self.win.i18n.t('gui.categories')}"]
        )

    def select_tab_script(self, script):
        for t_index in range(0, self.scr_treeview.model().rowCount()):
            scr_item = self.scr_treeview.model().item(t_index, 0)
            if scr_item != None and scr_item.hasChildren():
                for c_index in range(0, scr_item.rowCount()):
                    chl_item = scr_item.child(c_index, 0)
                    if script in chl_item.text():
                        self.scr_treeview.setCurrentIndex(
                            chl_item.index())
                        break

    @Slot()
    def set_search_opt(self):
        if self.sender() == self.s_name:
            self.win.yaml_vars["searchOpt"] = 1
            self.last_scr_search = ""
        if self.sender() == self.s_author:
            self.win.yaml_vars["searchOpt"] = 2
            self.last_scr_search = ""
        if self.sender() == self.s_category:
            self.win.yaml_vars["searchOpt"] = 3
            self.last_scr_search = ""

    @Slot(int)
    def show_add_fav(self, pos):
        try:
            if self.scr_treeview.currentIndex().isValid():
                script = self.scr_treeview.model().itemFromIndex(
                    self.scr_treeview.currentIndex())
                if script.parent() != None:
                    self.exec_add_fav(script, pos)
                else:
                    if script.text() != self.win.i18n.t(
                        "gui.script_not_found"
                    ):
                        self.exec_category_opts(pos)
        except Exception as e:
            self.win.show_exception(e)

    def exec_add_fav(self, script, pos):
        add_fav = QMenu(self.win)
        add_menu = QAction(
            QIcon(
                f"{self.win.resources_path}plus.png"
            ),
            self.win.i18n.t("gui.add_fav")
        )
        open_script_web = QAction(
            self.win.i18n.t("gui.script_web")
        )
        add_fav.addAction(add_menu)
        add_fav.addSeparator()
        add_fav.addAction(open_script_web)
        click_btn = add_fav.exec_(
            self.sender().viewport().mapToGlobal(pos)
        )
        if add_menu == click_btn:            
            from libs.fav_dlg import FavDlg
            ranking_dlg = FavDlg(self.win)
            ranking_dlg.set_label_script(script.text(), 0)
            ranking_dlg.saveRanking.connect(self.add_favorite)
            ranking_dlg.exec()
        elif click_btn == open_script_web:
            self.win.open_url(f'https://nmap.org/nsedoc/scripts/{script.text()}.html')

    @Slot(str, str)
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
                    self.win.get_favorite_img(ranking),
                    self.win.dbm.get_ranking_text(ranking)
                )
                fav_icon.setSizeHint(QSize(20, 25))
                self.win.fav_dock.fav_treeview.model().appendRow(
                    [fav_name, fav_icon]
                )
                if script not in self.win.fav_list.keys():
                    self.win.fav_list[script] = ranking
                self.win.fav_dock.clear_fav_search()
                QMessageBox.information(
                    self,
                    self.win.i18n.t("gui.dock_favorites"),
                    msg,
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
            else:
                raise Exception(msg)
        except Exception as e:
            self.win.show_exception(e)

    def create_gui_fav(self, **kwargs):
        db = None
        already = False
        try:
            db, cursor = self.win.dbm.get_connect(True)
            cursor.execute(
                "INSERT INTO favorites (name, ranking) VALUES (?, ?);",
                (kwargs["name"], kwargs["ranking"])
            )
            db.commit()
            if cursor.rowcount == 1:
                return (True, self.win.i18n.t("gui.fav_add"))
        except IntegrityError as e:
            already = True
            pass
        except Exception as e:
            return (False, "Error : " + e.args[0])
        finally:
            if db:
                db.close()
            if already:
                return (False, self.win.i18n.t("gui.fav_already_added"))       

    def exec_category_opts(self, pos):
        tree_menu = QMenu(self.win)
        collapse_menu = QAction(
            QIcon(f"{self.win.resources_path}minus.png"),
            self.win.i18n.t("gui.collapse_all"
                        )
        )
        expand_menu = QAction(
            QIcon(f"{self.win.resources_path}plus.png"),
            self.win.i18n.t("gui.expand_all")
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

    @Slot()
    def search_enter_pressed(self):
        self.search()

    @Slot()
    def search_key_pressed(self):
        if self.win.yaml_vars["searchOnKey"]:
            self.search()

    @Slot()
    def init_search(self):
        self.search()

    @Slot(int, int)
    def script_selected(self, current, previous):
        del previous
        script = self.scr_treeview.model().itemFromIndex(
            current
        )
        if script is not None:
            if script.parent() != None:
                self.win.main_widget.create_script_tab(
                    script.text()
                )

    def search(self):
        pattern = str(self.search_text.text()).lower()
        if len(pattern) >= 2 and self.last_scr_search != pattern:
            if self.win.yaml_vars["searchOpt"] == 1:
                self.show_search_results(
                    self.get_search_results(pattern)
                )
            elif self.win.yaml_vars["searchOpt"] == 2:
                self.show_author_results(
                    self.get_author_results(pattern)
                )
            elif self.win.yaml_vars["searchOpt"] == 3:
                self.show_category_results(
                    self.get_category_results(pattern)
                )
        else:
            self.reset_search_results(pattern)

    def show_search_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in sorted(results.keys()):
                category = QStandardItem(cat_key)
                category.setData(
                    self.win.i18n.t(
                        self.gui_script_cat,
                        count=len(results[cat_key]),
                        category=cat_key
                    ), Qt.StatusTipRole
                )
                category.setEditable(False)
                category.setSelectable(False)
                for name in sorted(results[cat_key]):
                    self.win.scripts_found += 1
                    script = QStandardItem(name)
                    script.setData(
                        self.win.author_txt +
                        f": {self.win.author_list[name]}",
                        Qt.StatusTipRole
                    )
                    script.setEditable(False)
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {self.win.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = self.win.i18n.t(
                self.gui_scripts_found,
                count = self.win.scripts_found
            )
            self.win.status_left.setText(
                self.last_scr_result
            )

    def get_search_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self.win.scripts_found = 0
        for key in self.win.scripts_list.keys():
            for name in self.win.scripts_list[key]:
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

    def show_author_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in sorted(results.keys()):
                category = QStandardItem(cat_key)
                category.setData(
                    self.win.i18n.t(
                        self.gui_script_cat,
                        count = len(results[cat_key]),
                        category = cat_key
                    ),
                    Qt.StatusTipRole
                )
                category.setEditable(False)
                category.setSelectable(False)
                for name in sorted(results[cat_key]):
                    self.win.scripts_found += 1
                    script = QStandardItem(name)
                    script.setEditable(False)
                    script.setData(
                        f"{self.win.author_txt}: " +
                        self.win.author_list[name],
                        Qt.StatusTipRole
                    )
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {self.win.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = self.win.i18n.t(
                self.gui_scripts_found,
                count = self.win.scripts_found
            )
            self.win.status_left.setText(
                self.last_scr_result
            )

    def get_author_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self. scripts_found = 0
        for key in sorted(self.win.scripts_list):
            for script in self.win.scripts_list[key]:
                if pattern.lower() in self.win.author_list[script].lower():
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

    def show_category_results(self, results):
        if results != False:
            model = self.scr_treeview.model()
            model.clear()
            for cat_key in results.keys():
                category = QStandardItem(cat_key)
                category.setData(
                    self.win.i18n.t(
                        self.gui_script_cat,
                        count = len(self.win.scripts_list[cat_key]),
                        category = cat_key
                    ),
                    Qt.StatusTipRole
                )
                category.setEditable(False)
                for name in sorted(results[cat_key]):
                    self.win.scripts_found += 1
                    script = QStandardItem(name)
                    script.setData(
                        f": {self.win.author_list[name]}",
                        Qt.StatusTipRole
                    )
                    script.setEditable(False)
                    category.appendRow(script)
                model.appendRow(category)
            self.scr_treeview.setModel(model)
            self.scr_treeview.model().setHorizontalHeaderLabels(
                [f"  {self.win.i18n.t('gui.act_category')}"]
            )
            self.scr_treeview.expandAll()
            self.last_scr_result = self.win.i18n.t(
                self.gui_scripts_found,
                count=self.win.scripts_found
            )
            self.win.status_left.setText(
                self.last_scr_result
            )

    def get_category_results(self, pattern):
        results = {}
        self.last_scr_search = pattern
        self.win.scripts_found = 0
        for key in self.win.scripts_list.keys():
            if pattern.lower() in key:
                results[key] = self.win.scripts_list[key]
        if len(results) == 0:
            self.search_not_found()
            return False
        return results

    def search_not_found(self):
        model = self.scr_treeview.model()
        model.clear()
        result = QStandardItem(
            self.win.i18n.t(
                self.win.gui_script_not
            )
        )
        result.setData(
            self.win.i18n.t(
                self.win.gui_script_not
            ),
            Qt.StatusTipRole
        )
        result.setEditable(False)
        result.setSelectable(False)
        model.appendRow(result)
        self.scr_treeview.setModel(model)
        self.scr_treeview.model().setHorizontalHeaderLabels(
            [f"  {self.win.i18n.t('gui.search_results')}"]
        )
        self.last_scr_result = self.win.i18n.t(
            self.win.gui_script_not
        )
        self.win.status_left.setText(
            self.last_scr_result
        )

    def reset_search_results(self, pattern):
        self.last_scr_search = pattern
        if self.win.scripts_found != self.win.total_scripts and\
                len(self.last_scr_search) < 2:
            self.win.scripts_found = self.win.total_scripts
            self.load_scripts()
            self.last_scr_search = ""
            self.last_scr_result = ""
            self.win.status_left.setText(
                self.win.welcome
            )

    @Slot()
    def clear_search(self):
        if self.search_text.text() != "":
            self.search_text.setText("")
        self.last_scr_result = ""
        self.win.status_left.setText(
            self.win.welcome
        )
        self.load_scripts()