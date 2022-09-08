#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import os
import re
import sys
import libs.console as console
import libs.dbmodule as dbmodule

# main action
if __name__ == '__main__':

  if not os.path.isfile(dbmodule.dbname):    
    dbmodule.init_setup()
  else:    
    dbmodule.update_app()
      
  if len( sys.argv ) == 1:
    console = console.Console()
    try:
      console.cmdloop()
    except KeyboardInterrupt:
      console.postloop()    
  else:
    if sys.argv[1] == "-g":
      import libs.ngui      