<p align="center">
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191317706-98de49f1-fdef-467e-b9c2-943fb8be9a9b.gif#gh-dark-mode-only"/>
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191317849-1d7c3138-ea05-4631-9295-3a5530266259.gif#gh-light-mode-only"/>
</p>
<h1 align="center">Motor de búsqueda de scripts Nmap</h1>
<br/>
<br>
<p>Es un fork de la aplicación NSEarch de <a href="https://github.com/jtibaquira/nsearch">Jacobo Tibaquirá</a> de la comunidad <a href="https://www.dragonjar.org">DragonJAR</a>, el cual integra una interfaz gráfica y agrega nuevos comandos.
</p>
<p align="center">    
    <img width="320" title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/211227761-b074f8c5-21bf-48d9-9c76-7b2201316f45.png"/>
    <img width="320" title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/211227760-578ee02c-c1f8-4c9c-97be-2209082baa2a.png"/>
    <img width="320" title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/211227758-c53c351d-23e7-4015-8ee8-c06bbd02976e.png"/>
</p>
<br/>
<h2>Requerimientos</h2>
<br/>

- [x] Python 3 (Probado en 3.7, 3.8, 3.9, 3.10)
- [x] python-venv o python3-virtualenv
- [x] pyside >= 6.4.1
- [x] python3-nmap
- [x] python-i18n
- [x] PyYAML
- [x] rich
- [x] requests 

<br/>
<h2>Instalación</h2>
<br/>
<p>Descargar y ejecutar install.sh para verificar e instalar los requerimientos de la aplicación y crear el archivo de configuración.</p>   

```bash
git clone https://github.com/f0rk0ne/NSEarch-GUI.git 
```

```bash
bash install.sh
```
<br>
<h3>Ejecutar</h3>
<br>

```bash
./nsearch
```

Cuando se requieran operaciones con privilegios root, por ejemplo, descargar los scripts NSE faltantes o ejecutar ciertos escaneos nmap.

```bash
./nsearch_root
o
sudo -E env PATH=$PATH ./nsearch
```

<br>
<h3>Instalación manual</h3>
<br>
<p>Dependiendo de la distribución de Linux es necesario instalar una versión de Python3 compatible con los módulos para la GUI, en el ejemplo se utiliza python3.9, pero también existen otras alternativas (python3.7, python3.8, python3.9, python3.10)</p>

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
<h4>Ejecución</h4>
<br>

```bash
source NSEarchEnv/bin/activate
python3 nsearch.py
deactivate
```

<br>
Si la consola no muestra los emojis, en el siguiente enlace se encuentra una solución <a href="https://www.reddit.com/r/linux/comments/ao0mp3/how_to_better_enable_color_emojis/#t1_efxvrmq">https://www.reddit.com/r/linux/comments/ao0mp3/how_to_better_enable_color_emojis/#t1_efxvrmq</a>
<br>
<br>
<h2>Configuración</h2>
<br/>
<h3>Archivo de configuración</h3>
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
    <th>Descripción</th>
    <th>Tipo</th>
    <th>Valores</th>        
</tr>
<tr>
    <td>lang</td>
    <td>Idioma</td>
    <td>string</td>
    <td>"es" (Español) <br> "en" (Ingles)</td>
</tr>
<tr>
    <td>seachOnKey</td>
    <td>Buscar al teclear</td>
    <td>bool</td>
    <td>1 (Activo)<br> 0 (Desactivo)</td>
</tr>
<tr>
    <td>searchOpt</td>
    <td>Opciones de búsqueda</td>
    <td>int</td>
    <td>1 (Nombre)<br> 2 (Autor)<br> 3 (categoría)</td>
</tr>
<tr>
    <td>theme</td>
    <td>Tema</td>
    <td>int</td>
    <td>1 (Predeterminado)<br> 2 (Oscuro)<br> 3 (Claro)</td>
</tr>
<tr>
    <td>histLen</td>
    <td>Tamaño en líneas del archivo histórico</td>
    <td>int</td>
    <td>100</td>
</tr>
<tr>
    <td>splashAnim</td>
    <td>Activar animación</td>
    <td>bool</td>
    <td>1 (Activo)<br> 0 (Desactivo)</td>
</tr>
<tr>
    <td>verticalTitle</td>
    <td>Muestra el título en modo vertical en la GUI</td>
    <td>bool</td>
    <td>1 (Activo)<br> 0 (Desactivo)</td>
</tr>
<tr>
    <td>singleTab</td>
    <td>Muestra la ayuda de los scripts NSE en una pestaña o varias pestañas</td>
    <td>bool</td>
    <td>1 (Activo)<br> 0 (Desactivo)</td>
</tr>
<tr>
    <td>tabCount</td>
    <td>Cuando la opción singleTab esta desactivada, indica cuantas pestañas se pueden cargar para mostrar la ayuda de los scripts NSE</td>
    <td>int</td>
    <td>5<br>10<br>20<br>30</td>
</tr>
</table>
<br>
<h2>Novedades</h2>
<h3>Consola</h3>

<p align="center">
<img width="320" title="NSEarch modo consola" src="https://user-images.githubusercontent.com/77067446/211227519-2306cf1e-bfb3-4718-ba3f-63ffe447d7b9.png">
<img width="320" title="NSEarch modo consola" src="https://user-images.githubusercontent.com/77067446/211227521-7198dcf0-4573-4b6d-a3ec-ec5473d3f342.png">
<img width="320" title="NSEarch modo consola" src="https://user-images.githubusercontent.com/77067446/211227523-c90cdb0b-af12-4303-88e3-7fe55dd3c0b7.png">
</p>

- La Base de datos ahora está incluida en el repositorio, ya que contiene todos los scripts de la web de nmap.
- Al integrar el módulo Python rich, se incluyeron varias de las funcionalidades en la versión consola, por ejemplo, resultados en columnas, animaciones al crear la BD entre otras.
- Se agregó el comando showcat que muestra las Categorías y permite listar los scripts en una categoría y al finalizar ver la ayuda de estos.
- Se agregó el comando history el cual permite visualizar el histórico de comandos ejecutados, muy similar al comando history de Linux.
- Se agregó el comando update el cual permite actualizar la BD y descargar los scripts NSE faltantes desde la página de <a href="https://www.nmap.org">nmap</a>
- Ahora incluye emojis.
- Se reintegró el comando run, en esta nueva versión del fork.

<br>
<h2>GUI</h2>
<br>
<p>La GUI fue escrita en Python Qt, y contiene dos QDockWidgets para gestionar los scripts y los favoritos.</p>
<p>Los contenidos de ayuda de los scripts se visualizan en formato HTML en pestañas.</p>
<p>La selección del idioma aplica para la versión consola también.</p>
<br>
<h3>Iniciar NSEarch GUI</h3>
<br>

```bash
./nsearch.py -g

```

<br>
<h3>Configuración GUI</h3>
<br>
<p>Permite establecer las opciones de la interfaz.</p>
<br>
<p align="center">
    <img title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/209732405-26109d10-4381-4621-ad87-2a33380d79bd.png#gh-dark-mode-only"/>
    <img title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/209732401-998a2bbd-e1e5-4bd7-9bc4-ea03b699ebd0.png#gh-light-mode-only"/>
</p>    
<h3>Panel Scripts</h3>
<br>
<p>Permite gestionar los scripts NSE.</p>
<br>
<p align="center">
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/211223950-12a56f96-d6d9-41a0-894d-91da69f05b15.png#gh-dark-mode-only">
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/211223951-d0fd9ef5-7f8a-42ac-90dd-3e77f39b2dba.png#gh-dark-mode-only">        
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/211213584-770c3faa-8e17-4007-9358-34f30b40ac94.png#gh-light-mode-only">
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/211213582-c6b11899-0a37-4013-a040-2182fc1a8319.png#gh-light-mode-only">
</p>
<h4>Agregar script a favoritos</h4>
<br>
<p>Permite agregar un script a favoritos con un ranking.</p>
<p align="center">         
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/211224216-d795c3cd-f13d-4412-9c89-612169fdfaf2.png#gh-dark-mode-only">    
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/211224215-b751407d-4c6a-46e2-8bed-8b3e4b067087.png#gh-dark-mode-only">      
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/211213904-015703a8-fd4f-42f6-a899-e57dc54159e2.png#gh-light-mode-only">
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/211213903-395bffb7-0756-40c7-ab00-d9f9732ee820.png#gh-light-mode-only">
</p>

<h3>Panel Favoritos</h3>
<br>
<p>Permite actualizar y eliminar los scripts favoritos.</p>
<p align="center">
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211224872-f05a206f-6e1e-4696-b0ae-6e40007a5aa0.png#gh-dark-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211224619-5f8efc14-729a-423d-befe-09ea31a42e0b.png#gh-dark-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211224620-67e3131d-3860-450e-a7fe-9133939194f5.png#gh-dark-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211214216-d3c073c2-5d80-4948-99c8-e1bc1776bdb5.png#gh-light-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211214215-888067c0-0ea1-4e8d-a3d3-16957d9db1c7.png#gh-light-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/211214214-660149a7-6e43-482b-9166-a17500ab721a.png#gh-light-mode-only"/>
</p>

<br>
<p>Para obtener información más detallada sobre la herramienta, visitar <a href="https://github.com/f0rk0ne/NSEarch-GUI/wiki/Documentacion-NSEarch">Wiki NSEarch GUI</a></p>
