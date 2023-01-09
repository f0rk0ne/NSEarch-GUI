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
    <img width="320" title="NSEarch GUI themes" src="https://user-images.githubusercontent.com/77067446/211228408-6e5eb4a3-174c-4677-afb4-781ed463bd9e.png"/>
    <img width="320" title="NSEarch GUI themes" src="https://user-images.githubusercontent.com/77067446/211228409-d7f6ca3f-d843-4565-b2c1-c0c4e03e228b.png"/>
    <img width="320" title="NSEarch GUI themes" src="https://user-images.githubusercontent.com/77067446/211228410-ba08feb6-8433-4970-a577-2d506582c37b.png"/>
</p>
<br/>
<h2>Requirements</h2>
<br/>

- [x] Python 3 (Tested in 3.7, 3.8, 3.9, 3.10)
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

<p align="center">
<img width="320" title="NSEarch Console mode" src="https://user-images.githubusercontent.com/77067446/211228697-174a11ea-50bc-427e-a082-026efdee8061.png"/>
<img width="320" title="NSEarch Console mode" src="https://user-images.githubusercontent.com/77067446/211228699-b49d2353-4568-404a-88c6-44e511090cac.png"/>
<img width="320" title="NSEarch Console mode" src="https://user-images.githubusercontent.com/77067446/211228701-bbead606-c315-476b-8925-936db4acb043.png"/>
</p>

- Database now is included in the repository, thus contains all NSE scripts from nmap web.
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
    <img title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/209881076-220a92a8-77dc-4821-bc3d-6b5c5146a3f5.png#gh-light-mode-only"/>
    <img title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/209881075-16c1062b-e3b7-4896-a321-d0184118e1da.png#gh-dark-mode-only"/>
</p>
<h3>Scripts Panel</h3>
<br>
<p>Allows manage NSE scripts.</p>
<br>
<p align="center">
    <img title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/211229762-b1bf9e87-2fe2-4e17-bd84-3f4bf3cb8c18.png#gh-dark-mode-only"/>
    <img title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/211229950-6671b761-b392-4644-a5d6-7246ebbc707f.png#gh-dark-mode-only"/>
    <img title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/211229792-878c636a-74ac-4978-b65f-30bb6bb4bdd0.png#gh-light-mode-only"/>
    <img title="NSEarch scripts panel" src="https://user-images.githubusercontent.com/77067446/211229794-ac089972-59a7-4d7f-b6b7-596abbfbc6a2.png#gh-light-mode-only"/>
</p>
<h4>Add script to favorites</h4>
<br>
<p>Allows add a script to favorites with ranking.</p>
<p align="center">
    <img title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/211230680-be8e2c4e-3f80-4e1a-a521-3bc21a04ca98.png#gh-dark-mode-only"/>
    <img title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/211230681-a717528f-0d56-417f-bae8-35f65554d0f6.png#gh-dark-mode-only"/>   
    <img title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/211230712-269c566b-0a56-4ebc-b5d8-db08d1677e37.png#gh-light-mode-only"/>    
    <img title="NSEarch add script to favorites" src="https://user-images.githubusercontent.com/77067446/211230714-3fc47bda-557e-4f78-900d-a0955cb9265d.png#gh-light-mode-only"/>    
</p>
<h3>Favorites Panel</h3>
<br>
<p>Allows update script ranking and delete favorites.</p>
<p align="center">
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231841-681905f7-f69a-4ad9-a5c0-b7a615f2d8a3.png#gh-dark-mode-only"/>
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231931-1cff1272-47e8-477f-8487-92454f3e5fea.png#gh-dark-mode-only"/>
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231980-1148dcbb-ea98-4f0e-b2b8-17d1a171280e.png#gh-dark-mode-only"/>    
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231705-1ec62bfa-8d23-4030-972d-779404be52d3.png#gh-light-mode-only"/>
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231706-63b7d756-d49f-4612-8b8f-4dc601664f5d.png#gh-light-mode-only"/>    
    <img title="NSEarch favorites panel" src="https://user-images.githubusercontent.com/77067446/211231708-81c2af98-3208-4cbf-8aa4-e2d5c3247849.png#gh-light-mode-only"/>
</p>
