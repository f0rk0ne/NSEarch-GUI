#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import hashlib
import re
import html.entities
import time
import yaml
import re
import requests
import nmap3
import stat
import asyncio
from rich import box
from rich.console import Console
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns
from rich.tree import Tree
from rich.spinner import Spinner
from rich.live import Live
from rich.prompt import IntPrompt
from rich.progress import Progress

COLOR_1 = "bright_red"
BOLD_COLOR_1 = "bold bright_red"
COLOR_2 = "deep_sky_blue1"
BOLD_COLOR_2 = f"bold deep_sky_blue1"
COLOR_3 = "indian_red"
DB_NAME = "nmap_scripts.sqlite3"
CONFIG_FILE = 'config.yaml'
NMAP_URL = "https://nmap.org/"
NSE_URL = f"{NMAP_URL}nsedoc/"
SCRIPT_URL = f"{NSE_URL}scripts/"
DOWNLOAD_URL = "https://svn.nmap.org/nmap/scripts/"
DB_URL = "https://raw.githubusercontent.com/f0rk0ne/NSEarch-GUI/main/nmap_scripts.sqlite3"
CHECKSUM_URL = "https://raw.githubusercontent.com/f0rk0ne/NSEarch-GUI/main/db/checksum"
YAML_EXT = ".yaml"
CATEGORIES = [
    "auth", "broadcast", "brute", "default",
    "discovery", "dos", "exploit", "external",
    "fuzzer", "intrusive", "malware",
    "safe", "version", "vuln"
]

class Utils:

    console = Console()
    banner = " _   _  _____  _____                     _\n"
    banner += "| \ | |/  ___||  ___|                   | |\n"
    banner += "|  \| |\ `--. | |__    __ _  _ __   ___ | |___\n"
    banner += "| . ` | `--. \|  __|  / _` || '__| / __|| '_  |\n"
    banner += "| |\  |/\__/ /| |___ | (_| || |   | (__ | | | |\n"
    banner += "\_| \_/\____/ \____/  \__,_||_|    \___||_| |_|\n"

    footer = "Version 1.0 https://bit.ly/3Rv9FNL @jjtibaquira\n"
    footer += "Email:🙎jko@dragonjar.org | 🙎www.dragonjar.org"
    lastcommand, lastargs = '', ''
    history, __hist_file = [], 'history'
    spinner_text, __debug, db_url = '', False, DB_URL
    db_name = DB_NAME
    path_reg = "^(\/)+[\w\d\.\/]+(\/)$"
    bool_reg = "^[0|1]$"
    opt_reg = "^[1-3]$"
    scripts_result = {}
    script_to_download = []
    conf_vars = {
        "lang": {"value": None, "regexp": "^(es|en)$"},
        "scriptsPath": {"value": None, "regexp": path_reg},
        "filePath": {"value": None, "regexp": "^(\/)+[\w\d\.\/]+(script\.db)$"},        
        "scriptdb": {"value": None, "regexp": "^(nmap_scripts\.sqlite3)$"},
        "categories": {"value": None, "regexp": ""},
        "checksum": {"value": None, "regexp": "^[a-fA-F\d]{64}$"},
        "searchOnKey": {"value": None, "regexp": bool_reg},
        "searchOpt": {"value": None, "regexp": opt_reg},
        "theme": {"value": None, "regexp": opt_reg},
        "splashAnim": {"value": None, "regexp": bool_reg},
        "histLen": {"value": None, "regexp": "^[\d]{1,}$"},
        "verticalTitle": {"value": None, "regexp": bool_reg},
        "singleTab": {"value": None, "regexp": bool_reg},
        "tabCount": {"value": None, "regexp": "^[\d]{1,2}$"}
    }

    def __init__(self):
        self.console = Console()        

    # print contents
    def print(self, renderable, print_header=False):
        render = Panel(renderable, box.MINIMAL) if "st"\
            in str(type(renderable)) else renderable
        if print_header:
            self.console.clear()
            if render != None:
                self.console.print(Group(self.get_banner(), render))
            else:
                self.console.print(self.get_banner())
        elif render != None:
            self.console.print(render)

    # get banner
    def get_banner(self):
        table = Table(
            expand=True,
            show_lines=True,
            show_header=False,
            border_style=COLOR_1,
            box=box.ROUNDED,
            pad_edge=True,
            padding=(0, 0)
        )
        table.add_column()
        table.add_row(
            Align.center(
                Text(
                    self.banner,
                    style=COLOR_2
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
        return Panel(table, padding=(0, 0), box=box.MINIMAL)

    # print exit message
    def print_exit(self, text):
        self.print(Text(f'{text} ... ', style=COLOR_3))
        self.save_history()

    # show spinner on create DB
    def show_spinner(self, text):
        self.print(
            Padding(
                Text(
                    self.spinner_text,
                    style=COLOR_2
                ),
                pad=[0, 1]
            ),
            True
        )
        with Live(
            Panel(
                Spinner(
                    "aesthetic",
                    text=text,
                    style=COLOR_1
                ),
                padding=[0, 1],
                box=box.MINIMAL
            ),
            console=self.console
        ) as live:
            time.sleep(.48)
            live.stop()

    # create a rich table instance
    def get_result_table(self, show_expand=True):
        table = Table.grid(expand=show_expand, padding=(1, 2), pad_edge=True)
        table.add_column()
        table.add_column()
        return table

    # print search results
    def print_results(self, items, params, result_text):
        sc = [
            f"[{COLOR_2}]{a[0]}.[/{COLOR_2}] {html.escape(a[1]['name'])}"
            for a in items
        ]
        title = f"[{COLOR_1}]{result_text}[/{COLOR_1}]"
        for a in params.keys():
            title += f"[{COLOR_2}]{a}:[/{COLOR_2}][white]{params[a]}[/white] "
        if len(sc) >= 1:
            self.print(
                Group(
                    Padding(
                        Align.center(
                            title
                        ),
                        (0, 1)
                    ),
                    Panel(
                        Columns(
                            sc,
                            expand=True,
                            equal=True,
                            padding=(1, 2)
                        ),
                        padding=(1, 2),
                        box=box.MINIMAL
                    )
                ),
                True
            )
            return True
        else:
            return False

    # print search by author results
    def print_author_results(self, items, params, result_text):
        title = f'[{COLOR_1}]{result_text}[/{COLOR_1}]'
        for a in params.keys():
            search_by = f"[{COLOR_2}]{a}:[/{COLOR_2}]"
            title += f"{search_by}[white]{params[a]}[/white] "
        table = self.get_result_table()
        table.add_row(
            Text(
                'Name',
                style=BOLD_COLOR_2
            ),
            Text(
                'Author',
                style=BOLD_COLOR_2
            )
        )
        for a in items:
            script = html.escape(a[1]['name'])
            script = f"[{COLOR_2}]{str(a[0])}.[/{COLOR_2}] {script}"
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

    # get ranking
    def get_ranking(self, ranking):
        if ranking == 0:
            return '[yellow]⭐️[/yellow]'
        if ranking == 1:
            return '[yellow]⭐️⭐️[/yellow]'
        if ranking == 2:
            return '[yellow]⭐️⭐️⭐️[/yellow]'

    # print favorites
    def print_favs(self, items, cols):
        table = self.get_result_table(False)
        table.add_column()
        table.add_row(
            Text(
                cols['name'],
                style=BOLD_COLOR_2
            ),
            Text(
                cols['ranking'],
                style=BOLD_COLOR_2
            ),
            ''
        )
        for value in items:
            table.add_row(
                value['name'],
                value['ranking'],
                value['stars']
            )
        self.print(table, True)

    # check if nse script exists
    def script_exists(self, script):
        if os.path.exists(script):
            return True
        return False
    
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
    
    def get_script_args_formatted(self, sc_args):
        scargs = sc_args.replace(".\n", ".\n\n")
        while scargs.endswith("\n"):
            scargs = scargs[:-1]
        return scargs

    # print script help
    def print_doc(self, **kwargs):
        if len(kwargs) == 0:
            return False
        categories = ''.join(
            [
                f"{a}, "
                for a in kwargs["categories"]
            ]
        )[:-2]
        requires = ''.join(
            [
                f"{NSE_URL}lib/{a}.html\n"
                for a in kwargs["requires"].split(",")
            ]
        )
        table = Table.grid(expand=True, padding=(1, 2), pad_edge=True)
        table.add_column()
        table.add_row(
            Padding(
                Align.center(
                    f'💻️ [{BOLD_COLOR_1}]{kwargs["name"]}[/{BOLD_COLOR_1}] 💻️'
                ),
                1
            )
        )
        table.add_row(
            f'[{BOLD_COLOR_2}]Categories :[/{BOLD_COLOR_2}] {categories}'
        )      
        table.add_row(
            f'[{BOLD_COLOR_2}]Author :[/{BOLD_COLOR_2}] {kwargs["author"]}'
        )
        table.add_row(
            f'[{BOLD_COLOR_2}]License :[/{BOLD_COLOR_2}] {kwargs["license"]}'
        )
        table.add_row(
            f'[{BOLD_COLOR_2}]Script Web :[/{BOLD_COLOR_2}] ' +
            f'{SCRIPT_URL}{kwargs["name"]}.html'
        )
        table.add_row(
            f'[{BOLD_COLOR_2}]Script Download :[/{BOLD_COLOR_2}] ' +
            f'{DOWNLOAD_URL}{kwargs["name"]}.nse'
        )        
        table.add_row(
            f'\n[{BOLD_COLOR_2}]Description :[/{BOLD_COLOR_2}]\n\n' + 
            f'{self.get_description_formatted(kwargs["summary"])}'
        )
        if kwargs["args"]:
            table.add_row(
                f'\n[{BOLD_COLOR_2}]Script Arguments :[/{BOLD_COLOR_2}]\n\n' + 
                f'{self.get_script_args_formatted(kwargs["args"])}'
            )
        if kwargs["usage"] != None:            
            table.add_row(
                f'\n[{BOLD_COLOR_2}]Usage :[/{BOLD_COLOR_2}]\n\n' + 
                f'{kwargs["usage"]}'
            )
        table.add_row(
            f'[{BOLD_COLOR_2}]Requires :[/{BOLD_COLOR_2}]'
        )
        table.add_row(
            f'{requires}'
        )
        self.print(table, True)

    # format description lines
    def get_description_formatted(self, text):
        tmp = ''
        try:
            for a in text.splitlines():
                if a != '':
                    if (
                        a.endswith(".") or a.endswith(":") or
                        a.endswith(")") or a.startswith("*") or
                        a.endswith(".html")
                    ):
                        tmp += f"{a}\n\n"                    
                    else:
                        tmp += a
            while tmp.endswith('\n'):
                tmp = tmp[:-1]                
        except Exception as e:
            del e
            return text
        return tmp

    # print all categories
    def print_categories(self, categories, cat_title):
        tree = Tree(
            f"🐉️ [{BOLD_COLOR_1}]{cat_title}[/{BOLD_COLOR_1}]"
        )
        for a, b in categories:
            cat = f"[{COLOR_2}]{a}.[/{COLOR_2}] 🐲️ {b}"
            tree.add(cat)
        self.print(Panel(tree, padding=(1, 2), box=box.MINIMAL))

    # print scripts in a category
    def print_script_category(self, cat, scripts):
        sc = [
            f"[{COLOR_2}]{a}.[/{COLOR_2}] {html.escape(b)}"
            for a, b in scripts
        ]
        if len(sc) >= 1:
            self.print(Group(
                Padding(
                    Text(
                        f"🐉️ {cat} 🐉️",
                        justify='center',
                        style=COLOR_1
                    ),
                    (0, 1)
                ),
                Panel(
                    Columns(
                        sc,
                        expand=True,
                        equal=True,
                        padding=(1, 2)
                    ),
                    padding=(1, 2),
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
        for a, b, c in os.walk("/usr"):
            del b
            if "nmap" in a:
                for d in c:
                    if d == "script.db":
                        return f"{a}/"

    # check if configuration file exists
    def config_file_exits(self):
        if not os.path.exists(CONFIG_FILE):
            self.create_config_file()
            return False
        return True

    # get database checksum
    def get_checksum(self):
        if os.path.exists(DB_NAME):
            return hashlib.sha256(
                open(DB_NAME, "rb").read()
            ).hexdigest()
        return False

    # check database checksum
    def is_db_checksum(self, current_checksum):
        checksum = self.get_checksum()        
        return checksum == current_checksum

    # get yaml items
    def get_yaml(self):
        stream = None
        try:
            stream = open(CONFIG_FILE, 'r+')
            item = yaml.safe_load(stream)
            if isinstance(item, dict):
                if "config" in item.keys():
                    return item["config"]
                else:
                    self.create_config_file()
                    return dict()
            else:
                self.create_config_file()
                return dict()            
        except Exception as e:
            self.print_traceback(e)
        finally:
            if stream:
                stream.close()

    # check configuration file
    def check_config_file(self):
        try:
            if self.config_file_exits():
                item = self.get_yaml()
                for key in self.conf_vars.keys():
                    if key in item.keys():
                        if not self.load_conf_var(item, key):
                            return False                        
                    else:
                        self.create_config_file()
                        return False
        except Exception as e:
            self.print_traceback(e)

    # load config var
    def load_conf_var(self, item, key):
        if isinstance(item[key], list):
            if set(item[key]) == set(CATEGORIES):
                self.conf_vars[key]["value"] = item[key]
            else:
                self.create_config_file()
                return False
        elif re.match(
            self.conf_vars[key]["regexp"],
            str(item[key])
        ):
            self.conf_vars[key]["value"] = item[key]
        else:
            self.create_config_file()
            return False
        return True

    # get yam files vars
    def get_db_vars(self):
        try:            
            scripts_path = self.get_scripts_path()            
            if not os.path.exists(scripts_path):
                scripts_path = ''
            file_path = scripts_path + 'script.db'
            if not os.path.exists(file_path):
                file_path = ''           
            return (
                scripts_path,
                file_path,
                DB_NAME
            )
        except Exception as e:
            self.print_traceback(e)

    # get yam vars
    def get_yaml_vars(self):
        yaml_vars = dict()
        for key in self.conf_vars.keys():
            yaml_vars[key] = self.conf_vars[key]["value"]
        return yaml_vars

    # create configuration file
    def create_config_file(
        self, search_on_key=1,
        search_opt=1, theme=1,
        splash_anim=1, lang="",
        vertical_title=1, single_tab=1,
        tab_count=5
    ):
        try:                   
            scripts_path, file_path, dbname = self.get_db_vars()
            if not lang:
                if "LANG" in os.environ.keys():
                    lang = "es" if "es" in os.environ["LANG"] else "en"
                else:
                    lang = "en"
            stream = open('config.yaml', 'w')
            stream.write("config:\n")
            stream.write(f"  lang: {lang}\n")
            stream.write(f"  scriptsPath: {scripts_path}\n")
            stream.write(f"  filePath: {file_path}\n")            
            stream.write(f"  scriptdb: {dbname}\n")
            stream.write(f"  categories: {CATEGORIES}\n")
            stream.write(f"  checksum: {self.get_checksum()}\n")
            stream.write(f"  searchOnKey: {search_on_key}\n")
            stream.write(f"  searchOpt: {search_opt}\n")
            stream.write(f"  theme: {theme}\n")
            stream.write("  histLen: 100\n")
            stream.write(f"  splashAnim: {splash_anim}\n")
            stream.write(f"  verticalTitle: {vertical_title}\n")
            stream.write(f"  singleTab: {single_tab}\n")
            stream.write(f"  tabCount: {tab_count}")
            stream.close()
            self.check_config_file()
        except Exception as e:
            if "Permission denied" in e.args:
                print("Executed with root privileges or change folder owne")
                exit(0)
            self.print_traceback(e)

    # get script usage html
    def get_script_usage(self, usage):
        html = ''        
        if usage:
            usage = self.html_entities(usage)
            usage_ = "".join(
                f"{line}</br>"
                for line in usage.splitlines()
            )       
            html = f'''<section class="usage">
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
                        <code><p>---</p>{usage_}<p>---</p></code>
                      </div>
                    </section>
              </section>'''
        return html

    # get javascript tag for scripts views
    def get_js_theme(self):
        return """<script>
            function setTheme(theme){
                var h = document.querySelector("html");
                h.setAttribute("id", theme);                    
            }
        </script>"""

    # format script help contents
    def format_paragraph(self, text):
        text_ = self.get_description_formatted(text)
        final = ''.join(
            f'<p>{a}</p>'
            for a in text_.splitlines()
        )        
        return final

    # convert html tags in htmlentities
    def html_entities(self, text):
        return text.replace(
            "&", "&amp;"
        ).replace(
            "<", "&lt;"
        ).replace(
            ">", "&gt;"
        )

    # get script args html
    def get_script_args(self, args):
        html = ''
        if args:
            args = self.html_entities(args)
            text = "".join(
                f"<p>{line}</p>"
                for line in args.splitlines()
            )
            text = text.replace(".</p>",".<br><br></p>")
            html = f'''
            <section class="script-args">
                <h2>Script Arguments</h2>
                {text}
            </section>
            '''
        return html

    # get summary html
    def get_summary(self, summary):
        summary = self.html_entities(summary)
        return f"""
        <section class="description">
            <h2>Description</h2>
            {self.format_paragraph(summary)}
        </section>"""

    # get script requires links
    def get_script_requires_links(self, requires):
        return "".join(
            f"<a href='{NSE_URL}lib/{line}.html'>{line}</a>, "
            for line in requires.split(",")
        )

    # get script categories links
    def get_script_cat_links(self, categories):
        return ''.join(
            [
                f"<a href='{NSE_URL}categories/{a}.html'>{a}</a>, " 
                for a in categories
            ]
        )[:-2]

    # get script web link
    def get_script_web_link(self, name):
        return f"""
            <a href="{SCRIPT_URL}{name}.html">
            {name}.html
            </a>
        """

    # get script download link
    def get_script_download_link(self, name):
        return f"""
            <a href="{DOWNLOAD_URL}{name}.nse">
            {name}.nse
            </a>
        """

    # get license link
    def get_script_license_link(self, license):
        if "man-legal" in license:
            return f"""Same as Nmap -- See 
                <a href='https://nmap.org/book/man-legal.html'>
                man-legal
                </a>"""                
        elif "BSD-simplified" in license:
            return f"""Simplified (2-clause) BSD license -- See
                <a href='https://nmap.org/svn/docs/licenses/BSD-simplified'>
                BSD simplified
                </a>"""
        else:
            return ""

    # get script data in html format
    def get_script_html(self,  theme, **kwargs):
        return f'''
        <!DOCTYPE html>
        <html id="{theme}">
        <head>
            <meta name="content-type" content="text/html;charset=utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            {self.get_script_style()}
            {self.get_js_theme()}
            </head>
            <body>
                <main>
                    <header>
                        <h1>{kwargs['name']}.nse</h1>
                    </header>
                    <section class="script-info">
                        <ul><li>Author : </li><li>&nbsp;{kwargs['author']}</li></ul>
                        <ul>
                            <li>License : </li>
                            <li>&nbsp;{self.get_script_license_link(kwargs['license'])}</li>
                        </ul>
                        <ul>
                            <li>Categories : </li>
                            <li>&nbsp;{self.get_script_cat_links(kwargs["categories"])}</li>
                        </ul>
                        <ul>
                            <li>Requires : </li>
                            <li>&nbsp;{self.get_script_requires_links(kwargs["requires"])}</li>
                        </ul>
                        <ul>
                            <li>Script Web : </li>
                            <li>&nbsp;{self.get_script_web_link(kwargs["name"])}</li>
                        </ul>
                        <ul>
                            <li>Script Download : </li>
                            <li>&nbsp;{self.get_script_download_link(kwargs["name"])}</li>
                        </ul>
                    </section>
                    {self.get_summary(kwargs['summary'])}
                    {self.get_script_args(kwargs['args'])}
                    {self.get_script_usage(kwargs['usage'])}
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
          html[id='light']{background-color:#eff;color:#646060;}
          main{ padding:30px; }
          header{ pading-bottom:30px;border-bottom:1px solid silver; }
          h1{ 
            font-family:Architects Daughter;
            font-weight:normal;font-size:25px;text-align:center;
          }
          h2{ font-family:Architects Daughter;font-weight:normal; }
          html a{cursor:pointer;}
          html[id='dark'] a{color:#676767;}          
          .description p, .script-args p, .usage p{
            text-align:justify;word-break:break-all;
            margin-top:5px;font-size:15px; 
          }
          .script-info{ padding-top:50px; }
          .description, .script-args, .usage{ padding-top:20px; }
          section ul{ 
            list-style:none;display:inline-block;
            box-content:border-box;width:100%;padding:0px;margin:3px 0;
          }
          ul>li>a{word-wrap:break-line;}
          section ul li:first-child{ font-weight:bold;font-size:15px; }
          section ul li{ display:inline-block;float:left;font-size:15px; }
          .shell{ 
            background-color:#000;padding:0px 0px 0px 0px;
            color:#fff;overflow-x:auto;margin:0px auto;
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
    def get_home_html(self, **kwargs):
        home_img = self.get_home_img(kwargs['show_anim'])
        return f'''
        <!DOCTYPE html>
        <html id="{kwargs['theme']}">
          <head>
            <meta name="content-type" content="text/html;charset=utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            {self.get_home_styles()}
            {self.get_js_theme()}
          </head>
          <body>
            <main>
              <header>
                <h1>{kwargs['title']}</h1>
                <img src="file://{kwargs['path']}resources/{home_img}">
                <h2>{kwargs['version']}</h2>
                <img src="file://{kwargs['path']}resources/nsearch.png">
              </header>
              <section>
                <p>{kwargs['description']}</p>
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
              html[id='light']{background-color:#eff;color:#646060;}
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
            content = hist_file.read() if perm == "r" else ""
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
    def append_history(self, cmd, hist_len):
        if "history" not in cmd and cmd != "":
            self.history.append(cmd)
        if len(self.history) > int(hist_len):
            self.history.pop(0)

    # print history list
    def print_history(self, text):
        if len(self.history) == 0:
            self.print(
                Padding(
                    Text(
                        text,
                        style=COLOR_1
                    ),
                    (1, 2)
                ),
                True
            )
            return False

        index = 0
        rows = []
        for a in self.history:
            index += 1
            if a:
                rows.append(
                    f"[{COLOR_2}]{str(index)}.[/{COLOR_2}] [reset]{a}"
                )
        self.print(
            Panel(
                Columns(rows, expand=True, equal=True, padding=(1, 2)),
                padding=(1, 2),
                box=box.MINIMAL
            )
        )
        return True

    # clear history list
    def clear_history(self, hist_text):
        try:
            if os.path.exists(self.__hist_file):
                h_file = open(self.__hist_file, "w")
                h_file.write("")
                h_file.close()
                self.print(
                    f"[{COLOR_2}]{hist_text}[/{COLOR_2}]",
                    True
                )
                self.history.clear()
        except Exception as e:
            self.print_traceback(e)

    # save history on exit
    def save_history(self):
        content = "".join(f"{a}\n" for a in self.history)
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
        table.title_style = COLOR_3
        table.padding = (1, 2, 1, 0)
        for a in commands:
            if a == command:
                for b in commands[a]:
                    if b == command:
                        description = Text(commands[a][b])
                    else:
                        table.add_row(
                            Text(
                                b, style=COLOR_2
                            ),
                            commands[a][b]
                        )
        title_container = Padding(
            Text(title, style=COLOR_3),
            pad=(1, 0)
        )
        self.print(
            Panel(
                Group(
                    title_container,
                    Padding(description, pad=(0, 0)),
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

    # rich int prompt
    def ask(self, msg):
        return IntPrompt.ask(msg)
   
    def is_con(self):
        try:
            if requests.get("https://www.google.com").ok:                
                return True
        except requests.ConnectionError as e:            
            return False
        except Exception as e:
            self.print_traceback(e)

    # rename database file
    def rename_db(self):
        if os.path.exists(DB_NAME):
            db_id = self.get_db_copy_id()
            os.rename(DB_NAME, f"{DB_NAME}.old.{db_id}")

    # check database updates
    def check_db_update(self, current_checksum):
        try:
            with requests.get(CHECKSUM_URL) as req:
                if req.status_code == 200:                    
                    if req.text.strip("\n") != current_checksum:
                        self.rename_db()
                        return True
            return False
        except requests.ConnectionError as e:
            del e
            return 2
        except Exception as e:
            self.print_traceback(e)            

    # get database copy numeration
    def get_db_copy_id(self):
        path = os.path.abspath(__file__)
        path = "".join(
            f"{a}/" for a in path.split("/")[:-2]
        )
        db_id = 0        
        for a, b ,c in os.walk(path):
            if a.endswith("NSEarch-GUI/"):
                for d in c:
                    if ".old." in d:
                        db_id_ = int(d.split(".")[-1:][0])
                        if db_id_ > db_id:
                            db_id = db_id_
        return db_id + 1

    # download db
    def download_db(self, text, conn_error):
        try:  
            self.print("", True)
            with requests.get(DB_URL, stream=True) as req:
                if req.status_code == 200:
                    total_length = int(req.headers.get("Content-Length"))                    
                    self.rename_db()
                    stream = open(DB_NAME, "wb")              
                    with Progress() as progress:
                        task = progress.add_task(f"  {text}", total=total_length)
                        for chunk in req.iter_content(1):
                            stream.write(chunk)
                            progress.update(task, advance=1)
                    stream.close()
                    return True
            return False
        except requests.ConnectionError as e:
            self.print(f"[{BOLD_COLOR_2}]{conn_error}[/{BOLD_COLOR_2}]")
        except Exception as e:
            self.print_traceback(e)

    # get nmap template
    def get_nmap_template(self, template):
        try:            
            template_path = f"templates/{template}.yaml"
            if os.path.exists(template_path):
                stream = open(template_path, "+r")
                item = yaml.safe_load(stream)
                stream.close()
                return item
            else:
                self.print(f"Template not found {template_path}")
        except Exception as e:
            self.print_traceback(e)

    def run_nmap(self, net, arguments, root_text):
        try:
            nm = nmap3.NmapAsync()
            result = asyncio.run(
                nm.scan_command(
                    net,
                    arguments
                )
            )
            self.print_nmap_results(
                net,
                nm.parser.filter_top_ports(result)
            )
        except Exception as e:
            if "root" in str(e):
                self.print(
                    f"nmap {arguments} {net}\n"+
                    root_text
                )
                return None
            self.print_traceback(e)

    # print nmap results
    def print_nmap_results(self, net, result):
        try:
            if isinstance(result, dict):                
                table = Table.grid(expand=True)
                table.add_column()            

                table.add_row(
                    Align.center(
                        f"Scan results for [{BOLD_COLOR_2}]{net}[/{BOLD_COLOR_2}]\n"
                    )
                )
                table.add_row(
                    f"{self.get_nmap_version(result['stats'])}"
                )
                table.add_row(
                    result['stats']['args']
                )
                self.print(
                    Panel(table, box=box.MINIMAL)
                )
                self.print_host_data(result)
        except Exception as e:
            self.print_traceback(e)

    def get_nmap_version(self, data):
        if data:
            return str(
                f"[{BOLD_COLOR_1}]Nmap Version [/{BOLD_COLOR_1}]" +
                data['version']
            )

    def print_host_data(self, result):
        host_table = Table.grid(
            expand=True,            
            collapse_padding=True
        )
        pad = (1,0,0,0)
        host_table.add_column()        
        for host in result.keys():
            if (host != "runtime" and host != "stats" 
            and host != "task_results"):                
                header = self.get_result_header(
                    result[host],
                    host                        
                )                
                ports = self.get_result_ports(
                    result[host]["ports"]
                )                
                osmatch = self.get_os_match(
                    result[host]["osmatch"]
                )                
                scripts = self.get_scripts_results()                
                host_table.add_row(header)
                if ports:
                    host_table.add_row(Padding(ports, pad=pad))
                if osmatch:
                    host_table.add_row(Padding(osmatch, pad=pad))
                if scripts:
                    host_table.add_row(Padding(scripts, pad=pad))
        host_table.add_row(
            Padding(
                self.get_scan_summary(
                    {
                        "startstr": result["stats"]["startstr"],
                        "timestr": result["runtime"]["timestr"],
                        "elapsed": result["runtime"]["elapsed"],
                        "summary": result["runtime"]["summary"]
                    }
                ),
                pad=pad
            )
        )
        self.print(
            Panel(
                host_table,
                box=box.MINIMAL
            )
        )        

    def get_result_header(self, host, target):
        state = host["state"]        
        host_title = f'[{BOLD_COLOR_1}]Host: [/{BOLD_COLOR_1}] {target}\n'
        host_str = ''

        if "hostname" in host.keys():
            if len(host["hostname"]) > 0:
                hostname = host["hostname"][0]                
                host_str = f'[{BOLD_COLOR_2}]Name:[/{BOLD_COLOR_2}]{hostname["name"]} '
                host_str += f'[{BOLD_COLOR_2}]Type:[/{BOLD_COLOR_2}]{hostname["type"]}\n'                
        
        state_str = f'[{BOLD_COLOR_2}]State:[/{BOLD_COLOR_2}]{state["state"]} '
        state_str += f'[{BOLD_COLOR_2}]Reason:[/{BOLD_COLOR_2}]{state["reason"]} '
        state_str += f'[{BOLD_COLOR_2}]ttl:[/{BOLD_COLOR_2}]{state["reason_ttl"]}'        
        return f"{host_title}{host_str}{state_str}"

    def get_result_ports(self, ports):
        if len(ports) > 0:
            table = self.get_ports_table()
            for b in ports:
                if isinstance(b, dict):
                    cpe, product = "", ""                    
                    table.add_row(
                        b["protocol"],
                        b["portid"],
                        b["state"],
                        b["reason"],
                        b["reason_ttl"],
                        b["service"]["name"],
                        product,
                        cpe
                    )                
                    if len(b["scripts"]) > 0:                    
                        self.add_script_results(b["scripts"], b["portid"])
            return table
        else:
            return None

    def get_port_strs(self, b):
        cpe = ""
        product = ""
        if len(b["cpe"]) > 0:
            cpe = b["cpe"][0]["cpe"].replace("cpe:/", "")
        if "product" in b["service"].keys():
            product = b["service"]["product"]
        return (cpe, product)

    def add_script_results(self, scripts, port):
        port_scripts = []
        for z in scripts:
            keys = z.keys()
            if "name" in keys and "raw" in keys and "data" in keys:
                port_scripts.append({
                    "name": z["name"],
                    "raw": z["raw"],
                    "data": z["data"]
                })                
        self.scripts_result.setdefault(
            port,
            port_scripts
        )

    def get_ports_table(self):
        table = Table.grid(padding=(0,2))
        titles = [ 
            "protocol", "Port",
            "State", "Reason",
            "ttl", "Service",
            "Service Product", "cpe"
        ]

        for index, title in enumerate(titles):
            table.add_column()
            titles[index] = f"[{BOLD_COLOR_2}]{title}[/{BOLD_COLOR_2}]"
        
        table.add_row( 
            titles[0], titles[1],
            titles[2], titles[3],
            titles[4], titles[5],
            titles[6], titles[7]
        )
        return table  

    def get_scripts_results(self):
        table = None
        if len(self.scripts_result) > 0:            
            for key in self.scripts_result.keys():                
                title = f"[{BOLD_COLOR_2}]Script(s) result(s) for port[/{BOLD_COLOR_2}] ({key})"
                table = Table.grid(expand=True, padding=(1,0))
                table.add_column()
                table.add_row(Align.center(title))
                for result in self.scripts_result[key]:
                    raw = self.format_port_raw(result['raw'])
                    if raw:
                        raw = f"\n{raw}"
                    table.add_row(
                        f"[green3]{result['name']}[/green3]:" +
                        raw
                    )
            self.scripts_result = {}            
        return table

    def get_scan_summary(self, data):
        table = Table.grid()
        table.add_column()
        
        table.add_row(data["summary"])
        table.add_row(
            f"[{BOLD_COLOR_1}]Start time:[/{BOLD_COLOR_1}] {data['startstr']}"
        )
        table.add_row(
            f"[{BOLD_COLOR_1}]End time:[/{BOLD_COLOR_1}] {data['timestr']}"
        )
        table.add_row(
            f"[{BOLD_COLOR_1}]Elapsed:[/{BOLD_COLOR_1}] {data['elapsed']}"
        )
        return table        

    def format_port_raw(self, raw):
        raw = str(raw)
        while (raw.startswith("\n") or
        raw.startswith(" ")):
            raw = raw[1:]
        while raw.endswith("\n"):
            raw = raw[:-1]
        return raw

    def get_os_match(self, data):
        if data:
            data = data[0]
            table = Table.grid(padding=(0,2))
            table.add_column()
            table.add_column()
            table.add_row(
                f"[{BOLD_COLOR_1}]OS Match[/{BOLD_COLOR_1}]",
                ""
            )
            for b in data.keys():
                if b == "osclass":
                    for c in data[b].keys():
                        table.add_row(
                            f"[{BOLD_COLOR_2}]{c}:[/{BOLD_COLOR_2}]",
                            data[b][c]
                        )
                else:
                    table.add_row(
                        f"[{BOLD_COLOR_2}]{b}:[/{BOLD_COLOR_2}] ", 
                        data[b]
                    )
            return table            

    def init_script_update(self, scripts, script_path, download_text):
        for script in scripts:
            if not os.path.exists(
                f"{script_path}{script}.nse"
            ):                
                self.script_to_download.append(
                    script
                )
        if len(self.script_to_download) > 0:
            if self.is_root():
                return self.init_scripts_download(download_text)
            return {"result": 3}
        else:
            return {"result": 0}

    def is_root(self):
        if os.geteuid() == 0:
            return True
        return False
            
    def init_scripts_download(self, download_text):
        scripts_path = self.get_scripts_path()
        downloaded = []
        for script in self.script_to_download:
            downloaded.append(
                self.download_script(
                    script,
                    scripts_path,
                    download_text
                )
            )
        ok = [a for a in downloaded if a == True ]
        scripts = len(self.script_to_download)
        self.script_to_download = []
        if len(ok) == len(downloaded):
            return {
                "result":1,
                "count": scripts
            }
        else:
            return {
                "result": 2,
                "ok": len(ok),
                "error": len(downloaded)
            }        

    def download_script(self, script, scripts_path, download_text):
        sc_path = f"https://svn.nmap.org/nmap/scripts/{script}.nse"
        try:
            with requests.get(sc_path) as req:
                if req.status_code == 200:
                    total_length = int(req.headers.get("Content-Length"))                    
                    script_file = f"{scripts_path}{script}.nse"
                    stream = open(script_file, "wb")              
                    with Progress() as progress:                    
                        task = progress.add_task(f"  {download_text} {script}", total=total_length)
                        for chunk in req.iter_content(1):
                            stream.write(chunk)  
                            progress.update(task, advance=1)
                    stream.close()
                    os.chmod(script_file, 0o644)
                    return True
                else:
                    return False
        except Exception as e:
            del e            
        return False

    def print_templates(self, text):
        table = Table.grid(padding=(1,2))
        table.add_column()
        table.add_column()
        table.add_column()
        table.add_row(
            f"[{BOLD_COLOR_2}]{text[0]}[/{BOLD_COLOR_2}]",
            f"[{BOLD_COLOR_2}]{text[1]}[/{BOLD_COLOR_2}]",
            f"[{BOLD_COLOR_2}]{text[2]}[/{BOLD_COLOR_2}]",
            f"[{BOLD_COLOR_2}]{text[3]}[/{BOLD_COLOR_2}]"
        )
        total_templates = 0
        for a, b, c in os.walk("templates"):
            del b            
            for d in c:
                if d.endswith(YAML_EXT):
                    args = self.check_template(d)
                    state = "👍"
                    if not args:
                        args = text[4]
                        state = "👎"
                    table.add_row(
                        f"templates/{d}",
                        d.strip(YAML_EXT),
                        state,
                        args
                    )
                    total_templates += 1
        table.add_row(
            f"[{BOLD_COLOR_1}]{text[5]}[/{BOLD_COLOR_1}]" +
            f" {str(total_templates)}",
            "", ""
        )
        self.print(Padding(table, pad=(1,2)))

    def check_template(self, template):
        try:            
            template_name = template.replace(YAML_EXT, "")
            stream = open(
                f"templates/{template}",
                "+r"
            )            
            item = yaml.safe_load(stream)
            stream.close()            
            return item[template_name]["arguments"]
        except Exception as e:
            if "not subscriptable" in str(e):
                return False

    # print exception traceback
    def print_traceback(self, e):
        if self.__debug and e:
            self.console.print_exception()
