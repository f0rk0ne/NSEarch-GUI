#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import sys
sys.path.append("libs")
import os
import dbmodule

# main action
if __name__ == '__main__':
  
  dbmodule.check_db()
        
  if len(sys.argv) == 2 and sys.argv[1] == "-g":
      import libs.ngui
  else:
    import console
    console = console.Console()
    try:
      console.cmdloop()
    except KeyboardInterrupt:
      console.postloop()