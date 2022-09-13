## console.py
#!/usr/bin/python
#-*- coding: utf-8 -*- 
import sys
sys.path.append("../libs")
import cmd
import os
import readline
from helper import *

class Console(cmd.Cmd):

  utils = utils.Utils()  
  __helper = Helper
  _history = ''  
  or_str = ""
  favorites = []
  scripts = []
  last_command = ''
  last_args = ''  
  great = ''  
  command_help = None  

  commands = [ 
              'help', 'showfav', 'addfav',
              'delfav', 'modfav', 'showcat',
              'search', 'doc', 'history'
            ]
  
  # autocomplete definition list
  search_commands = [ 'name', 'category', 'help', 'author']
  showfav_options = ['name', 'ranking', 'help']
  showcat_options = ['name', 'id']

  HELP_USAGE = "help.help_usage"
  HELP_FAV_NAME =  "help.help_fav_name"
  HELP_FAV_RANKING = "help.help_fav_ranking"  

  def __init__(self):    
    cmd.Cmd.__init__(self)    
    self.utils.print(None, True)
    self.prompt = "nsearch🐉️> "        
    self.doc_header = self.__helper.i18n.t("help.doc_header")
    self.misc_header = self.__helper.i18n.t("help.misc_header")
    self.undoc_header = self.__helper.i18n.t("help.undoc_header")
    self.or_str = self.__helper.i18n.t("help.help_or")
    self.great = self.__helper.i18n.t("help.great")
    self.ruler = '='    
    self.command_help = {}    
    self.loadHelp()
    self.__helper(parent=self)
    self.utils.get_history()
    self.get_favorites()
    self.get_scripts()

  # get favorites script name
  def get_favorites(self):
    if len(self.favorites) == 0:
      self.favorites = []
      tmp = dbmodule.get_favorites()
      for a in tmp:
        self.favorites.append(tmp[a]["name"])

  # get scripts name list
  def get_scripts(self):
    if len(self.scripts) == 0:
      self.scripts = dbmodule.get_scripts()

  def loadHelp(self):
    self.getHelpText()
    self.help_showfav()
    self.help_addfav()
    self.help_modfav()
    self.help_delfav()
    self.help_doc()
    self.help_last()
    self.help_search()    
    self.help_showcat()
    self.help_history()
    self.help_clear()
    
  # Command definitions ##
  def do_history(self, args):
    """Print a list of commands that have been entered"""    
    hist = self.__helper(args=args,command='history', parent=self)
    hist.process()

  def help_history(self):        
    usage = f"history {self.or_str} history clear"
    self.command_help["history"] = {
      "history": self.__helper.i18n.t("help.help_history"),
      "clear": self.__helper.i18n.t("help.help_history_clear"),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }

  def complete_history(self, text, line, begidx, endidx):
    del text, line, begidx, endidx
    return ["clear"]

  def do_exit(self, args):
    """Exits from the console"""
    del args
    return -1

  def do_help(self, args):
    """Get help on commands
       'help' or '?' with no arguments prints a list of 
       commands for which help is available
       'help <command>' or '? <command>' gives help on <command>
    """
    # The only reason to define this method is 
    # for the help text in the doc string    
    if args == "":
      args = "help"    
    self.utils.print_help(
      self.doc_header if args == "help" else self.misc_header,
      args,
      self.command_help
    )    

  # add commands help
  def getHelpText(self):
    command_str = {}
    for a in self.commands:
      if a != "help":
        command_str[a] = self.__helper.i18n.t(f"help.help_{a}")
    self.command_help["help"] = command_str    

  # Command definitions to support Cmd object functionality ##
  def do_EOF(self, args):
    """Exit on system end of file character"""
    return self.do_exit(args)

  # Override methods in Cmd object ##
  def preloop(self):
    """Initialization before prompting user for commands.
       Despite the claims in the Cmd documentation,
       Cmd.preloop() is not a stub.
    """
    cmd.Cmd.preloop(self)   ## sets up command completion    
    self._locals  = {}      ## Initialize execution namespace for user
    self._globals = {}
    old_delims = readline.get_completer_delims()
    readline.set_completer_delims(old_delims.replace('-', ''))

  def postloop(self):
    """Take care of any unfinished business.
       Despite the claims in the Cmd documentation,
       Cmd.postloop() is not a stub.
    """
    cmd.Cmd.postloop(self)   ## Clean up command completion
    self.utils.print_exit(
      self.__helper.i18n.t("setup.exit")
    )

  def precmd(self, line):
    """ This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
    """
    self.append_history(line)
    return line

  def append_history(self, line):    
    for a in self.commands:
      if line.startswith(a):       
        self.utils.append_history(
          line.strip(),
          self.__helper.dbmodule.hist_len
        )
        break

  def postcmd(self, stop, line):
    """If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    """
    del line
    return stop

  def emptyline(self):
    """Do nothing on empty input line"""
    pass

  def do_clear(self, args):
    """ Clear the shell """
    os.system("clear")
    del args
    self.utils.print(None, True)

  def help_clear(self):
    self.command_help["clear"] = {
      "clear": self.__helper.i18n.t("help.help_clear")
    }

  def do_search(self, args):
    """ Search """
    if not args:
      self.help_search()
      self.do_help("search")
      return False
    search = self.__helper( args,"search", parent=self)
    search.process()
    self.last_command = 'search'
    self.last_args = args

  def complete_search(self, text, line, begidx, endidx):
    del line, begidx, endidx
    if not text:
      commands = self.search_commands[:]
    else:
      commands = [f for f in self.search_commands if f.startswith(text)]
    return commands

  def help_search(self):    
    usage = ''.join(
      [
        f'search name:http {self.or_str} search http\n',
        'search category:exploit\n',
        'search author:fyodor\n',
        'search name:http category:exploit author:fyodor\n'
      ]
    )    
    self.command_help["search"] = {
      "search": self.__helper.i18n.t( "help.help_search" ),
      "name": self.__helper.i18n.t("help.help_search_name"),
      "category": self.__helper.i18n.t("help.help_search_category"),
      "author": self.__helper.i18n.t("help.help_search_author"),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }    

  def do_doc(self, args):
    """ Display Script Documentaion"""
    if not args:
      self.help_doc()
      self.do_help("doc")
      return False
    doc = self.__helper(args, parent=self)    
    doc.display_doc()
    self.last_command = 'doc'
    self.last_args = args

  def help_doc(self):
    self.command_help["doc"] = {
      "doc": self.__helper.i18n.t("help.help_doc"),
      self.__helper.i18n.t(self.HELP_USAGE): 
        self.__helper.i18n.t("help.help_doc_exmp")
    }

  def complete_doc(self, text, line, begidx, endidx):
    """ Autocomplete over the last result """
    del line, begidx, endidx        
    self.get_scripts()
    return [i for i in self.scripts if i.startswith(text)]

  def do_last(self,args):
    """ last help"""
    try:      
      if self.last_command:
        search = self.__helper(
          args = self.last_args,
          command = self.last_command,
          parent = self
        )
        if self.last_command == 'doc':
          search.display_doc()
        else:
          search.process()
    except Exception as e:
      self.utils.print_traceback(e)
      search = self.__helper(args,"showfav", parent=self)
      search.process()

  def help_last(self):
    self.command_help["last"] = { 
      "last": self.__helper.i18n.t("help.help_last")
    }

  # handler fav actions
  def do_addfav(self,args):
    if not args:
      self.help_addfav()
      self.do_help("addfav")
      return False
    helper = self.__helper(args,"addfav", parent=self)
    helper.process()
    self.favorites = []
    self.get_favorites()

  def help_addfav(self):    
    usage = f'addfav name:http-ls ranking:{self.great}\n'    
    usage += f'{self.or_str} addfav name:http-ls'
    self.command_help["addfav"] = {
      "addfav": self.__helper.i18n.t("help.help_addfav"),
      "name": self.__helper.i18n.t(self.HELP_FAV_NAME),
      "ranking": self.__helper.i18n.t(self.HELP_FAV_RANKING),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }

  def complete_addfav(self, text, line, begidx, endidx):
    """ Autocomplete over the last result """
    del line, begidx, endidx
    self.get_scripts()
    return [i for i in self.scripts if i.startswith(text)]

  def do_delfav(self,args):
    if not args:
      self.help_delfav()
      self.do_help("delfav")
      return False
    search = self.__helper(args,"delfav", parent=self)
    search.process()
    self.favorites = []
    self.get_favorites()

  def help_delfav(self):
    usage = 'delfav name:http-ls '
    usage += f"{self.or_str} delfav http-ls" 
    self.command_help["delfav"] = {
      "delfav": self.__helper.i18n.t("help.help_delfav"),
      "name": self.__helper.i18n.t(self.HELP_FAV_NAME),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }

  def complete_delfav(self, text, line, begidx, endidx):
    """ Autocomplete over the last result """
    del line, begidx, endidx
    self.get_favorites()
    return [i for i in self.favorites if i.startswith(text)]

  def do_modfav(self,args):
    if not args:
      self.help_modfav()
      self.do_help("modfav")
      return False
    search = self.__helper(args,"modfav", parent=self)
    search.process()
    self.favorites = []
    self.get_favorites()

  def help_modfav(self):
    usage = f'modfav name:http newname:http-new-script newranking:{self.great}'    
    self.command_help["modfav"] = { 
      "modfav": self.__helper.i18n.t("help.help_showfav"),
      "name": self.__helper.i18n.t("help.help_search_name"),
      "newname": self.__helper.i18n.t(self.HELP_FAV_NAME),
      "newranking": self.__helper.i18n.t(self.HELP_FAV_RANKING),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }

  def complete_modfav(self, text, line, begidx, endidx):
    """ Autocomplete over the last result """
    del line, begidx, endidx
    self.get_favorites()
    return [i for i in self.favorites if i.startswith(text)]

  def do_showfav(self,args):
    search = self.__helper(args,"showfav", parent=self)
    search.process()
    self.last_command = 'showfav'
    self.last_args = args

  def help_showfav(self):
    usage = ''.join(
      [      
        f'showfav name:http-ls {self.or_str} showfav http-ls\n',
        f'showfav ranking:{self.great}\n',
        f'showfav name:http ranking:{self.great}\n'
      ]
    )
    self.command_help["showfav"] = { 
      "showfav": self.__helper.i18n.t("help.help_showfav"),
      "name": self.__helper.i18n.t(self.HELP_FAV_NAME),
      "ranking": self.__helper.i18n.t(self.HELP_FAV_RANKING),
      self.__helper.i18n.t(self.HELP_USAGE): usage 
    }

  def complete_showfav(self, text, line, begidx, endidx):
    del line, begidx, endidx
    if not text:
      commands = self.showfav_options[:]
    else:
      commands = [ 
        f for f in self.showfav_options
        if f.startswith(text)
      ]
    return commands

  def do_showcat(self, args):
    show  = self.__helper(args, "showcat", parent=self)
    show.process()
    self.last_command = 'showcat'
    self.last_args = args

  def complete_showcat(self, text, line, begidx, endidx):
    del line, begidx, endidx        
    if not text:
      commands = self.showcat_options[:]
    else:
      commands = [
        f for f in self.showcat_options
        if f.startswith(text)
      ]
    return commands    
  
  def help_showcat(self):    
    usage = ''.join(
      [
        'showcat\n',
        f'showcat id:1 {self.or_str} showcat 1\n',
        f'showcat name:auth {self.or_str} showcat auth'
      ]
    )
    self.command_help['showcat'] = { 
      'showcat' : self.__helper.i18n.t("help.help_showcat"),
      'id': self.__helper.i18n.t("help.help_showcat_id"),
      'name': self.__helper.i18n.t(self.HELP_FAV_NAME),
      self.__helper.i18n.t(self.HELP_USAGE): usage
    }
  
  def default(self, line):
    """Called on an input line when the command prefix is not recognized.
       In that case we show help.
    """
    del line
    try:        
        cmd.Cmd.do_help(self, "")
    except Exception as e:
      self.utils.print_traceback(e)
      self.utils.print(e.__class__, ":", e )
