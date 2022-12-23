import sys
sys.path.append("../libs")
import i18n
import utils

class HelperNmap:

  i18n = None
  args = ""
  template = ""  
  __parent = None
  utils = utils.Utils()  

  def __init__(self,args, parent):
    self.args = args
    self.net = ""
    self.template = ""
    self.i18n = i18n
    self.__parent = parent

  def process(self):
    try:
      if self.args == "templates":
        self.show_templates()
      else:
        if self.__validateParams():
          self.utils.show_spinner(f"{self.i18n.t('help.running_scan')} {self.net}")
          self.utils.run_nmap(
            self.net,
            self.arguments,
            self.i18n.t("setup.root_user")          
          )
        else:
          pass
    except Exception as e:
      self.utils.print_traceback(e)
  
  def __validateParams(self):
    argsdic = {}
    if self.args.find('net:') != -1 and self.args.find('template:') != -1:
      if len(self.args.split(":")) == 3:
        argsdic.update({
          self.args.split(":")[0]:self.args.split(":")[1].split(" ")[0],
          self.args.split(":")[1].split(" ")[1]:self.args.split(":")[2].split(" ")[0]
          })
      elif len(self.args.split(":")) == 2:
        argsdic.update({
          self.args.split(":")[0]:self.args.split(":")[1].split(" ")[0]
        })
      else:
        pass
    else:
      self.__parent.do_help("run")
    return self.__setParams(**argsdic)

  #evaluate and list templates
  def show_templates(self):    
    self.utils.print_templates(
      [
        self.i18n.t("setup.file"),
        self.i18n.t("setup.template"),
        self.i18n.t("setup.status"),
        self.i18n.t("setup.arguments"),
        self.i18n.t("setup.wrong_template"),
        self.i18n.t("setup.total_files")
      ]
    )

  #private function to set params
  def __setParams(self,**kwargs):
    try:
      if kwargs is not None:
        if "net" in kwargs.keys() and "template" in kwargs.keys():
          net = kwargs["net"]
          arguments = kwargs["template"]
          self.net = net
          item = self.utils.get_nmap_template(arguments)          
          values = item[arguments]["arguments"]
          self.arguments = values        
          return True
        else:
          return False
      else:
        return False
    except Exception as e:      
      if "not subscriptable" in str(e):
        self.print_template_msg()
        return False

  def print_template_msg(self):
    self.utils.print(
      self.i18n.t("setup.bad_template")
    )