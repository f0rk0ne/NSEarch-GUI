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
<img title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/191131576-cecee5ca-747a-4bc8-a101-947146268bb7.png"/>
</p>
<br/>
<h2>Requerimientos</h2>
<br/>

- [x] Python 3 ( Probado en 3.6, 3.9.2 y 3.10 )
- [x] python-virtualenv 
- [x] python3-pyqt5
- [x] python3-pyqt5.qtwebkit ( Debian )
- [x] python36-pyqt5.qtwebkit ( Centos )
- [x] python-i18n
- [x] python3-yaml
- [x] python3-rich

<br/>
<h2>Instalación</h2>
<br/>
<p>Descargar y ejecutar install.sh con permisos root para verificar e instalar los requerimientos de la aplicación y crear el archivo de configuración.</p>   

```bash
sudo git clone https://github.com/f0rk0ne/NSEarch-GUI.git 
```

```bash
sudo bash install.sh
```

<br>
<p>Ejecutar la primera vez con permisos root para crear la BD con los scripts de Nmap.</p>

```bash
sudo ./nsearch
```

<br>
<p>Cambiar permisos de los archivos.</p>

```bash
sudo chown 1000:1000 -R * && sudo chmod 755 -R *
o
sudo chown 1000:1000 -R NSEarch-GUI && sudo chmod 755 -R NSEarch-GUI
```

<br>
<h2>Configuración</h2>
<br/>
<h3>Archivo de configuración</h3>
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
</table>
<br>
<h2>Novedades</h2>
<h3>Consola</h3>

- Al integrar el módulo Python rich, se incluyeron varias de las funcionalidades en la versión consola, por ejemplo resultados en columnas, animaciones al crear la BD entre otras.
- Se agregó el comando showcat que muestra las Categorías y permite listar los scripts en una categoría y al finalizar ver la ayuda de estos.
- Se agregó el comando history el cual permite visualizar el histórico de comandos ejecutados, muy similar al comando history de Linux.
- Ahora incluye emojis.

<br>
<h2>GUI</h2>
<br>
<p>La GUI fue escrita en Python Qt5, y contiene dos QDockWidgets para gestionar los scripts y los favoritos.</p>
<p>Los contenidos de ayuda de los scripts se visualizan en formato HTML en pestañas.</p>
<p>La selección del idioma aplica para la versión consola también.</p>
<br>
<h3>Iniciar NSEarch GUI</h3>
<br>

```bash
./nsearch.py

```

<br>
<h3>Configuración GUI</h3>
<br>
<p>Permite establecer las opciones de la interfaz.</p>
<br>
<p align="center">
    <img width="400" title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/191139252-62ca128e-ab78-4497-b3d0-868eacf197f8.png#gh-light-mode-only"/>
    <img width="400" title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/191139255-0868c0ac-f8a2-4839-bfe3-84e82aaada8b.png#gh-dark-mode-only"/>
</p>    
<h3>Panel Scripts</h3>
<br>
<p>Permite gestionar los scripts NSE.</p>
<br>
<p align="center">
    <img width="500" title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/191142595-77ad4afe-960d-4ea9-b5de-c6927bc500f7.png#gh-light-mode-only"/>
    <img width="500" title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/191142598-73e286d9-d56f-4842-9a68-f9c817f85a09.png#gh-dark-mode-only"/>
</p>
<h4>Agregar script a favoritos</h4>
<br>
<p>Permite agregar un script a favoritos con un ranking.</p>
<p align="center">         
    <img width="700" title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/191146139-a331c7a9-d4ac-40bd-95a4-dd3304d041e6.png#gh-light-mode-only"/>
    <img width="700" title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/191145255-ce32737a-9a71-49b1-86de-d076ccf9c3b4.png#gh-dark-mode-only"/>
</p>
<h3>Panel Favoritos</h3>
<br>
<p>Permite actualizar y eliminar los scripts favoritos.</p>
<p align="center">    
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/191157139-401aa8fb-cf99-43e9-aab9-8e748f1a48e3.png#gh-light-mode-only"/>
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/191157141-52df45d0-be96-4d36-a82d-cb57798e6301.png#gh-dark-mode-only"/>
</p>
