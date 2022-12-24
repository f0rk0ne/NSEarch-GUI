from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QDockWidget
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTreeView
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox

class FavoriteDock(QDockWidget):
    
    win = None
    fsearch_text = None
    fsearch_btn = None
    fclear_btn = None
    fav_treeview = None
    fav_layout = None
    script_text = "  Script"
    gui_dock_fav = "gui.dock_favorites"

    def __init__(self, parent):
        super(FavoriteDock, self).__init__(parent)
        try:
            self.win = parent
            self.setupUi()
            self.load_favorites()
            self.fav_treeview.selectionModel().currentChanged.connect(
                self.favorite_selected
            )
            self.load_lang()
        except Exception as e:
            parent.show_exception(e)            

    def setupUi(self):
        self.setObjectName("favoritedock")
        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth()
        )
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(258, 200))
        self.setMaximumSize(QSize(400, 524287))
        
        self.setFloating(False)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetClosable|
            QDockWidget.DockWidgetFeature.DockWidgetMovable|
            QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar            
        )
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea
        )
        self.setWidget(self.fav_layout)
        self.init_layout()        

    def init_layout(self):
        self.fav_layout = QWidget()
        self.fav_layout.setObjectName("fav_layout")
        fav_gridlayout = QGridLayout(self.fav_layout)
        fav_gridlayout.setObjectName("fav_gridlayout")

        self.init_search_controls()
        fav_gridlayout.addWidget(self.fsearch_text, 0, 0, 1, 1)  
        fav_gridlayout.addWidget(self.fsearch_btn, 0, 1, 1, 1)
        fav_gridlayout.addWidget(self.fclear_btn, 0, 2, 1, 1)

        self.fav_treeview = QTreeView(self.fav_layout)
        self.fav_treeview.setObjectName("fav_treeview")
        self.fav_treeview.setMinimumSize(QSize(220, 100))
        self.fav_treeview.setContextMenuPolicy(Qt.CustomContextMenu)        
        self.fav_treeview.setIconSize(QSize(55, 22))
        self.fav_treeview.setIndentation(5)
        self.fav_treeview.setSortingEnabled(True)
        self.fav_treeview.setAnimated(True)
        self.fav_treeview.sortByColumn(0, Qt.AscendingOrder)        

        self.fav_treeview.customContextMenuRequested.connect(
            self.show_fav_opts
        )

        fav_gridlayout.addWidget(self.fav_treeview, 1, 0, 1, 3)        
        self.setWidget(self.fav_layout)
        self.init_reg_exp()

    def init_search_controls(self):
        self.fsearch_text = QLineEdit(self.fav_layout)
        self.fsearch_text.setObjectName("fsearch_text")
        self.fsearch_text.setMinimumSize(QSize(0, 40))
        self.fsearch_text.textEdited.connect(
            self.fav_key_pressed
        )
        self.fsearch_text.editingFinished.connect(
            self.fav_enter_pressed
        )
        
        self.fsearch_btn = QPushButton(self.fav_layout)
        self.fsearch_btn.setObjectName("fsearch_btn")
        self.fsearch_btn.setMinimumSize(QSize(40, 40))
        self.fsearch_btn.setMaximumSize(QSize(30, 16777215))
        self.fsearch_btn.clicked.connect(
            self.init_fav_search
        )

        fsicon = QIcon()
        fsicon.addFile(
            f"{self.win.resources_path}glass.png",
            QSize(24, 24),
            QIcon.Normal,
            QIcon.Off
        )
        self.fsearch_btn.setIcon(fsicon)
        self.fsearch_btn.setIconSize(QSize(24, 24))

        self.fclear_btn = QPushButton(self.fav_layout)
        self.fclear_btn.setObjectName("fclear_btn")
        self.fclear_btn.setMinimumSize(QSize(40, 40))
        self.fclear_btn.setMaximumSize(QSize(30, 16777215))
        self.fclear_btn.clicked.connect(
            self.clear_fav_search
        )

        fcicon = QIcon()
        fcicon.addFile(
            f"{self.win.resources_path}brush.png",
            QSize(24, 24),
            QIcon.Normal,
            QIcon.Off
        )
        self.fclear_btn.setIcon(fcicon)
        self.fclear_btn.setIconSize(QSize(24, 24))

    def load_lang(self):        
        self.setWindowTitle(
            self.win.i18n.t("gui.dock_favorites")
        )
        self.fsearch_text.setPlaceholderText(
            self.win.i18n.t("gui.search_placeholder")
        )
        self.fsearch_text.setStatusTip(
            f'  {self.win.i18n.t("gui.st_search")}'
        )
        self.fsearch_btn.setStatusTip(
            f'  {self.win.i18n.t("gui.st_search_favorite")}'
        )
        self.fclear_btn.setStatusTip(
            f'  {self.win.i18n.t("gui.st_clear_fav_search")}'
        )

    def init_reg_exp(self):
        self.fsearch_text.setValidator(
            QRegularExpressionValidator(
                QRegularExpression("[A-Za-z0-9\-]{0,100}"),
                self.win
            )
        )

    def load_favorites(self):
        fmodel = self.fav_treeview.model()
        if fmodel == None:
            fmodel = QStandardItemModel(0, 1, self)
        else:
            fmodel.clear()
        if len(self.win.fav_list) > 0:
            for name in sorted(self.win.fav_list.keys()):
                fav = QStandardItem(name)
                if name in self.win.author_list.keys():
                    fav.setData(                        
                        self.win.i18n.t(
                            "gui.fav_info",
                            script = name,
                            author = self.win.author_list[name]
                        ),
                        Qt.StatusTipRole
                    )
                fav.setEditable(False)
                fav.setSizeHint(QSize(160, 25))
                fav_icon = QStandardItem(
                    self.win.get_favorite_img(
                        self.win.fav_list[name]
                    ),
                    self.win.dbm.get_ranking_text(
                        self.win.fav_list[name]
                    )
                )
                fav_icon.setSizeHint(QSize(60, 25))
                fmodel.appendRow([fav, fav_icon])             
                fmodel.setHorizontalHeaderLabels(
                    [self.script_text, "Ranking"]
                )
        else:
            fmodel.setHorizontalHeaderLabels(
                [self.script_text, "Ranking"]
            )
        self.fav_treeview.setModel(fmodel)
        self.fav_treeview.setColumnWidth(0, 160)
        self.fav_treeview.setColumnWidth(1, 60)

    def select_tab_fav(self, script):
        for f_index in range(0, self.fav_treeview.model().rowCount()):
            fav_item = self.fav_treeview.model().item(f_index, 0)
            if script in fav_item.text():
                self.fav_treeview.setCurrentIndex(fav_item.index())
                break

    @Slot(int)
    def show_fav_opts(self, pos):
        try:
            if self.fav_treeview.currentIndex().isValid():
                script = None
                if self.fav_treeview.currentIndex().column() == 0:
                    script = self.fav_treeview.model().itemFromIndex(
                        self.fav_treeview.currentIndex()
                    )
                else:
                    script = self.fav_treeview.model().item(
                        self.fav_treeview.currentIndex().row(),
                        0
                    )
                if script.text() in self.win.fav_list.keys():
                    show_menu = QMenu(self.win)
                    del_fav_act = QAction(
                        QIcon(
                            f"{self.win.resources_path}minus.png"
                        ),
                        self.win.i18n.t("gui.del_fav")
                    )
                    del_fav_act.setObjectName("del_fav")
                    del_all_fav_act = QAction(
                        QIcon(
                            f"{self.win.resources_path}minus.png"
                        ),
                        self.win.i18n.t("gui.del_all_favs")
                    )
                    del_all_fav_act.setObjectName("del_all_fav")
                    mod_fav_act = QAction(
                        QIcon(
                            f"{self.win.resources_path}update.png"
                        ),
                        self.win.i18n.t("gui.update_ranking")
                    )
                    mod_fav_act.setObjectName("mod_fav")
                    show_menu.addAction(mod_fav_act)
                    show_menu.addSeparator()
                    show_menu.addAction(del_fav_act)
                    show_menu.addSeparator()
                    show_menu.addAction(del_all_fav_act)
                    click_btn = show_menu.exec_(
                        self.sender().viewport().mapToGlobal(pos)
                    )
                    self.exec_fav_menu(click_btn, script)
        except Exception as e:
            print(e)
            self.win.show_exception(e)

    def exec_fav_menu(self, click_btn, script):
        if click_btn != None:
            if "del_fav" == click_btn.objectName():
                self.del_fav(script)
            if "mod_fav" == click_btn.objectName():
                self.mod_fav(script)
            if "del_all_fav" == click_btn.objectName():
                self.del_all_fav()

    def del_fav(self, script):
        if self.delete_gui_fav(name = script.text()):
            self.win.fav_list.pop(script.text())
            self.fav_treeview.model().removeRows(
                script.index().row(),
                1,
                QModelIndex()
            )

    def mod_fav(self, script):
        if script.text() not in self.win.fav_list.values():
            self.win.load_favorites_data()
            ranking = self.win.fav_list[script.text()]
            self.create_fav_dlg(script.text(), ranking)

    def create_fav_dlg(self, script, ranking):
        from libs.fav_dlg import FavDlg
        fav_dlg = FavDlg(self.win)
        fav_dlg.set_label_script(script = script, ranking = ranking)
        fav_dlg.saveRanking.connect(self.update_favorite)
        fav_dlg.exec()

    @Slot(str, str)
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
            if self.win.fav_list[script] != ranking:
                result, msg = self.update_gui_fav(
                    name=script,
                    ranking=ranking
                )
                if result:
                    self.win.fav_list[script] = ranking
                    item_img = self.fav_treeview.model().item(
                        sc_item.row(),
                        1
                    )
                    item_img.setText(
                        self.win.dbm.get_ranking_text(ranking)
                    )
                    item_img.setIcon(
                        self.win.get_favorite_img(ranking)
                    )
                    self.win.status_left.setText(
                        self.win.i18n.t(
                            self.gui_dock_fav
                        )
                    )
                    QMessageBox.information(
                        self,
                        self.win.i18n.t(
                            self.gui_dock_fav
                        ),
                        msg,
                        QMessageBox.Ok,
                        QMessageBox.Ok
                    )
                else:
                    self.win.show_exception(msg)
            else:
                QMessageBox.information(
                    self,
                    "Ranking",
                    self.win.i18n.t("gui.different_ranking"),
                    QMessageBox.Ok,
                    QMessageBox.Ok
                )
        except Exception as e:
            self.win.show_exception(e)
   
    def update_gui_fav(self, **kwargs):
        db = None
        try:
            db, cursor = self.win.dbm.get_connect(True)
            cursor.execute(
                "UPDATE favorites set ranking=? WHERE name=?;",
                (kwargs["ranking"], kwargs["name"])
            )
            db.commit()
            if cursor.rowcount == 1:
                cursor.close()
            return (True, self.win.i18n.t("gui.fav_updated"))
        except Exception as e:
            self.win.show_exception(e)
            return (False, "Error : " + e.args[0])
        finally:
            if db:
                db.close()
    
    def del_all_fav(self):
        if len(self.fav_treeview.selectionModel().selectedIndexes()) > 0:
            if self.delete_all_fav():
                self.fav_treeview.model().clear()
                self.fav_treeview.model().setHorizontalHeaderLabels(
                    [self.script_text, "Ranking"]
                )
                self.fav_treeview.setColumnWidth(0, 247)
                self.fav_treeview.setColumnWidth(1, 60)
                self.win.fav_list = dict()

    def delete_gui_fav(self, **kwargs):
        db = None
        try:
            db, cursor = self.win.dbm.get_connect(True)
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE name=?;",
                (kwargs["name"],)
            )
            db.commit()
            if cursor.rowcount == 1:
                QMessageBox.information(
                    self,
                    self.win.i18n.t(
                        self.gui_dock_fav
                    ),
                    self.win.i18n.t("gui.fav_deleted"),
                    QMessageBox.Ok, QMessageBox.Ok
                )
                return True
        except Exception as e:
            self.win.show_exception(e)
        finally:
            if db:
                db.close()

    def delete_all_fav(self):
        db = None
        try:
            db, cursor = self.win.dbm.get_connect(True)
            cursor = db.cursor()
            cursor.execute("DELETE FROM favorites;")
            db.commit()
            if cursor.rowcount >= 1:
                QMessageBox.information(
                    self,
                    self.win.i18n.t(self.gui_dock_fav),
                    self.win.i18n.t("gui.favs_deleted"),
                    QMessageBox.Ok, QMessageBox.Ok
                )
                return True
        except Exception as e:
            self.win.show_exception(e)
        finally:
            if db:
                db.close()

    @Slot(int, int)
    def favorite_selected(self, current, previous):
        del previous
        if self.fav_treeview.model().rowCount() > 1:
            script = None
            if current.column() == 0:
                script = self.fav_treeview.model().itemFromIndex(
                    current
                ).text()
            else:
                script = self.fav_treeview.model().item(
                    current.row(),
                    0
                ).text()
            if script in self.win.fav_list.keys():
                self.win.main_widget.create_script_tab(
                    script
                )

    @Slot()
    def init_fav_search(self):
        self.search_fav()

    def search_fav(self):
        pattern = self.fsearch_text.text()
        if len(pattern) >= 2 and self.win.last_fav_search != pattern\
                and len(self.win.fav_list) > 0:
            results = {}
            self.win.last_fav_search = pattern
            fav_found = 0
            for fav_key in self.win.fav_list.keys():
                if pattern in fav_key:
                    fav_found += 1
                    results[fav_key] = self.win.fav_list[fav_key]
            self.show_fav_results(results, fav_found)
        else:
            self.win.last_fav_search = pattern
            if self.fav_treeview.model().rowCount() < len(self.win.fav_list)\
                and len(self.win.last_fav_search) < 2:
                self.load_favorites()
                self.win.last_fav_search = ""
                self.win.last_fav_result = ""
                self.win.status_left.setText(
                    self.win.welcome
                )

    def show_fav_results(self, results, fav_count):
        fmodel = self.fav_treeview.model()
        if len(results) > 0:
            fmodel.clear()
            for fav in results.keys():
                fav_name = QStandardItem(str(fav))
                fav_name.setEditable(False)
                fav_name.setSizeHint(QSize(160, 25))
                fav_name.setData(                    
                    self.win.i18n.t(
                        "gui.fav_info",
                        script = fav,
                        author = self.win.author_list[fav]
                    ),
                    Qt.StatusTipRole
                )
                fav_icon = QStandardItem(
                    self.win.get_favorite_img(
                        results[fav]
                    ),
                    self.win.dbm.get_ranking_text(results[fav])
                )
                fav_icon.setEditable(False)
                fav_icon.setSizeHint(QSize(60, 25))
                fmodel.appendRow([fav_name, fav_icon])
            self.fav_treeview.setModel(fmodel)
            self.fav_treeview.model().setHorizontalHeaderLabels(
                [self.script_text, "Ranking"])
            self.fav_treeview.setColumnWidth(0, 160)
            self.fav_treeview.setColumnWidth(1, 60)
            self.win.last_fav_result = self.win.i18n.t(
                "gui.fav_found",
                count=fav_count
            )
            self.win.status_left.setText(
                self.win.last_fav_result
            )
        else:
            fmodel.clear()
            result = QStandardItem(
                self.win.i18n.t("gui.fav_not_found")
            )
            result.setEditable(False)
            result.setSelectable(False)
            fmodel.appendRow(result)
            self.fav_treeview.setModel(fmodel)
            self.fav_treeview.model().setHorizontalHeaderLabels(
                [f"  {self.win.i18n.t('gui.search_results')}"]
            )
            self.fav_treeview.setColumnWidth(0, 247)
            self.fav_treeview.setColumnWidth(1, 60)
            self.win.last_fav_result = self.win.i18n.t(
                "gui.fav_not_found"
            )
            self.win.status_left.setText(
                self.win.last_fav_result
            )

    @Slot()
    def fav_enter_pressed(self):
        self.search_fav()

    @Slot()
    def clear_fav_search(self):
        if self.fsearch_text.text() != "":
            self.fsearch_text.setText("")
        self.last_fav_result = ""
        self.win.status_left.setText(
            self.win.welcome
        )
        self.load_favorites()

    @Slot()
    def fav_key_pressed(self):
        if self.win.yaml_vars["searchOnKey"]:
            self.search_fav()