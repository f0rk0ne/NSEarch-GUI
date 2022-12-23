#!/usr/bin/python
#-*- coding: utf-8 -*- 
from PySide6.QtCore import Qt 
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLayout 
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon

class AbtDlg(QDialog):
  
  i18n = None
  theme = None
  link_color = None
  sizePolicy = None
  font_bold = None
  resources_path = None
  logo, dots, version_text = None, None, None
  author_label, dots, author_text = None, None, None
  mail_label, dots_2, mail_text = None, None, None
  github_label, dots_3, github_text = None, None, None
  web_label, dots_4, web_text = None, None, None

  def __init__(self, parent):
    super(AbtDlg, self).__init__(parent)    
    self.theme = parent.yaml_vars["theme"]
    self.i18n = parent.i18n
    self.resources_path = parent.resources_path
    self.setupUi()
  
  def setupUi(self):    
    self.setObjectName(u"AbtDlg")    
    self.resize(680, 670)
    self.setWindowModality(Qt.ApplicationModal)
    self.setModal(True)    
    self.setMinimumSize(QSize(680, 670))
    self.setMaximumSize(QSize(680, 670))
    self.setContextMenuPolicy(Qt.NoContextMenu)

    self.sizePolicy = QSizePolicy(
      QSizePolicy.Maximum, QSizePolicy.Maximum
    )
    self.sizePolicy.setHorizontalStretch(1)
    self.sizePolicy.setVerticalStretch(1)
    self.setSizePolicy(self.sizePolicy)
    self.setWindowIcon(
      QIcon(f"{self.resources_path}nmap-logo-small")
    )
        
    self.font_bold = QFont()
    self.font_bold.setBold(True)
    self.initUi()

  def initUi(self):
    self.init_theme_color()
    self.init_controls()
    self.loadLang()
    gridLayout = QGridLayout(self)
    gridLayout.setObjectName(u"gridLayout")
    gridLayout.setSizeConstraint(QLayout.SetFixedSize)
    gridLayout.setHorizontalSpacing(0)
    gridLayout.setVerticalSpacing(10)
    gridLayout.setContentsMargins(30, 30, 30, 30)

    gridLayout.addWidget(self.logo, 0, 1, 1, 4)
    gridLayout.addWidget(self.version_text, 1, 1, 1, 4)
    gridLayout.addWidget(self.author_label, 2, 1, 1, 1)
    gridLayout.addWidget(self.dots, 2, 2, 1, 1)
    gridLayout.addWidget(self.author_text, 2, 3, 1, 1)
    gridLayout.addWidget(self.mail_label, 3, 1, 1 ,1)
    gridLayout.addWidget(self.dots_2, 3, 2, 1, 1)
    gridLayout.addWidget(self.mail_text, 3, 3, 1, 1)
    gridLayout.addWidget(self.github_label, 4, 1, 1, 1)
    gridLayout.addWidget(self.dots_3, 4, 2, 1, 1)
    gridLayout.addWidget(self.github_text, 4, 3, 1, 1)
    gridLayout.addWidget(self.web_label, 5, 1, 1, 1)
    gridLayout.addWidget(self.dots_4, 5, 2, 1, 1)
    gridLayout.addWidget(self.web_text, 5, 3, 1, 1)
    self.setLayout(gridLayout)

  def init_controls(self):
    self.logo = QLabel(self)
    self.logo.setObjectName(u"logo")
    self.logo.setMinimumSize(QSize(300, 120))
    self.logo.setPixmap(
      QPixmap(f"{self.resources_path}about.png")
    )
    self.logo.setScaledContents(False)
    self.logo.setAlignment(Qt.AlignCenter)
    self.logo.setMargin(0)

    self.version_text = QLabel(self)
    self.version_text.setObjectName(u"version_text")
    self.version_text.setMinimumSize(QSize(0, 30))
    self.version_text.setMaximumSize(QSize(16777215, 40))
    font = QFont()
    font.setPointSize(15)
    font.setBold(True)
    self.version_text.setFont(font)
    self.version_text.setAlignment(Qt.AlignCenter)
    self.init_author_controls()  

  def init_author_controls(self):
    self.author_label = QLabel(self)
    self.author_label.setObjectName(u"author_label")
    self.author_label.setMinimumSize(QSize(90, 0))
    self.author_label.setMaximumSize(QSize(80, 16777215))
    self.author_label.setTextInteractionFlags(Qt.NoTextInteraction)
    self.author_label.setFont(self.font_bold)

    self.dots = QLabel(self)
    self.dots.setObjectName(u"dots")
    self.dots.setMinimumSize(QSize(20, 0))
    self.dots.setMaximumSize(QSize(20, 16777215))    
    self.dots.setAlignment(
      Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter
    )
    self.dots.setFont(self.font_bold)
    self.dots.setText(":")
    
    self.author_text = QLabel(self)
    self.author_text.setObjectName(u"author_text")        
    self.author_text.setSizePolicy(self.sizePolicy)
    self.author_text.setMinimumSize(QSize(180, 0))
    self.author_text.setMaximumSize(QSize(16777215, 31))
    self.init_mail_controls()

  def init_mail_controls(self):
    self.mail_label = QLabel(self)
    self.mail_label.setObjectName(u"mail_label")
    self.mail_label.setMinimumSize(QSize(90, 0))
    self.mail_label.setMaximumSize(QSize(80, 31))
    self.mail_label.setFont(self.font_bold)
    self.mail_label.setTextInteractionFlags(Qt.NoTextInteraction)

    self.dots_2 = QLabel(self)
    self.dots_2.setObjectName(u"self.dots_2")
    self.dots_2.setFont(self.font_bold)
    self.dots_2.setText(":")
    self.dots_2.setMinimumSize(QSize(20, 0))
    self.dots_2.setMaximumSize(QSize(20, 16777215))    
    self.dots_2.setAlignment(
      Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter
    )
    
    self.mail_text = QLabel(self)
    self.mail_text.setObjectName(u"mail_text")        
    self.mail_text.setSizePolicy(self.sizePolicy)          
    self.mail_text.setText(
      u'<a href="mailto:ktools2017@gmail.com" style=\
        "text-decoration:none;"><span style="color:{color};">\
        ktools2017@gmail.com</span></a>'
    )
    self.mail_text.setTextFormat(Qt.RichText)
    self.mail_text.setOpenExternalLinks(True)
    self.mail_text.setTextInteractionFlags(
      Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse
    )
    self.init_git_controls()

  def init_git_controls(self):
    self.github_label = QLabel(self)
    self.github_label.setObjectName(u"github_label")
    self.github_label.setMinimumSize(QSize(90, 0))
    self.github_label.setMaximumSize(QSize(80, 31))    
    self.github_label.setFont(self.font_bold)
    self.github_label.setStyleSheet(u"")
    self.github_label.setTextInteractionFlags(
      Qt.NoTextInteraction
    )

    self.dots_3 = QLabel(self)
    self.dots_3.setObjectName(u"dots_3")
    self.dots_3.setText(":")
    self.dots_3.setMinimumSize(QSize(20, 0))
    self.dots_3.setMaximumSize(QSize(20, 16777215))
    self.dots_3.setFont(self.font_bold)
    self.dots_3.setAlignment(
      Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter
    )

    self.github_text = QLabel(self)
    self.github_text.setObjectName(u"github_text")        
    self.github_text.setSizePolicy(self.sizePolicy)    
    self.github_text.setText(
      u'<a href="https://github.com/f0rk0ne" style=\
      "text-decoration:none;"><span style="color:{color};">\
      https://github.com/f0rk0ne</span></a>'
    )
    self.github_text.setTextFormat(Qt.RichText)
    self.github_text.setOpenExternalLinks(True)
    self.github_text.setTextInteractionFlags(
      Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse
    )
    self.init_web_controls()

  def init_web_controls(self):
    self.web_label = QLabel(self)
    self.web_label.setObjectName(u"web_label")
    self.web_label.setMinimumSize(QSize(90, 0))
    self.web_label.setMaximumSize(QSize(80, 31))
    self.web_label.setFont(self.font_bold)
    self.web_label.setStyleSheet(u"")
    self.web_label.setTextInteractionFlags(Qt.NoTextInteraction)

    self.dots_4 = QLabel(self)
    self.dots_4.setObjectName(u"dots_4")
    self.dots_4.setText(":")
    self.dots_4.setMinimumSize(QSize(20, 0))
    self.dots_4.setMaximumSize(QSize(20, 16777215))
    self.dots_4.setFont(self.font_bold)
    self.dots_4.setAlignment(
      Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter
    )

    self.web_text = QLabel(self)
    self.web_text.setObjectName(u"web_text")
    self.web_text.setSizePolicy(self.sizePolicy)
    self.web_text.setTextFormat(Qt.RichText)
    self.web_text.setOpenExternalLinks(True)
    self.web_text.setTextInteractionFlags(
      Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse
    )

  def init_theme_color(self):
    if self.theme == 1:
      self.link_color = "blue"
    elif self.theme == 2:
      self.link_color = "#77d4fc"
    else:
     self.link_color = "#306981"     

  def loadLang(self):
    color_tag = "{color}"
    self.setWindowTitle(self.i18n.t("gui.act_about"))
    self.version_text.setText(self.i18n.t("gui.version"))
    self.author_label.setText(self.i18n.t('gui.act_author'))
    self.author_text.setText(self.i18n.t("gui.gui_author"))
    self.mail_label.setText(self.i18n.t("gui.email"))
    self.github_label.setText(self.i18n.t("gui.github"))
    self.web_label.setText(self.i18n.t("gui.web"))    
    web_link = self.i18n.t("gui.web_link")
    self.web_text.setText(
      f'<a href="{web_link}" style="text-decoration:none;">\
      <span style="color:{self.link_color};">{web_link}</span></a>'
    )     
    self.github_text.setText(
      self.github_text.text().replace(color_tag, self.link_color)
    )
    self.mail_text.setText(
      self.mail_text.text().replace(color_tag, self.link_color)
    )