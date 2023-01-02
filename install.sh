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
nmapversion=$(which nmap 2>/dev/null)
ispython=$(which python3 2>/dev/null)
python3version=$(python3 -V 2>/dev/null)
pipversion=$(which pip3 2>/dev/null)
sha256sum=$(which sha256sum 2>/dev/null)
sha256=$(which sha256 2>/dev/null)
kernel=$(uname -r)
os="$(uname -s) $kernel"
arch=$(uname -m)
vers=("11" "10" "9" "8" "7")
nsearchenv="NSEarchEnv"

function create_config_file(){
  checksum=
  dbpath=$(find /usr -type f -name "script.db" 2>/dev/null | awk 'gsub("script.db","")')
  if [[ $dbpath ]]; then
    filePath=$dbpath'script.db'
    if [[ $ismacox ]]; then
      printf "[+] CheckSum MacSOX....\n"
      checksum=$(sha256sum $filePath | awk '{print $4}')
    else
      printf "[+] CheckSum not MacSOX....\n"
      checksum=$(sha256sum $filePath | awk '{print $1}')
    fi
    lang=$(echo $LANG|cut -d_ -f1)
    printf "[+] Creating config.yaml file ...\n"
    printf "config: \n" > config.yaml
    printf "  scriptsPath: '$dbpath'\n" >> config.yaml
    printf "  filePath: '$filePath'\n" >> config.yaml    
    printf "  scriptdb: 'nmap_scripts.sqlite3'\n" >> config.yaml
    printf '  categories: ["auth","broadcast","brute","default","discovery","dos","exploit","external","fuzzer","intrusive","malware","safe","version","vuln"]\n' >> config.yaml
    printf "  checksum: '$checksum'\n" >> config.yaml
    printf "  histLen: 100\n" >> config.yaml
    printf "  lang: '$lang'\n" >> config.yaml
    printf "  searchOpt: 1\n" >> config.yaml
    printf "  searchOnKey: 1\n" >> config.yaml
    printf "  theme: 1\n" >> config.yaml
    printf "  splashAnim: 1\n" >> config.yaml
    printf "  singleTab: 1\n" >> config.yaml
    printf "  tabCount: 5" >> config.yaml
    chmod 777 config.yaml
  fi
  createLauncher
  printf "[+] NSEarch is ready for be launched uses python3 ./nsearch\n"
}

function createLauncher(){
  if [[ -f nsearch ]]; then
    rm nsearch
  fi
  if [[ -f nsearch_root ]]; then
    rm nsearch_root
  fi  
  pyversion=$(checkPythonVersion)  
  printf "#!/bin/bash\n" >> nsearch
  printf "source $nsearchenv/bin/activate\n" >> nsearch
  printf "$pyversion nsearch.py \$1\n" >> nsearch
  printf "deactivate\n" >> nsearch
  printf "#!/bin/bash\n" >> nsearch_root
  printf "sudo -E env PATH=\$PATH ./nsearch" >> nsearch_root
  chmod 777 nsearch*
}

function installPipRequeriments(){
  printf "[+] Creating environment for NSEarch ...\n"
  pythonbin=$(checkPythonVersion)
  "$pythonbin" -m venv $nsearchenv --prompt NSEarch
  "$pythonbin" -m pip install --upgrade pip
  source $nsearchenv/bin/activate
  "$pythonbin" -m pip install --upgrade pip
  printf "[+] Checking pip libs ...\n"
  "$pythonbin" -m pip install -r requirements.txt
  deactivate
}

function installpipDebian(){
  printf "[+] Installing pip ...\n"
  sudo apt-get install python3-pip -y
  installPipRequeriments
}

function installpipRedHat(){
  printf "[+] Installing pip ...\n"
  sudo yum install python3-pip -y  
  installPipRequeriments
}

function checkPythonVersion(){  
  for a in "${vers[@]}"; do
    if [ -f "/usr/bin/python3.$a" ] || [ -f "/usr/local/bin/python3.$a" ]; then
      printf "python3.$a"
      break
    fi
  done
}

function installPythonDebian(){  
  for b in "${vers[@]}"; do
    if [[ $(sudo apt-get search python3."$b") ]] ; then      
      sudo apt-get install -y python3."$b"
      printf "ok"   
      break
    fi
  done
}

function installPythonRedHat(){    
  for b in "${vers[@]}"; do
    if [[ $(sudo yum search python3"$b" 2>/dev/null) ]]; then
      sudo yum install -y python3"$b" 
      printf "ok"
      break
    elif [[ $(sudo yum search python3.$b 2>/dev/null) ]]; then
      sudo yum install -y python3.$b       
      printf "ok"
      break
    fi   
  done
}

function installPythonMacos(){
  for a in "${vers[@]}"; do
    if [[ $(brew search python3."$a") ]]; then
      brew install python@3."$a"
      printf "ok"
      break
    fi    
  done
}

if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ] ; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  sudo apt-get install sqlite3 fonts-noto-color-emoji python3-virtualenv qtwayland5 -y
  checkpip=0
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    sudo apt-get install nmap -y
  fi
  if [[ $ispython ]] && [[ $(checkPythonVersion) ]]; then
    printf "[+] Python is already installed :D\n"
    checkpip=1
  else
    echo "Installing python3.x ..."
    if [[ $(installPythonDebian) ]] ; then
      checkpip=1     
    else
      printf "Couldn't find a Python3 version compatible"
    fi
  fi
  if [ $checkpip -eq 1 ]; then
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments
    else
      installpipDebian
    fi
  fi
  create_config_file
elif [ -f /etc/redhat-release ]; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  sudo yum install google-noto-emoji-color-fonts epel-release python3-virtualenv sqlite-devel -y; sudo yum update -y;
  checkpip=0
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    sudo yum install nmap -y
  fi
  if [[ $ispython ]] && [[ $(checkPythonVersion) ]]; then
    printf "[+] Python is already installed :D\n"
    checkpip=1
  else
    echo "Installing python3.x ..."   
    if [[ $(installPythonRedHat) ]]; then
      checkpip=1      
    else
      printf "Couldn't find a Python3 version compatible"
      exit
    fi    
  fi
  if [ $checkpip -eq 1 ]; then
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments 
    else
      installpipRedHat
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
