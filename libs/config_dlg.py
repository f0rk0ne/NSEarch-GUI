#!/usr/bin/python
#-*- coding: utf-8 -*- 
import i18n
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic
from traceback import print_exc

try:
    form, base = uic.loadUiType("ui/configuration.ui")
except Exception as ex:
    print_exc() & exit(0)

class ConfDlg(base, form):

  saveResult = pyqtSignal(tuple, name='saveResult')
  lang, search_on_key, search_opt = None, None, None
  theme, show_animation, locale = None, None, None
  active, inactive = None, None
  themes = [ 
            i18n.t("gui.act_default" ),
            i18n.t("gui.act_dark" ),
            i18n.t("gui.act_light" ) 
            ]

  def __init__(self, parent):
    super(base, self).__init__(parent)
    self.setupUi(self)
    self.setWindowModality(Qt.WindowModal)
    self.setWindowTitle(i18n.t("gui.act_configuration" ) )
    self.loadLang()

  def loadLang(self):
    self.lang_group.setTitle(i18n.t("gui.menu_language" ) )
    self.search_on_group.setTitle(i18n.t("gui.act_search_on_key" ) )
    self.theme_group.setTitle(i18n.t("gui.menu_theme" ) )
    self.search_by_group.setTitle(i18n.t("gui.menu_search_opts" ) )
    self.splash_group.setTitle(i18n.t("gui.show_anim" ) )
    self.btn_accept.setText(i18n.t("gui.accept" ) )
    self.btn_cancel.setText(i18n.t("gui.cancel" ) )
    self.lang_es.setText(i18n.t("gui.act_spanish" ) )
    self.lang_en.setText(i18n.t("gui.act_english" ) )
    self.search_by_name.setText(i18n.t("gui.act_name" ) )
    self.search_by_author.setText(i18n.t("gui.act_author" ) )
    self.search_by_category.setText(i18n.t("gui.act_category" ) )
    for a in range(0, self.theme_select.count()):
      self.theme_select.setItemText(a, self.themes[a] )

  def initControls(self, data):    
    self.lang, self.search_on_key, self.search_opt,\
    self.theme, self.show_animation = data
    self.active = i18n.t("gui.active")
    self.inactive = i18n.t("gui.inactive")
    self.show_txt = i18n.t("gui.show")
    self.hide_txt = i18n.t("gui.hide")
    if self.lang == "es":
      self.lang_es.setChecked(True)
    else:
      self.lang_en.setChecked(True)
    self.search_on.setChecked(bool(self.search_on_key))
    self.search_on.setText(
      self.active if self.search_on_key else self.inactive
    )
    self.show_anim.setChecked(bool(self.show_animation))
    self.show_anim.setText(
      self.show_txt if self.show_animation else self.hide_txt
    )
    self.theme_select.setCurrentIndex(self.theme-1)
    if self.search_opt == 1:
      self.search_by_name.setChecked(True)
    elif self.search_opt == 2:
      self.search_by_author.setChecked(True)
    else:
      self.search_by_category.setChecked(True)

  def save(self):
    self.lang = 'es' if self.lang_es.isChecked() else 'en'
    self.search_on_key = self.search_on.isChecked()
    self.search_opt = self.get_search_opt()
    self.theme = self.theme_select.currentIndex()+1
    self.show_animation = self.show_anim.isChecked()    
    self.saveResult.emit((
                          self.lang, self.search_on_key,
                          self.search_opt, self.theme,
                          self.show_animation
                       ))
    self.close()

  def get_search_opt(self):
    if self.search_by_name.isChecked():
      return 1
    return 2 if self.search_by_author.isChecked() else 3

  def cancel(self):
    self.close()

  def update_text(self, checked):
    self.search_on.setText(
      self.active if checked else self.inactive
    )

  def update_anim_text(self, checked):
    self.show_anim.setText(
      self.show_txt if checked else self.hide_txt
    )
