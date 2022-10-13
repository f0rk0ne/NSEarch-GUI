#!/usr/bin/env bash
printf "\n"
echo "=================================================";
echo " _   _  _____  _____                     _     ";
echo "| \ | |/  ___||  ___|                   | |    ";
echo "|  \| |\ \`--. | |__    __ _  _ __   ___ | |___  ";
echo "| . \` | \`--. \|  __|  / _\` || '__| / __|| '_  |";
echo "| |\  |/\__/ /| |___ | (_| || |   | (__ | | | |";
echo "\_| \_/\____/ \____/  \__,_||_|    \___||_| |_|";
echo "=================================================";
echo " Version 1.0 https://bit.ly/3Rv9FNL @jjtibaquira";
echo " Email: jko@dragonjar.org  |   www.dragonjar.org";
echo "=================================================";
printf "\n"

ismacox=$(sw_vers 2>/dev/null)

#Check if is it root
if ! [ $(id -u) = 0 ] && ! [[ $ismacox ]] ; then
 echo "[-] You must be a root user" 2>&1
 exit 1
fi

nmapversion=$(which nmap 2>/dev/null)
ispython=$(which python3 2>/dev/null)
python3version=$(python3 -V 2>/dev/null)
pipversion=$(which pip3 2>/dev/null)
sha256sum=$(which sha256sum 2>/dev/null)
sha256=$(which sha256 2>/dev/null)
kernel=$(uname -r)
os="$(uname -s) $kernel"
arch=$(uname -m)
vers=("9" "8" "7" "6")
nsearchenv="NSEarchEnv"

function create_config_file(){
  checksum=
  dbpath=$(find /usr -type f -name "script.db" 2>/dev/null | awk 'gsub("script.db","")')
  if [[ $dbpath ]]; then
    filePath=$dbpath'script.db'
    if [[ $ismacox ]]; then
      printf "[+] CheckSum MacSOX....\n"
      checksum=$(sha256 $filePath | awk '{print $4}')
    else
      printf "[+] CheckSum not MacSOX....\n"
      checksum=$(sha256sum $filePath | awk '{print $1}')
    fi
    lang=$(echo $LANG|cut -d_ -f1)
    printf "[+] Creating config.yaml file ...\n"
    printf "config: \n" > config.yaml
    printf "  scripts_path: '$dbpath'\n" >> config.yaml
    printf "  filePath: '$filePath'\n" >> config.yaml
    printf "  fileBackup: 'scriptbk.db'\n" >> config.yaml
    printf "  scriptdb: 'nmap_scripts.sqlite3'\n" >> config.yaml
    printf '  categories: ["auth","broadcast","brute","default","discovery","dos","exploit","external","fuzzer","intrusive","malware","safe","version","vuln"]\n' >> config.yaml
    printf "  checksum: '$checksum'\n" >> config.yaml
    printf "  histLen: 100\n" >> config.yaml
    printf "  lang: '$lang'\n" >> config.yaml
    printf "  searchOpt: 1\n" >> config.yaml
    printf "  searchOnKey: 1\n" >> config.yaml
    printf "  theme: 1\n" >> config.yaml
    printf "  splashAnim: 1\n" >> config.yaml    
    chmod 777 config.yaml
  fi
  createLauncher
  printf "[+] NSEarch is ready for be launched uses python3 ./nsearch\n"
}

function createLauncher(){
  if [[ -f nsearch ]]; then
    rm nsearch
  fi
  printf "#!/bin/bash\n" >> nsearch
  printf "source $nsearchenv/bin/activate\n" >> nsearch
  printf "python3 nsearch.py \$1\n" >> nsearch
  printf "deactivate" >> nsearch
  chown 1000:1000 -R *
  chmod 777 -R *
}

function installPipRequeriments(){
  printf "[+] Installing virtualenv and creating environment ...\n"
  pythonbin=$(checkPythonVersion)
  "$pythonbin" -m venv $nsearchenv --prompt NSEarch
  "$pythonbin" -m pip install --upgrade pip
  source $nsearchenv/bin/activate
  printf "[+] Checking pip libs ...\n"
  "$pythonbin" -m pip install -r requirements.txt
  deactivate
}

function installpipDebian(){
  printf "[+] Installing pip ...\n"
  apt-get install python3-pip -y
  installPipRequeriments
}

function installpipRedHat(){
  printf "[+] Installing pip ...\n"
  yum install python3-pip -y  
  installPipRequeriments
}

function checkPythonVersion(){  
  for a in "${vers[@]}"; do
    if [ -f "/usr/bin/python3.$a" ]; then
      printf "python3.$a"
      break
    fi
  done
}

function installPythonDebian(){  
  for b in "${vers[@]}"; do
    if [[ $(apt-get search python3."$b") ]] ; then
      echo "Installing python3.$b ..."
      apt-get install -y python3."$b"
      printf "ok"   
      break
    fi
  done
}

function installPythonRedHat(){    
  for b in "${vers[@]}"; do
    if [[ $(yum search python3"$b" 2>/dev/null) ]]; then
      yum install -y python3"$b" 
      printf "ok"
      break
    elif [[ $(yum search python3.$b 2>/dev/null) ]]; then
      yum install -y python3.$b       
      printf "ok"
      break
    fi   
  done
}

function installPythonMacos(){
  for a in "${vers[@]}"; do
    if [[ $(brew search python3."$a") ]]; then
      brew install python3."$a"
      printf "ok"
      break
    fi
    if [[ $(brew search python3"$a") ]]; then
      brew install python3"$a"
      printf "ok"
      break
    fi
  done
}

if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ] ; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  apt-get install openssl sqlite3 libsqlite3-dev fonts-noto-color-emoji python3-virtualenv qtwayland5 -y
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    apt-get install nmap -y
  fi
  if [[ $ispython ]] && [[ $(checkPythonVersion) ]]; then
    printf "[+] Python is already installed :D\n"
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments
    else
      installpipDebian
    fi
  else
    echo "Installing python3.x ..."
    if [[ $(installPythonDebian) ]] ; then
      installpipDebian
    else
      printf "Couldn't find a Python3 version compatible"
    fi
  fi  
  create_config_file
elif [ -f /etc/redhat-release ]; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  yum install openssl-devel sqlite sqlite-devel google-noto-emoji-color-fonts epel-release python3-virtualenv -y; yum update -y;
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    yum install nmap -y
  fi
  if [[ $ispython ]] && [[ $(checkPythonVersion) ]]; then
    printf "[+] Python is already installed :D\n"
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments 
    else
      installpipRedHat
    fi
  else
    echo "Installing python3.x ..."
    if [[ $(installPythonRedHat) ]]; then
      installpipRedHat     
    else
      printf "Couldn't find a Python3 version compatible"
      exit
    fi    
  fi
  create_config_file
elif [[ $ismacox ]]; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  brew install -v sqlite3
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    brew install -v nmap
  fi
  if [[ $ispython ]] && [[ $(checkPythonVersion) ]]; then
    printf "[+] Python is already installed :D\n"
    printf "[+] Pip is already installed :D\n"
    installPipRequeriments
  else
    printf "Installing python 3.x ..."
    if [[ $(installPythonMacos) ]]; then
      printf "[+] Pip is already installed :D\n"
      installPipRequeriments
    else
      printf "Couldn't find a Python3 version compatible"
    fi 
  fi
  create_config_file
else
  if [[ $nmapversion ]] && [[ $ispython ]] && [[ $pipversion ]]; then
    printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
    installPipRequeriments
    printf "[+] Requirement already satisfied ... \n"
    create_config_file
  else
    echo "[-] Could not find a autoinstall for $os ($arch $kernel)"
  fi
fi
