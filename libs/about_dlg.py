import os, sys, i18n
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import uic
from traceback import print_exc
sys.path.append('..')

try:
    base, form = uic.loadUiType("ui/about.ui")
except Exception as ex:
    print_exc() & exit(0)

class AbtDlg(base, form):

  link_color = None

  def __init__(self, parent):
    super(base, self).__init__(parent)
    self.setupUi(self)
    self.setWindowModality(Qt.WindowModal)
    self.setWindowTitle(i18n.t("gui.st_developer"))
    if parent.theme == 1:
      self.link_color = "blue"
    elif parent.theme == 2:
      self.link_color = "#77d4fc"
    else:
     self.link_color = "#306981"
    self.loadLang()

  def loadLang(self):
    color_tag = "{color}"
    self.author_label.setText(f"{i18n.t('gui.act_author')} :")
    self.author_text.setText(i18n.t("gui.gui_author"))
    self.mail_label.setText(i18n.t("gui.email"))
    self.github_label.setText(i18n.t("gui.github"))
    self.web_label.setText(i18n.t("gui.web"))
    self.web_text.setText(
      self.web_text.text().replace(color_tag, self.link_color)
    )
    self.github_text.setText(
      self.github_text.text().replace(color_tag, self.link_color)
    )
    self.mail_text.setText(
      self.mail_text.text().replace(color_tag, self.link_color)
    )