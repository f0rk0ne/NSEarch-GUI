#!/usr/bin/python
#-*- coding: utf-8 -*- 
import dbm
import os
import hashlib
import re
from rich.console import Console
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns
from rich.tree import Tree
from rich.spinner import Spinner
from rich.live import Live
import html
import time
import libs.dbmodule as dbmodule

class Utils:

  console = Console()
  banner = " _   _  _____  _____                     _\n"
  banner += "| \ | |/  ___||  ___|                   | |\n"
  banner += "|  \| |\ `--. | |__    __ _  _ __   ___ | |__\n"
  banner += "| . ` | `--. \|  __|  / _` || '__| / __|| '_  |\n"
  banner += "| |\  |/\__/ /| |___ | (_| || |   | (__ | | | |\n"
  banner += "\_| \_/\____/ \____/  \__,_||_|    \___||_| |_|\n"

  footer = "Version 1.0 https://bit.ly/3Rv9FNL @jjtibaquira\n"
  footer += "Email:🙎jko@dragonjar.org | 🙎www.dragonjar.org"
  lastcommand, lastargs = '', '' 
  history, __hist_file = [], 'history'
  spinner_text, __debug = '', True
  conf_keys = ["config", "scriptsPath", "filePath",
               "fileBackup", "scriptdb", "categories",
               "checksum", "searchOnKey", "searchOpt",
               "theme", "splashAnim", "lang", "histLen"
               ]
  COLOR_1 = "bright_red"
  BOLD_COLOR_1 = "bold bright_red"
  COLOR_2 = "deep_sky_blue1"
  BOLD_COLOR_2 = f"bold deep_sky_blue1"
  COLOR_3 = "indian_red"  

  def __init__(self):    
    self.console = Console()

  def print(self, renderable, print_header=False):
    render = Panel(renderable, box.MINIMAL) if "str"\
    in str(type(renderable)) else renderable
    if print_header:
      self.console.clear()
      if render != None:        
        self.console.print(Group(self.get_banner(), render))
      else:
        self.console.print(self.get_banner())
    elif render != None:
      self.console.print(render)

  def get_banner(self):
    table = Table(
      expand = True,
      show_lines = True,
      show_header = False,
      border_style = self.COLOR_1,
      box = box.ROUNDED,
      pad_edge = True,
      padding=(0,0)
   )
    table.add_column()
    table.add_row(
      Align.center(
        Text(
          self.banner,
          style=self.COLOR_2
       )
     )
   )
    table.add_row(
      Align.center(
        Text(
          self.footer, style='white'
       )
     )
   )
    return Panel(table,padding=(0,0),box=box.MINIMAL)

  def print_exit(self, text):
    self.print(Text(f'{text} ... ', style=self.COLOR_3))
    self.save_history()

  def show_spinner(self, text):
    self.print(
      Padding(
        Text(
          self.spinner_text,
          style = self.COLOR_2
       ),
        pad=[0,1]
     ),
      True
   )
    with Live(
      Panel(
        Spinner(
          "aesthetic",
          text = text,
          style = self.COLOR_1),
          padding=[0,1],
          box = box.MINIMAL
       ),
        console = self.console 
   ) as live:      
      time.sleep(.48)
      live.stop()

  def get_result_table(self, show_expand = True):
    table = Table.grid(expand=show_expand, padding=(1,2), pad_edge=True)
    table.add_column()
    table.add_column()
    return table

  def print_results(self, items, params, result_text):    
    sc = [ 
      f"[{self.COLOR_2}]{a[0]}.[/{self.COLOR_2}] {html.escape(a[1]['name'])}"
      for a in items 
    ]    
    title = f"[{self.COLOR_1}]{result_text}[/{self.COLOR_1}]"
    for a in params.keys():
      title += f"[{self.COLOR_2}]{a}:[/{self.COLOR_2}][white]{params[a]}[/white] "
    if len(sc) >= 1:
      self.print(
        Group(       
          Padding(
            Align.center(
              title
           ),
            (0,1)
         ),
          Panel(
            Columns(
              sc,
              expand = True,
              equal = True,
              padding = (1,2) 
           ),
            padding=(1,2),
            box=box.MINIMAL 
         )
       ),
       True
     )
      return True
    else:
      return False

  def print_author_results(self, items, params, result_text):      
    title = f'[{self.COLOR_1}]{result_text}[/{self.COLOR_1}]'
    for a in params.keys():
      search_by = f"[{self.COLOR_2}]{a}:[/{self.COLOR_2}]"
      title += f"{search_by}[white]{params[a]}[/white] "
    table = self.get_result_table()
    table.add_row(
      Text(
        'Name',
        style = self.BOLD_COLOR_2
      ),
      Text(
        'Author',
        style = self.BOLD_COLOR_2
      )
    )
    for a in items:      
      script = html.escape(a[1]['name'].replace('.nse',''))
      script = f"[{self.COLOR_2}]{str(a[0])}.[/{self.COLOR_2}] {script}"
      author = a[1]['author'].replace(
        params['author'],
        f"[bold]{params['author']}[/bold]"
      ).replace(
        params['author'].title(),
        f"[bold]{params['author'].title()}[/bold]"
      )
      table.add_row(
        script,
        re.sub(
          '[\<\>\{\}]', '', author
        ) 
      )
    self.print(Group(Align.center(title), table), True)

  def get_ranking(self, ranking):
    if ranking == 0:
      return '[yellow]⭐️[/yellow]'
    if ranking == 1:
      return '[yellow]⭐️⭐️[/yellow]'
    if ranking == 2:
      return '[yellow]⭐️⭐️⭐️[/yellow]'

  def print_favs(self, items, cols):
    table = self.get_result_table(False)
    table.add_column()
    table.add_row(
      Text(
        cols['name'],
        style = self.BOLD_COLOR_2
     ),
      Text(
        cols['ranking'],
        style = self.BOLD_COLOR_2
     ),
      ''
   )
    for key, value in items:
      table.add_row(
        value['name'],
        dbmodule.get_ranking_text(value['ranking']),
        self.get_ranking(value['ranking'])
     )
    self.print(table, True)

  def get_script_data(self, script_path):    
    script_path = f"{script_path}.nse" \
    if not script_path.endswith(".nse") else script_path
    script_file = open(script_path, 'r').read()
    author = self.get_author(script_file)
    description = self.get_description(script_file)
    script_license = self.get_license(script_file)
    categories = self.get_categories(script_file)
    usage = self.get_usage(script_file)
    return (
            self.get_description_formatted(description),
            usage, f"{author} ",
            script_license, categories
           )

  # get splash image
  def get_splash_img(self, show_anim):
    if show_anim:
      return 'splash.gif'
    return 'splash.png'

  # get home image
  def get_home_img(self, show_anim):
    if show_anim:
      return 'logo.gif'
    return 'nmap-logo.png'

  # get usage
  def get_usage(self, data):
    lindex = 0
    try:
      lindex = data.index("@usage")
    except ValueError as e:
      del e
      return ''
    return "".join([
                      f"{line}\n"
                      for line in data[lindex:].splitlines()
                      if line.startswith("--")
                    ])      

  # get categories
  def get_categories(self, data):
    lindex = 0
    try:
      lindex = data.index("categories =") + len("categories =") 
    except ValueError as e:
      del e
      lindex = data.index("categories") + len("categories")
    categories = data[lindex:]
    if "{" in categories:
      categories = categories.split("{")[1].split("}")[0]     
    return re.sub(
                  '^\s','',
                  re.sub(r'[\"\{\}\s]', '', categories)
                 ).replace(',', ', ')

  # get license
  def get_license(self, data):
    lindex = 0    
    try:
      lindex = data.index("license =") + len("license =")
    except ValueError as e:
      del e
      try:
        lindex = data.index("license") + len("license")
      except ValueError as e:
        del e
        return ""
    script_license = data[lindex:].split("\n")[0]
    return re.sub(
                  '[\"|\;]', '',
                  re.sub(r'^\s', '', script_license)
                 )

  # get description
  def get_description(self, data):
    lindex = 0
    try:
      lindex = data.index("description =") + len("description =")
    except ValueError as e:
      del e
      try:
        lindex = data.index("description=") + len("description=")    
      except ValueError as e:
        del e
        return ""
    description = data[lindex:]      
    if "[[" in description:
      description = description.split("[[")[1].split("]]")[0]
    else:
      description = description.split('"')[0]
    return description

  # get author name
  def get_author(self, data):
    lindex = 0
    try:
      lindex = data.index("author =") + len("author =")
    except ValueError as e:
      del e
      try:
        lindex = data.index("-- @author") + len("-- @author")
      except ValueError as e:
        del e
        return ""
    author = data[lindex:].split("\n")[0]
    if author.endswith("{"):
      author = data[lindex:].split("}")[0]
    author = re.sub(r'[\'\"\{\}\<\>\-\=\@\(\)\;\[\]]','', author)
    return re.sub(r'^\s', '',author).strip("\n")

  # print script help
  def print_doc(self, script_path):    
    description, usage, author, script_license, categories = \
    self.get_script_data(script_path)
    table = Table.grid(expand = True, padding = (1,2), pad_edge = True)
    table.add_column()
    sc = script_path.split('/')[-1].replace('.nse','')
    table.add_row(
      Padding(
        Align.center(
          f'💻️ [{self.BOLD_COLOR_1}]{sc}[/{self.BOLD_COLOR_1}] 💻️' 
       ),
        1
     )
   )
    table.add_row(
      f"[{self.BOLD_COLOR_2}]Author :[/{self.BOLD_COLOR_2}] {author}"
   )
    table.add_row(
      f"[{self.BOLD_COLOR_2}]License :[/{self.BOLD_COLOR_2}] {script_license}"
   )
    table.add_row(
      f"[{self.BOLD_COLOR_2}]Categories :[/{self.BOLD_COLOR_2}] {categories}"
   )
    table.add_row(
      f"[{self.BOLD_COLOR_2}]Description :[/{self.BOLD_COLOR_2}]\n\n{description}"
   )
    if usage != None:
      usage = usage.split(
        '@xmloutput'
     )[0] if '@xmloutput' in usage else usage
      table.add_row(
        f"[{self.BOLD_COLOR_2}]Usage :[/{self.BOLD_COLOR_2}]\n\n{usage}"
     )
    self.print(table, True)

  # format description lines
  def get_description_formatted(self, text):
    tmp = ''
    try:    
      for a in text.splitlines():
        if a != '':
          if a.endswith(".") or a.endswith(":") or\
          a.endswith(")") or a.startswith("*"):
            tmp += f"{a}\n\n"
          else:          
            tmp += a
      while tmp.endswith('\n'):
        tmp = tmp[:-1]
        tmp.replace('description=[[','')
    except Exception as e:
      del e
      return text
    return tmp
  
  def print_categories(self, categories, cat_title):    
    tree = Tree(
      f"🐉️ [{self.BOLD_COLOR_1}]{cat_title}[/{self.BOLD_COLOR_1}]"
    ) 
    for a,b in categories:
      cat = f"[{self.COLOR_2}]{a}.[/{self.COLOR_2}] 🐲️ {b}"
      tree.add(cat)
    self.print(Panel(tree, padding=(1,2), box=box.MINIMAL))
   
  # print scripts in a category    
  def print_script_category(self, cat, scripts):    
    sc = [
          f"[{self.COLOR_2}]{a}.[/{self.COLOR_2}] {html.escape(b.replace('.nse',''))}"
          for a,b in scripts
          ]    
    if len(sc) >= 1:
      self.print(Group(
                    Padding(
                      Text(
                        f"🐉️ {cat} 🐉️",
                        justify='center',
                        style=self.COLOR_1
                       ),
                      (0,1)
                     ),
                    Panel(
                      Columns(
                        sc,
                        expand=True,
                        equal=True,
                        padding=(1,2) 
                       ),
                        padding=(1,2),
                      box=box.MINIMAL 
                   )
                 ),
                  True
               )
      return True
    else:
      return False

  # get scripts path
  def get_scripts_path(self):
    current_checksum = ''
    scripts_path = '/usr/share/nmap/scripts/'
    if not os.path.exists(scripts_path):
      scripts_path = ''
    file_path = scripts_path + 'script.db'
    if not os.path.exists(file_path):
      file_path = ''
    else:
      current_checksum = hashlib.sha256(
        open(file_path,'rb').read() 
     ).hexdigest()
    file_backup = 'scriptbk.db'
    dbname = 'nmap_scripts.sqlite3'     
    return (
      scripts_path,
      file_path,
      file_backup,
      dbname,
      current_checksum
   )

  # check configuration file
  def check_config_file(self, conf_file):    
    if self.config_file_exits(conf_file):      
      content = open(conf_file, 'r')
      lines = content.read().splitlines()
      if len(lines) == 0 or len(lines) < len(self.conf_keys):        
        self.create_config_file()
        return False
      else:
        for a in lines:          
          if a.split(":")[0].strip(" ") not in self.conf_keys:
            self.create_config_file()
            break                  

  # check if configuration file exists
  def config_file_exits(self, conf_file):    
    if not os.path.exists(conf_file):      
      self.create_config_file()
      return False
    return True

  # create configuration file
  def create_config_file(self, search_on_key = 1,
                         search_opt = 1, theme = 1,
                         splash_anim = 1):
    scripts_path, file_path, file_backup,\
    dbname, current_checksum = self.get_scripts_path()
    stream = open('config.yaml', 'w')
    stream.write("config:\n")
    stream.write(
      f'  lang: "{"es" if "es" in os.environ["LANG"] else "en"}"\n'
   )
    stream.write(f"  scriptsPath: {scripts_path}\n")
    stream.write(f"  filePath: {file_path}\n")
    stream.write(f"  fileBackup: {file_backup}\n")
    stream.write(f"  scriptdb: {dbname}\n")
    stream.write('  categories: ["auth","broadcast","brute","default",\
    "discovery","dos","exploit","external","fuzzer","intrusive",\
    "malware","safe","version","vuln"]\n')
    stream.write(f"  checksum: {current_checksum}\n")
    stream.write(f"  searchOnKey: {search_on_key}\n")
    stream.write(f"  searchOpt: {search_opt}\n")
    stream.write(f"  theme: {theme}\n")
    stream.write("  histLen: 100\n")
    stream.write(f"  splashAnim: {splash_anim}")
    stream.close()

  # get script usage html
  def get_script_usage(self, usage):
    return f'''<section class="usage">
                  <h2>Usage</h2>
                    <section class="shell">
                      <ul class='console-menu'>
                        <li>File</li>
                        <li>Edit</li>
                        <li>View</li>
                        <li>Search</li>
                        <li>Terminal</li>
                        <li>Help</li>
                      </ul>
                      <div class="shell-content">
                        <code><p>---</p>{usage}<p>---</p></code>
                      </div>
                    </section>
              </section>'''

  # get script data in html format
  def get_script_html(
    self, script, author, license,
    categories, description, usage, theme
 ):
    return f'''
      <!DOCTYPE html>
      <html id="{theme}">
        <head>
          <meta name="content-type" content="text/html;charset=utf-8">
          <meta name="viewport" content="width=device-width,initial-scale=1.0">
          {self.get_script_style()}
          </head>
          <body>
            <main>
              <header>
                <h1>{script}.nse</h1>
              </header>
              <section class="script-info">
                <ul><li>Author : </li><li>&nbsp;{author}</li></ul>
                <ul><li>License : </li><li>&nbsp;{license}</li></ul>
                <ul><li>Categories : </li><li>&nbsp;{categories}</li></ul>
              </section>
              <section class="description">
                <h2>Description</h2>
                {description}
              </section>
                {usage}
            </main>
          </body>
        </html>'''

  # get script html styles
  def get_script_style(self):    
    return '''
      <style type="text/css">
        <!--
          html[id='default']{background-color:#fff;color:#333;}
          html[id='dark']{background-color:#ddd;color:#5b5b5b;}
          html[id='light']{background-color:#fbfbfb;color:#646060;}
          main{ padding:30px; }                    
          header{ pading-bottom:30px;border-bottom:1px solid silver; }
          h1{ 
            font-family:Architects Daughter;
            font-weight:normal;font-size:25px;text-align:center;
          }
          h2{ font-family:Architects Daughter;font-weight:normal; }
          html[id='dark'] a{color:#676767;}
          .description p{
            text-align:justify;word-break:break-all;
            margin-top:5px;font-size:15px; 
          }
          .script-info{ padding-top:50px; }
          .description, .usage{ padding-top:20px; }
          section ul{ 
            list-style:none;display:inline-block;
            box-content:border-box;width:100%;padding:0px;margin:3px 0;
          }
          section ul li:first-child{ font-weight:bold;font-size:15px; }
          section ul li{ display:inline-block;float:left;font-size:15px; }
          .shell{ 
            background-color:#000;padding:0px 0px 0px 0px;
            color:#fff;overflow-x:auto;margin:10px auto;
            border: 5px solid #d5d5d5;width:90%;
            height:auto;overflow:none;
          }
          .shell .console-menu { 
            margin:0px 0px 0px 0px;padding:0;width:100%;
            height:32px;list-style:none;background:#d5d5d5;
            color:#000;font-family:Times new Roman; 
          }
          .shell .console-menu li{ 
            display:inline-block;padding:5px 10px;
            font-size:14px;cursor:pointer;float:left;
            cursor:pointer;width:auto;font-weight:normal;
          }
          .shell .shell-content{ 
            padding:5px 10px 5px 10px;
            overflow-x:auto;font-size:15px;
          }
          .shell .shell-content p{ 
            padding:0px;font-size:14px;margin:0px; 
          }
          @media(max-width:640px){ .shell{ width:100%; } }
        -->
      </style>'''

  # get home tab html
  def get_home_html(
    self, title,  path, description, 
    version, theme, show_anim
 ):
    home_img = self.get_home_img(show_anim)
    return f'''
      <!DOCTYPE html>
        <html id="{theme}">
          <head>
            <meta name="content-type" content="text/html;charset=utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            {self.get_home_styles()}
          </head>
          <body>
            <main>
              <header>
                <h1>{title}</h1>
                <img src="file://{path}resources/{home_img}">
                <h2>{version}</h2>
                <img src="file://{path}resources/nsearch.png">
              </header>
              <section>
                <p>{description}</p>
              </section>
            </main>
          </body>
          </html>'''

  # get home tab styles
  def get_home_styles(self):
    return '''<style type="text/css">
            <!--
              html[id='default']{background-color:#fff;color:#333;}
              html[id='dark']{background-color:#ddd;color:#5b5b5b;}
              html[id='light']{background-color:#fbfbfb;color:#646060;}
              main{ padding:30px; } 
              img:nth-child(1){max-width:25%;}              
              header{ text-align:center; }
              h1{ 
                font-family:Architects Daughter;font-weight:normal;
                font-size:22px;text-align:center; 
              }
              h2{ 
                font-family:Architects Daughter;
                font-weight:normal;margin:20px 0; 
              }
              p{ text-align:justify;margin-top:30px; }
              img{ margin:40px 0 40px 0;zoom:0.7; }
              @media(max-width:600px){img{max-width:90%;}}
            -->
            </style>'''

  # get theme name
  def get_theme_name(self, theme):
    if theme == 1:
      return "default"
    return 'dark' if theme == 2 else 'light'

  # get history list
  def get_history(self):
    hist_file = None
    try:
      perm = 'r'
      if not os.path.exists(self.__hist_file):
        perm = 'x'
      hist_file = open(self.__hist_file, perm)
      content = hist_file.read()      
      count = 0
      for a in content.splitlines():
        if count <= 100:
          self.history.append(a)
        count += 1
    except Exception as ex:
      self.print_traceback(ex)
    finally:
      if hist_file != None:
        hist_file.close()

  # append command to history 
  def append_history(self, cmd):
    self.history.append(cmd)
    if len(self.history) > int(dbmodule.hist_len):      
      self.history.pop(0)

  # print history list
  def print_history(self, text):    
    if len(self.history) == 0:      
      self.print(
        Padding(
          Text(
            text,
            style=self.COLOR_1
          ),
          (1,2)
        ),
        True
      )
      return False
    
    index = 0
    rows = []    
    for a in self.history:
      index += 1
      rows.append(
        f"[{self.COLOR_2}]{str(index)}.[/{self.COLOR_2}] [reset]{a}"
      )      
    self.print(
      Panel(
        Columns(rows, expand=True, equal=True, padding=(1,2)),
        padding=(1,2),
        box=box.MINIMAL 
      )
    )
    return True

  # clear history list
  def clear_history(self, hist_text):    
    if os.path.exists(self.__hist_file):
      file = open(self.__hist_file, "w")
      file.write("")
      file.close()
      self.print(
        f"[{self.COLOR_2}]{hist_text}[/{self.COLOR_2}]",
        True
      )
      self.history.clear()

  # save history on exit
  def save_history(self):
    content = "".join( f"{a}\n" for a in self.history )
    content = content[0:-1]
    try:
      stream = open(self.__hist_file, "w")
      stream.write(f"{content}")
      stream.close()
    except Exception as e:
      self.print_traceback(e)

  # print command help
  def print_help(self, title, command, commands):    
    description = None
    table = self.get_result_table(True)        
    table.title_style = self.COLOR_3
    table.padding = (1,2,1,0)            
    for a in commands:       
      if a == command:
        for b in commands[a]:          
          if b == command:
            description = Text(commands[a][b])
          else:
            table.add_row(
              Text(
                b, style = self.COLOR_2
              ),
              commands[a][b]
            )
    title_container = Padding(
      Text(title, style=self.COLOR_3),
      pad = (1,0)
    )
    self.print(
      Panel(
        Group(
          title_container,
          Padding(description, pad=(0,0)),
          table
        ) 
        if description != None else
          Group(
            title_container,
            table
          ),
        box=box.MINIMAL, expand=False
      ), 
      True if command == "help" else False
    )

  # print exception traceback
  def print_traceback(self, e):
    print(type(e))
    if self.__debug and type(e) == Exception\
    or type(e) == TypeError: 
      self.print(e.args[0])
      self.console.print_exception()