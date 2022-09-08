import os, sys, i18n
from PyQt5.QtWidgets import QDialog, QLabel, QCheckBox, QComboBox, QPushButton, QRadioButton, qApp
from PyQt5.QtCore import Qt, QCoreApplication, QLocale, pyqtSignal
from PyQt5 import uic
from traceback import print_exc

try:
    form, base = uic.loadUiType("ui/favoriteRanking.ui")
except Exception as ex:
    print_exc() & exit(0)

class FavDlg(base, form):

  saveRanking = pyqtSignal(str, int, name='saveResult')
  ranking = [ 
              i18n.t("gui.ranking_normal"),
              i18n.t("gui.ranking_great"),
              i18n.t("gui.ranking_super_great") 
            ]
  script = ''

  def __init__(self, parent):
    super(base, self).__init__(parent)
    self.setupUi(self)
    self.setWindowModality(Qt.WindowModal)
    self.accept_btn.setText(i18n.t("gui.accept"))
    for a in range(0, self.ranking_cb.count()):
      self.ranking_cb.setItemText(a, self.ranking[a])

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