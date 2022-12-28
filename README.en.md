<p align="center">
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191317706-98de49f1-fdef-467e-b9c2-943fb8be9a9b.gif#gh-dark-mode-only"/>
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191317849-1d7c3138-ea05-4631-9295-3a5530266259.gif#gh-light-mode-only"/>
</p>
<h1 align="center">Nmap Script Engine Search</h1>
<br/>
<br>
<p>Is a fork for NSEarch app written by <a href="https://github.com/jtibaquira/nsearch">Jacobo Tibaquira</a> of <a href="https://www.dragonjar.org">DragonJAR</a> community, now includes a Graphical Interface and new commands.
</p>
<p align="center">
    <br>
    <img title="NSEarch GUI themes" src="https://user-images.githubusercontent.com/77067446/209880434-fb6553d0-e4ec-49f9-9174-38d25524e34e.png"/>
</p>
<br/>
<h2>Requirements</h2>
<br/>

- [x] Python 3 ( Tested in 3.7, 3.8, 3.9, 3.10 )
- [x] python3-venv or python3-virtualenv
- [x] pyside >= 6.4.1
- [x] python3-nmap
- [x] python-i18n
- [x] PyYAML
- [x] rich
- [x] requests 

<br/>
<h2>Installation</h2>
<br/>
<p>Download app from github repository and execute install.sh to check and install requirements and to create the configuration file.
</p>   

```bash
git clone https://github.com/f0rk0ne/NSEarch-GUI.git 
```

```bash
bash install.sh
```

<br>
<h3>Run</h3>
<br>

```bash
./nsearch
```

<p>When root operations are required, such as download missing NSE scripts or run some nmap scans.</p>

```bash
./nsearch_root
or
sudo -E env PATH=$PATH ./nsearch
```

<br>
<h3>Manual Install</h3>
<br>
<p>Denpending Linux distribution it's neccesary to install a python3 compatible version for GUI modules, this example uses python3.9, but exists other alternatives (python3.7, python3.8, python3.9, python3.10).</p>

```bash
apt-get install sqlite3 fonts-noto-color-emoji python3-virtualenv python3-pip qtwayland5 -y
apt-get update -y && apt-get upgrade -y 
```

```bash
yum install -y google-noto-emoji-color-fonts epel-release python3-virtualenv python3-pip sqlite-devel -y; sudo yum update -y
yum update -y && yum upgrade -y
```

```bash
python3.9 -m venv NSEarchEnv --prompt NSEarch
source NSEarchEnv/bin/activate
python3.9 -m pip install --upgrade pip
python3.9 -m pip install --user -r requirements.txt
deactivate
```

<br>
<h4>Run</h4>
<br>

```bash
source NSEarchEnv/bin/activate
python3 nsearch.py
deactivate
```

<br>
If console doesn't show colorized emojis, in this link you could to find the solution <a href="https://www.reddit.com/r/linux/comments/ao0mp3/how_to_better_enable_color_emojis/#t1_efxvrmq">https://www.reddit.com/r/linux/comments/ao0mp3/how_to_better_enable_color_emojis/#t1_efxvrmq</a>
<br>
<br>
<h2>Configuration</h2>
<br/>
<h3>Configuration File</h3>
<p>config.yaml</p>
    
```yaml
config:
  lang: es
  scriptsPath: /usr/share/nmap/scripts/
  filePath: /usr/share/nmap/scripts/script.db
  scriptdb: nmap_scripts.sqlite3
  categories: ['auth', 'broadcast', 'brute', 'default', 'discovery', 'dos', 'exploit', 'external', 'fuzzer', 'intrusive', 'malware', 'safe', 'version', 'vuln']
  checksum: bfa9e3c863ddd7ccd15620ac1d1c7f94d3652e2353388e7790c711fc444926d8
  searchOnKey: 1
  searchOpt: 1
  theme: 1
  histLen: 100
  splashAnim: 1
  verticalTitle: 1
  singleTab: 1
  tabCount: 5
```

<br>
<table width="100%">
<tr>        
    <th>Variable</th>
    <th>Description</th>
    <th>Type</th>
    <th>Values</th>        
</tr>
<tr>
    <td>lang</td>
    <td>Language</td>
    <td>string</td>
    <td>"es" (Spanish) <br> "en" (English)</td>
</tr>
<tr>
    <td>seachOnKey</td>
    <td>Search on key pressed</td>
    <td>bool</td>
    <td>1 (Active)<br> 0 (Inactive)</td>
</tr>
<tr>
    <td>searchOpt</td>
    <td>Search options</td>
    <td>int</td>
    <td>1 (Name)<br> 2 (Author)<br> 3 (Category)</td>
</tr>
<tr>
    <td>theme</td>
    <td>GUI theme</td>
    <td>int</td>
    <td>1 (Default)<br> 2 (Dark)<br> 3 (Light)</td>
</tr>
<tr>
    <td>histLen</td>
    <td>History file line count</td>
    <td>int</td>
    <td>100</td>
</tr>
<tr>
    <td>splashAnim</td>
    <td>Active Animation</td>
    <td>bool</td>
    <td>1 (Active)<br> 0 (Inactive)</td>
</tr>
<tr>
    <td>verticalTitle</td>
    <td>Shows vertical title in GUI mode</td>
    <td>bool</td>
    <td>1 (Active)<br> 0 (Inactive)</td>
</tr>
<tr>
    <td>singleTab</td>
    <td>Shows NSE scripts help in one or more tabs</td>
    <td>bool</td>
    <td>1 (Active)<br> 0 (Inactive)</td>
</tr>
<tr>
    <td>tabCount</td>
    <td>When singleTab is disabled, determines how many tabs are shown to load NSE scripts help</td>
    <td></td>
    <td>5<br>10<br>20<br>30</td>
</tr>
</table>
<br>
<h2>Changelog</h2>
<h3>Console</h3>

<img title="NSEarch Console mode" src="https://user-images.githubusercontent.com/77067446/209884384-64129a2c-2aa2-4541-94a9-36c0a4b86506.png"/>

- Database is included in the repository, thus contains all NSE scripts from nmap web.
- Console version includes some rich python module features, such as results in columns, animations at startup between others.
- New command showcat shows categories and list all scripts in a category and shows scripts help too.
- New command history to see executed commands, like Linux history command.
- New command update to download database or missing NSE scripts from <a href="https://www.nmap.org">nmap</a>
- Now includes emojis. 
- The run command has been reinstated in this new NSEarch fork version.

<br>
<h2>GUI</h2>
<br>
<p>GUI was written in Python Qt, and have two QDockWidgets to manage scripts and favorites.</p>
<p>Scripts help contents are shown in HTML format in tabs.</p>
<p>Language selection apply to console version too.</p>

<br>
<h3>Start NSEarch GUI</h3>

```bash
./nsearch -g
```

<br>
<h3>GUI Configuration</h3>
<br>
<p>Allows establish Graphical Interface options.</p>
<br>
<p align="center">
    <img width="400" title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/209881076-220a92a8-77dc-4821-bc3d-6b5c5146a3f5.png#gh-light-mode-only"/>
    <img width="400" title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/209881075-16c1062b-e3b7-4896-a321-d0184118e1da.png#gh-dark-mode-only"/>
</p>
<h3>Scripts Panel</h3>
<br>
<p>Allows manage NSE scripts.</p>
<br>
<p align="center">
    <img width="500" title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/191381243-9813e2dd-b904-4856-8b8a-b42bb930c22a.png#gh-light-mode-only"/>
    <img width="500" title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/191381245-9d49f89e-e593-4bc1-b10a-c547efc25f49.png#gh-dark-mode-only"/>
</p>
<h4>Add script to favorites</h4>
<br>
<p>Allows add a script to favorites with ranking.</p>
<p align="center">
    <img width="700" title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/191383691-a9061a4c-484d-46c8-a7e5-fbf913cce79c.png#gh-light-mode-only"/>
    <img width="700" title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/191383695-09d4386c-68cd-4a2e-8e3a-bb5464b77c3c.png#gh-dark-mode-only"/>
</p>
<h3>Favorites Panel</h3>
<br>
<p>Allows update script ranking and delete favorites.</p>
<p align="center">
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/191387136-13826ebc-c53e-4620-824e-80f22d19d83c.png#gh-light-mode-only"/>
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/191387480-d118347f-e974-4880-a4d8-60c00ee866d9.png#gh-dark-mode-only"/>
</p>
