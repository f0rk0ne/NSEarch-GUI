<p align="center">
    <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191133255-f501f351-5f7d-4da5-bf48-7f393456c6ad.gif#gh-light-mode-only"/>     <img title="NSEarch GUI" src="https://user-images.githubusercontent.com/77067446/191135554-410efda7-5348-4d55-a53c-e28cd0d13d7f.gif#gh-dark-mode-only"/>
</p>
<h1 align="center">Nmap Scripting Engine Search GUI</h1>
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
        <img src="https://user-images.githubusercontent.com/77067446/189161657-46ade1aa-723b-40e3-9c4c-70c14c362055.png"/>
</p>
<h4>Opciones</h4>
<br>

Opción | Tipo | Valores
 :-------- | :---- | :--------
Idioma | string | - "es" (Español)<br>- "en" (Ingles)
Tema | int | - 1 (Predeterminado)<br>- 2 (Oscuro)<br>- 3 (Claro)
Buscar al teclear | bool | - 1 (Activo)<br>- 0 (Desactivo)
Activar animación | bool | - 1 (Activo)<br>- 0 (Desactivo)
Opciones de búsqueda | int |- 1 (Nombre)<br>- 2 (Author)<br>- 3 (categoría)

</details>
<br>
<details><summary><h3>Panel Scripts</h3></summary>
<p>Permite gestionar los scripts NSE.</p>
<p align="center">   
    <img title="NSEarch panel scripts" src="https://user-images.githubusercontent.com/77067446/189177845-864da081-50bc-42de-99e3-389cab3f9c68.png"/>
</p>
<h4>Agregar script a favoritos</h4>
<p>Permite agregar un script a favoritos con un ranking.</p>
<p align="center">
    <img title="NSEarch Agregar script a favoritos" src="https://user-images.githubusercontent.com/77067446/189174323-2b75702e-e936-466c-a7af-aacbde47faae.png"/>
</p>
<br>
</details>
<br>
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
