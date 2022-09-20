<p align="center">
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191133255-f501f351-5f7d-4da5-bf48-7f393456c6ad.gif#gh-light-mode-only"/>     <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191135554-410efda7-5348-4d55-a53c-e28cd0d13d7f.gif#gh-dark-mode-only"/>
</p>
<h1 align="center">Motor de búsqueda de scripts Nmap</h1>
<br/>
<br>
<p>Es un fork de la aplicación NSEarch de <a href="https://github.com/jtibaquira/nsearch">Jacobo Tibaquirá</a> de la comunidad <a href="https://www.dragonjar.org">DragonJAR</a>, el cuál integra una interfaz gráfica y agrega nuevos comandos.
</p>
<p align="center">
    <img title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/191131576-cecee5ca-747a-4bc8-a101-947146268bb7.png"/>
</p>
<br/>
<h2>Requerimientos</h2>
<br/>

- [x] Python 3 ( Probado en 3.6, 3.9.2 y 3.10 )
- [x] python3-pyqt5
- [x] python3-pyqt5.qtwebkit ( Debian )
- [x] python36-pyqt5.qtwebkit ( Centos )
- [x] python-i18n
- [x] python3-yaml
- [x] python3-rich

<br/>
<h2>Instalación</h2>
<br/>
<p>Descargar y ejecutar install.sh con permisos root para verificar e instalar los requerimientos de la aplicación.</p>   

```bash
sudo git clone https://github.com/f0rk0ne/NSEarch-GUI.git 
```

```bash
sudo bash install.sh
```

<br>
<p>Ejecutar la primera vez con permisos root para crear la BD con los scripts de Nmap.</p>

```bash
sudo python3 nsearch.py
```

<br>
<p>Cambiar permisos de los archivos.</p>

```bash
sudo chown 1000:1000 -R * && sudo chmod 755 -R *
```

<br>
<h2>Configuración</h2>
<br/>
    <p>Una vez instaladas las dependencias de la aplicación, se inicia la creación de la base de datos de los scripts de Nmap y el archivo de configuración</p>
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
<h4>Opciones</h4>
<br>

Variable | Descripición | Tipo | Valores
 :----- | :---------- | :---- | :-------------
lang | Idioma | string | - "es" (Español)<br>- "en" (Ingles)
scriptsPath | Ruta scripts Nmap | string | Se agrega automáticamente
filePath | BD scripts Nmap | string | Se agrega automáticamente
fileBackup | Copia de seguridad Archivo BD | string | Se agrega automáticamente
scriptdb | BD NSEarch | string | Se agrega automáticamente
categories | Categorías de los scripts Nmap | list | ["auth","broadcast","brute","default","discovery",<br>"dos","exploit","external","fuzzer","intrusive",<br>"malware","safe","version","vuln"]
checksum | Sumatoria binaria BD NSEarch | string | Se agrega automáticamente
seachOnKey | Buscar al teclear | bool | - 1 (Activo)<br>- 0 (Desactivo)
searchOpt | Opciones de búsqueda | int |- 1 (Nombre)<br>- 2 (Author)<br>- 3 (categoría)
theme | Tema | int | - 1 (Predeterminado)<br>- 2 (Oscuro)<br>- 3 (Claro)
histLen | Tamaño en líneas del archivo hisorico | int | 100
splashAnim | Activar animación | bool | - 1 (Activo)<br>- 0 (Desactivo)

<br>
<h2>Novedades</h2>
<h3>Consola</h3>

- Al integrar el módulo Python rich, se incluyeron varias de las funcionalidades en la versión consola, por ejemplo resultados en columnas, animaciones al crear la BD entre otras.
- Se agrego el comando showcat que muestra las Categorías y permite listar los scripts en una categoría y al finalizar ver la ayuda de estos.
- Se agrego el comando history el cual permite visualizar el histórico de comandos ejecutados, muy similar al comando history de Linux.

<br>
<h2>GUI</h2>
<br>
<p>La GUI fue escrita en Python Qt5, y contiene dos QDockWidgets para gestionar los scripts y los favoritos.</p>
<p>Los contenidos de ayuda de los scripts se visualizan en formato HTML en pestañas.</p>
<p>La selección del idioma aplica para la versión consola también.</p>

<details><summary><h3>Configuración GUI</h3></summary>
<br>
<p>Permite establecer las opciones de la interfaz.</p>
<br>
<p align="center">
    <img title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/191139252-62ca128e-ab78-4497-b3d0-868eacf197f8.png#gh-light-mode-only"/>
    <img title="NSEarch GUI - Configuración" src="https://user-images.githubusercontent.com/77067446/191139255-0868c0ac-f8a2-4839-bfe3-84e82aaada8b.png#gh-dark-mode-only"/>
</p>
<br>
</details>
<details><summary><h3>Panel Scripts</h3></summary>
<br>
<p>Permite gestionar los scripts NSE.</p>
<br>
<p align="center">
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/191142595-77ad4afe-960d-4ea9-b5de-c6927bc500f7.png#gh-light-mode-only"/>
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/191142598-73e286d9-d56f-4842-9a68-f9c817f85a09.png#gh-dark-mode-only"/>
</p>
<h4>Agregar script a favoritos</h4>
<p>Permite agregar un script a favoritos con un ranking.</p>
<p align="center">
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/191145253-61fd8907-1dc2-4a44-8d27-cc05dbc74f56.png#gh-light-mode-only"/>
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/191145255-ce32737a-9a71-49b1-86de-d076ccf9c3b4.png#gh-dark-mode-only"/>
</p>
<br>
</details>
<details><summary><h3>Panel Favoritos</h3></summary>
<p>Permite gestionar los scripts favoritos.</p>
<p align="center">    
    <img title="NSEarch panel favoritos" src="https://user-images.githubusercontent.com/77067446/189177066-dc39edbe-cd3f-42e0-9d59-e9c4869fd501.png"/>   </p>
 <h4>Actualizar favoritos</h4>
 <p>Permite actualizar el ranking de un script favorito.</p>
 <p align="center">
    <img title="NSEarch actualizar favorito" src="https://user-images.githubusercontent.com/77067446/189179248-5805f7c4-23e9-45e8-8b51-6c8062feaa9f.png"/>    
 </p>
</details>
