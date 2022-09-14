#!/usr/bin/python
#-*- coding: utf-8 -*- 
import i18n
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from traceback import print_exc

try:
    form, base = uic.loadUiType("ui/favoriteRanking.ui")
except Exception as ex:
    print_exc() & exit(0)

class FavDlg(base, form):

  saveRanking = pyqtSignal(str, int, name='saveResult')
  ranking = [ 
              (i18n.t("gui.ranking_normal"), "normal.png"),
              (i18n.t("gui.ranking_great"), "great.png"),
              (i18n.t("gui.ranking_super_great"), "super-great.png")
            ]
  script = ''

  def __init__(self, parent):
    super(base, self).__init__(parent)
    self.setupUi(self)
    self.setWindowModality(Qt.WindowModal)
    self.accept_btn.setText(i18n.t("gui.accept"))    

  def set_images(self, icon_path, icon):
    for a, b in self.ranking:      
      self.ranking_cb.addItem(
        QIcon(f"{icon_path}{b}"),
        a
      )
      self.setWindowIcon(QIcon(icon))

  def set_label_script(self, script, ranking):
    self.script = script
    self.fav_label.setText(
      i18n.t(
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
