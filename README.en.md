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
    <img title="NSEarch GUI themes" src="https://user-images.githubusercontent.com/77067446/191378175-9fca005b-3c7e-4d4a-b089-e51828940945.png"/>
</p>
<br/>
<h2>Requirements</h2>
<br/>

- [x] Python 3 ( Tested in 3.6, 3.9.2 )
- [x] python-virtualenv
- [x] python3-pyqt5
- [x] python3-pyqt5.qtwebkit ( Debian )
- [x] python36-pyqt5.qtwebkit ( RHEL/centos )
- [x] python-i18n
- [x] python3-yaml
- [x] python3-rich

<br/>
<h2>Installation</h2>
<br/>
<p>
Download app from github repository and execute install.sh with root privileges to check and install requirements and to create the configuration file.
</p>   

```bash
sudo git clone https://github.com/f0rk0ne/NSEarch-GUI.git 
```

```bash
sudo bash install.sh
```

<br>
<p>Run first time with root privileges to create the Database with Nmap scripts.</p>

```bash
sudo ./nsearch
```

<br>


<br>
<h3>Manual Install</h3>
<br>

```bash
apt-get install -y openssl sqlite3 libsqlite3-dev fonts-noto-color-emoji python3-virtualenv
apt-get update -y && apt-get upgrade -y
```

```bash
yum install -y openssl-devel sqlite sqlite-devel google-noto-emoji-color-fonts epel-release python3-virtualenv
yum update -y && yum upgrade -y
```

```bash
python3.(6, 7, 8, 9) -m venv NSEarchEnv --prompt NSEarch
source NSEarchEnv/bin/activate
python3.(6, 7, 8, 9) -m pip install --upgrade pip
python3 -m pip install --user -r requirements.txt
deactivate
```

<br>
<h4>Run</h4>
<br>

```bash
source NSEarchEnv/bin/activate
python3 nsearch.py
```

<br>
<h2>Configuration</h2>
<br/>
<h3>Configuration File</h3>
<p>config.yaml</p>
    
```yaml
config:    
    lang: "es"
    scriptsPath: /usr/share/nmap/scripts/
    filePath: /usr/share/nmap/scripts/script.db
    fileBackup: scriptbk.db
    scriptdb: nmap_scripts.sqlite3
    categories: ["auth","broadcast","brute","default","discovery","dos","exploit","external","fuzzer","intrusive","malware","safe","version","vuln"]
    checksum: 7c773a63720928125492e2034b7dcc445afb24c1555626ab710bd15db7bf82a3
    searchOnKey: 1
    searchOpt: 3
    theme: 1
    histLen: 100
    splashAnim: 0
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
</table>
<br>
<h2>Changelog</h2>
<h3>Console</h3>

- Console version includes some rich python module features, such as results in columns, animations at startup between others.
- New command showcat shows categories and list all scripts in a category and shows scripts help too.
- New command history to see executed commands, like Linux history command.
- Now includes with emojis. 

<br>
<h2>GUI</h2>
<br>
<p>GUI was written in Python Qt5, and have two QDockWidgets to manage scripts and favorites.</p>
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
    <img width="400" title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/191378776-6b56a103-c352-4cbb-8609-12b1e67bd5ef.png#gh-light-mode-only"/>
    <img width="400" title="NSEarch GUI - Configuration" src="https://user-images.githubusercontent.com/77067446/191378778-86fa2f5b-8cb6-4201-bee9-ca6889897d92.png#gh-dark-mode-only"/>
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
