#!/usr/bin/python
#-*- coding: utf-8 -*- 
import sys
sys.path.append("../libs")
import os
import dbmodule
import utils

class Helper:

  utils = utils.Utils()
  categories = [] 
  __result_type = 0
  __parent = None  
  i18n = dbmodule.i18n
  dbmodule = dbmodule
  ARG_NAME = "name:"
  ARG_CATEGORY = "category:"
  ARG_RANKING = "ranking"
  ARG_AUTHOR = "author:"

  def __init__(self, args="",command="", parent=None):
    self.args = args
    self.command = command
    self.__parent = parent

  # process the commands
  def process(self):
    if self.command == "search":
      self.exec_search()
    elif self.command == "addfav" and self.args:
      self.exec_addfav()
    elif self.command == "modfav" and self.args:
      self.exec_modfav()
    elif self.command == "delfav" and self.args:
      self.exec_delfav()
    elif self.command == "showfav":
      self.exec_showfav()
    elif self.command == "showcat":
      self.exec_showcat()
    elif self.command == "history":
      self.exec_history()
    else:
      self.utils.print(self.i18n.t("help.help_command_error"))

  # exec search command
  def exec_search(self):
    params = self.__searchparams()   
    if not self.args:      
      self.dbmodule.lastresults = self.dbmodule.search_all()
      self.__result_type = 1
      self.print_last_result()      
    elif not params:      
      self.__parent.do_help("search")
    else:           
      self.dbmodule.lastresults = self.dbmodule.search_by_criterial(
        **params
      )      
      self.__result_type = 1
      self.print_last_result()

  # exec add favorite command
  def exec_addfav(self):
    params = self.__addfavparams()
    if params != False:
      self.dbmodule.create_favorite(**params)
    
  # exec modify favorite command
  def exec_modfav(self):
    params = self.__modfavparams()    
    if params != False:
      self.dbmodule.update_favorite(**params)    

  # exec show favorites command
  def exec_showfav(self):
    if not self.args:
      self.dbmodule.lastresults = self.dbmodule.get_favorites()
      self.__result_type = 2
      self.print_last_result()        
    else:
      params = self.__getfavparams()
      if params != False:
        self.dbmodule.lastresults = self.dbmodule.get_favorites(
          **params
        )
        self.__result_type = 2
        self.print_last_result() 

  # exec delete favorite
  def exec_delfav(self):
    params = self.__delfavparams()
    if params != False:
      if params["name"] in self.__parent.favorites:
        self.dbmodule.delete_favorite(**params)
      else:
        self.utils.print(
          f"[-] script {self.i18n.t('setup.del_fav_error')}",
          True
        )

  # exec show categories command
  def exec_showcat(self):
    self.categories = self.dbmodule.get_categories()
    if not self.args:                     
      self.utils.print_categories(
        self.categories,
        self.i18n.t("setup.categories")
      )
      self.categories = [ f"{a}. {b}" for a,b in self.categories ]
      self.ask_scripts_cat()
    else:        
      self.category, self.dbmodule.lastresults = \
      self.dbmodule.get_scripts_cat(**self.__showcatparams())
      self.__result_type = 3
      self.print_last_result()

  # exec history command
  def exec_history(self):
    if not self.args:
      if self.utils.print_history(
        self.i18n.t("setup.not_hist")
      ):
        self.ask_history()
    else:
      if self.args == "clear":
        self.utils.clear_history(
          self.i18n.t("setup.hist_clear")
        )

  # Display ask to execute history command
  def ask_history(self):
    res = self.utils.ask(
      self.i18n.t("setup.ask_history")
    )
    if res != 0 and res <= len(self.utils.history):
      res -= 1
      self.utils.print("", True)
      if self.utils.history[res].split(' ') == 0:
        self.exec_single_hist(res)        
      else:
        self.exec_hist(res)        

  # execute command without args
  def exec_single_hist(self, index):
    self.command = self.utils.history[index]
    if self.command == "help":
      self.__parent.do_help("help")
      return False
    self.process()

  # execute command with args
  def exec_hist(self, index):
    words = self.utils.history[index].split(' ')
    self.command = words[0]
    for a in range(1, len(words)):
      self.args += f"{words[a]} "      
    self.args = self.args.replace("\n", "")
    self.args = self.args[:-1]
    if self.command == 'doc':
      self.display_doc()
    elif self.command == 'help':
      self.__parent.do_help(self.args)
    else:  
      self.process()

  # Display ask to select category
  def ask_scripts_cat(self):
    answer = self.utils.ask(
      self.i18n.t("setup.ask_category_script")
    )
    if answer > 0:
      self.category, self.dbmodule.lastresults = self.dbmodule\
      .get_scripts_cat(**{'id':str(answer)})
      if not self.utils.print_script_category(
        self.category,
        self.dbmodule.lastresults.items()
      ):
        self.utils.print(self.i18n.t("setup.category_not_found"))
      else:
        self.ask_script()

  # Display ask to select script
  def ask_script(self):
    answer = self.utils.ask(
      self.i18n.t("setup.script_help")
    )
    if answer > 0:
      if answer in self.dbmodule.lastresults.keys():        
        self.show_doc_from_ask(
          self.dbmodule.lastresults[answer]
        )
      elif answer <= self.dbmodule.get_total_scripts():        
        self.show_doc_from_ask(
          self.dbmodule.get_script_by_id(answer)
        )

  # show doc from ask
  def show_doc_from_ask(self, args):
    self.command = 'doc'
    self.args = args
    cmd_str = f"doc {self.get_script_name()}\n"    
    self.utils.append_history(cmd_str, dbmodule.hist_len)
    self.display_doc()

  # Display the last results
  def print_last_result(self):    
    if self.__result_type == 1:      
      if "author" in self.args:
        self.utils.print_author_results(
          self.dbmodule.lastresults.items(),
          self.__searchparams(),
          self.i18n.t("setup.result_for")
        )
      else:        
        self.utils.print_results(
          self.dbmodule.lastresults.items(),
          self.__searchparams(),
          self.i18n.t("setup.result_for")
        )
      if len(self.dbmodule.lastresults.items()) > 0:
        self.ask_script()
      else:
        search_text = self.i18n.t('setup.search_not_found')
        self.utils.print(
          f"[deep_sky_blue1]{search_text}[/deep_sky_blue1]",
          True
        )
    elif self.__result_type == 2:
      cols = {}
      cols['name'] = self.i18n.t("setup.name")
      cols['ranking'] = self.i18n.t("setup.ranking")      
      self.utils.print_favs(
        self.dbmodule.get_fav_formmated(),
        cols
      )
    else:
      if not self.utils.print_script_category(
        self.category,
        self.dbmodule.lastresults.items()
      ):
        cat_text = self.i18n.t('setup.category_not_found')
        self.utils.print(
          f"[deep_sky_blue1]{cat_text}[/deep_sky_blue1]",
          True
        )
      else:
        self.ask_script()

  # Display the documentation per script
  def display_doc(self):    
    try:
      script_path = f"{self.dbmodule.scripts_path}{self.get_script_name()}"      
      if not os.path.exists(script_path) and \
      not script_path.endswith(".nse"):
        script_path = f"{script_path}.nse"      
      if not os.path.exists(script_path):
        self.utils.print(self.i18n.t("setup.del_fav_error"))
        return None
      self.utils.print_doc(script_path)
    except Exception as e:      
      self.utils.print_traceback(e)

  # get script name from args
  def get_script_name(self):
    arg = 'empty'
    if type(self.args) == str:      
        arg = self.args      
    elif type(self.args) == dict:
      arg = self.args["name"]
    return arg

  # used for the autocomplete
  def resultitems(self):
    i = 0
    items = []
    for k,v in self.dbmodule.lastresults.items():
      items.insert(i,v["name"])
      i = i + 1
    return items

  # get all favorites
  def get_favorites(self):
    favs = self.dbmodule.get_favorites()
    return [favs[a]["name"] for a in favs]

  # private function to set params for search command
  def __searchparams(self):    
    if (
        self.args.find(self.ARG_NAME) != -1 or 
        self.args.find(self.ARG_CATEGORY) != -1 or
        self.args.find(self.ARG_AUTHOR) != -1
      ):      
      return self.__set_params()
    elif len(self.args.split(':')) == 1 and len(self.args.split(" ")) == 0:
      self.args = f"{self.ARG_NAME}{self.args}"      
      return self.__set_params()
    else:      
      return False

  # private function to set params for modfav command
  def __getfavparams(self):
    if self.args.find(self.ARG_NAME) != -1 or\
      self.args.find(self.ARG_RANKING) != -1:
      return self.__set_params()    
    else:
      self.args = f"{self.ARG_NAME}{self.args}"
      return self.__set_params()

  # private function to set params for addfav command
  def __addfavparams(self):
    if self.args.find(self.ARG_NAME) != -1:
      return self.__set_params()
    self.__parent.do_help("addfav")
    return False

  # private function to set params for delfav command
  def __delfavparams(self):
    if self.args.find(self.ARG_NAME) != -1:
      return self.__set_params()
    else:
      self.args = f"{self.ARG_NAME}{self.args}"      
      return self.__set_params()

  # private function to set params for modfav command
  def __modfavparams(self):
    if self.args.find(self.ARG_NAME) != -1 and\
    (self.args.find('newname:') != -1 or\
    self.args.find('newranking:') != -1):
      return self.__set_params()
    else:
      self.__parent.do_help("modfav")
      return False    

  #private function to set params for showcat command
  def __showcatparams(self):    
    if self.args.find(self.ARG_NAME) != -1 or self.args.find('id:') != -1:
      return self.__set_params()
    elif self.args.isdigit():
      self.args = f"id:{self.args}"
      return self.__set_params()
    elif len(self.args) > 1:
      self.args = f"{self.ARG_NAME}{self.args}"
      return self.__set_params()

  # Set Params validations
  def __set_params(self):
    argsdic = {}    
    if len(self.args.split(":")) >= 4:
      argsdic.update(
        {
        self.args.split(":")[0]:
          self.args.split(":")[1].split(" ")[0],
        self.args.split(":")[1].split(" ")[1]:
          self.args.split(":")[2].split(" ")[0],
        self.args.split(":")[2].split(" ")[1]:
          self.args.split(":")[3].split(" ")[0]
        }
      )
    elif len(self.args.split(":")) == 3:
      argsdic.update({
        self.args.split(":")[0]:
          self.args.split(":")[1].split(" ")[0],
        self.args.split(":")[1].split(" ")[1]:
          self.args.split(":")[2].split(" ")[0]
        }
      )
    elif len(self.args.split(":")) == 2:
      argsdic.update(
        {
          self.args.split(":")[0]:
            self.args.split(":")[1].split(" ")[0]
        }
      )
    else:      
      self.utils.print(self.i18n.t("setup.bad_params"))
      return False
    if "" in argsdic.values():
      self.utils.print(self.i18n.t("setup.bad_params"))
      return False
    return argsdic
