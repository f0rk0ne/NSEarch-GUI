#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QFont

class FavDlg(QDialog):

    i18n = None
    resources_path = None
    accept_btn, fav_label, ranking_cb = None, None, None
    saveRanking = Signal(str, int, name='saveResult')
    _ui = None
    ranking = None
    script = ''

    def __init__(self, parent):
        super(FavDlg, self).__init__(parent)
        self.resources_path = parent.resources_path
        self.i18n = parent.i18n
        self.ranking = [
            (self.i18n.t("gui.ranking_normal"), "normal.png"),
            (self.i18n.t("gui.ranking_great"), "great.png"),
            (self.i18n.t("gui.ranking_super_great"), "super-great.png")
        ]
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Script Ranking")
        self.setWindowModality(Qt.WindowModal)
        self.resize(280, 200)
        self.setMinimumSize(QSize(280, 200))
        self.setMaximumSize(QSize(280, 200))
        self.setWindowIcon(
            QIcon(f"{self.resources_path}nmap-logo-small")
        )
        self.init_layout()

    def init_layout(self):
        self.init_controls()
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(5)
        grid_layout.setObjectName(u"gridLayout")
        grid_layout.setContentsMargins(20, 0, 20, 20)
        grid_layout.addWidget(self.fav_label, 0, 0, 1, 1)
        grid_layout.addWidget(self.ranking_cb, 1, 0, 1, 1)
        grid_layout.addWidget(self.accept_btn, 2, 0, 1, 1)

    def init_controls(self):
        self.fav_label = QLabel(self)
        self.fav_label.setObjectName(u"fav_label")
        self.fav_label.setMinimumSize(QSize(0, 60))
        self.fav_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(12)
        self.fav_label.setFont(font)
        self.fav_label.setLineWidth(1)
        self.fav_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.fav_label.setWordWrap(True)

        self.ranking_cb = QComboBox(self)
        self.ranking_cb.setObjectName(u"ranking_cb")
        self.ranking_cb.setMinimumSize(QSize(65, 40))
        self.ranking_cb.setIconSize(QSize(65, 22))

        for a, b in self.ranking:
            self.ranking_cb.addItem(
                QIcon(f"{self.resources_path}{b}"),
                a
            )

        self.accept_btn = QPushButton(self)
        self.accept_btn.setObjectName(u"accept_btn")
        self.accept_btn.setMinimumSize(QSize(0, 40))
        self.accept_btn.setText(self.i18n.t("gui.accept"))
        self.accept_btn.clicked.connect(self.save_result)

    def set_label_script(self, script, ranking):
        self.script = script
        self.fav_label.setText(
            self.i18n.t(
                "gui.add_fav_msg",
                script=self.script
            )
        )
        self.ranking_cb.setCurrentIndex(ranking)

    def save_result(self):
        ranking = self.ranking_cb.currentIndex()
        self.hide()
        self.saveRanking.emit(self.script, ranking)
        self.close()
