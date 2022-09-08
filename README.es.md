<h1 align="center">Nmap Scripting Engine Search GUI</h1>
<br/>
<p>Es un fork de la aplicación NSEarch de <a href="https://github.com/jtibaquira/nsearch">Jacobo Tibaquirá</a> de la comunidad <a href="https://www.dragonjar.org">DragonJAR</a>, el cuál integra una intefaz gráfica y agrega nuevos comandos.
</p>
<p align="center">
    <img title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/189005578-f5e44412-dfa5-42e7-a0d0-dfeb49a6c318.png"/>
</p>
<br/>
<h2>Requerimientos</h2>
<p>Python 3.9.2</p>
<p>python3-pyqt5</p>
<p>python3-pyqt5.qtwebkit</p>
<p>python-i18n</p>
<p>python3-yaml</p>
<br/>
<h2>Instalación</h2>
<p>
    Ejecutar install.sh para verificar e instalar los requerimientos de la aplicación.
</p>

```bash
sh install.sh
```

<details><summary><h2>Configuración</h2></summary>    
    <p>Una vez instaladas las dependencias de la aplicación, se inicia la creación de la base de datos de los scripts de Nmap y el archivo de configuración</p>
    <h3>Archivo de configuración</h3>
    
```yaml
config.yaml
config:
    ; Idíoma de la aplicación
    lang: "es"
    ; Ruta de los scripts de Nmap
    scriptsPath: /usr/share/nmap/scripts/
    ; ruta del archivo de la BD de Nmap
    filePath: /usr/share/nmap/scripts/script.db
    ; Backup de la BD de la aplicación
    fileBackup: scriptbk.db
    ; Archivo de BD de la aplicación
    scriptdb: nmap_scripts.sqlite3
    ; Categorías de los scripts de Nmap
    categories: ["auth","broadcast","brute","default","discovery","dos","exploit","external","fuzzer","intrusive","malware","safe","version","vuln"]
    ; Hash del archivo de la BD
    checksum: 7c773a63720928125492e2034b7dcc445afb24c1555626ab710bd15db7bf82a3
    ; GUI activa la búsqueda al teclear en scripts y favoritos
    searchOnKey: 1
    ; GUI activa por defecto buscar por
    searchOpt: 3
    ; El tema de la GUI
    theme: 1
    ; el máximo de registros en el archivo history
    histLen: 100
    ; Activa/Desactiva la animación en la SplashScreen
    splashAnim: 0
```
    
</details>
<details><summary><h2>Novedades</h2></summary>
<p></p>
</details>
