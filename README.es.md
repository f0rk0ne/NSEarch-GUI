<h1 align="center">Nmap Scripting Engine Search GUI</h1>
<br/>
<p>
    Es un fork de la aplicación NSEarch de <a href="https://github.com/jtibaquira/nsearch">Jacobo Tibaquirá</a> de la comunidad
    <a href="https://www.dragonjar.org">DragonJAR</a>, el cuál integra una interfaz gráfica y agrega nuevos comandos.
</p>
<p align="center">
    <img title="NSEarch GUI temas" src="https://user-images.githubusercontent.com/77067446/189005578-f5e44412-dfa5-42e7-a0d0-dfeb49a6c318.png"/>
</p>
<br/>
<h2>Requerimientos</h2>

- [x] Python 3
- [x] python3-pyqt5
- [x] python3-pyqt5.qtwebkit
- [x] python-i18n
- [x] python3-yaml
- [x] python3-rich

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
    lang: "es" ; Idíoma de la aplicación
    scriptsPath: /usr/share/nmap/scripts/ ; Ruta de los scripts de Nmap
    filePath: /usr/share/nmap/scripts/script.db ; ruta del archivo de la BD de Nmap
    fileBackup: scriptbk.db ; Backup de la BD de Nmap
    scriptdb: nmap_scripts.sqlite3 ; Archivo de BD de la aplicación
    ; Categorías de los scripts de Nmap
    categories: ["auth","broadcast","brute","default","discovery","dos","exploit","external","fuzzer","intrusive","malware","safe","version","vuln"]
    checksum: 7c773a63720928125492e2034b7dcc445afb24c1555626ab710bd15db7bf82a3 ; Hash del archivo de la BD
    searchOnKey: 1 ; GUI activa la búsqueda al teclear en scripts y favoritos
    searchOpt: 3 ; GUI activa por defecto buscar por nombre o autor o categoría  
    theme: 1 ; GUI tema
    histLen: 100 ; el máximo de registros en el archivo history
    splashAnim: 0 ; Activa/Desactiva la animación en la SplashScreen
```
    
</details>
<details><summary><h2>Novedades</h2></summary>
<h3>Consola</h3>

- Al integrar el módulo Python rich, se incluyeron varias de las funcionalidades en la versión consola, por ejemplo resultados en columnas, animaciones al crear la BD entre otras.
- Se agrego el comando showcat que muestra las Categorías y permite listar los scripts en una categoría y al finalizar ver la ayuda de estos.
- Se agrego el comando history el cual permite visualizar el histórico de comandos ejecutados, muy similar al comando history de Linux.

</details>
<h2>GUI</h2>
<p>La GUI fue escrita en Python Qt5, y contiene dos QDockWidgets para gestionar los scripts y los favoritos.</p>
<p>Los contenidos de ayuda de los scripts se visualizan en formato HTML en pestañas.</p>
<p>La selección del idioma aplica para la versión consola también.</p>
<h3>Temas</h3>
<p>La GUI integra tres temas:</p>

- Oscuro
- Claro
- Predeterminado
