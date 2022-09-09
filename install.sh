#!/usr/bin/env bash
printf "\n"
echo "=================================================";
echo " _   _  _____  _____                     _     ";
echo "| \ | |/  ___||  ___|                   | |    ";
echo "|  \| |\ \`--. | |__    __ _  _ __   ___ | |__  ";
echo "| . \` | \`--. \|  __|  / _\` || '__| / __|| '_ \ ";
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
paythonversion=$(which python3 2>/dev/null)
pipversion=$(which pip3 2>/dev/null)
sha256sum=$(which sha256sum 2>/dev/null)
sha256=$(which sha256 2>/dev/null)
kernel=$(uname -r)
os="$(uname -s) $kernel"
arch=$(uname -m)

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
    printf "  histLen: 100" >> config.yaml
    chmod 777 config.yaml
  fi
  printf "[+] NSEarch is ready for be launched uses python3 nsearch.py\n"
}
create_config_file
function installPipRequeriments(){
  printf "[+] Checking pip libs ...\n"
  pip install -r requirements.txt
}

function installpipDebian(){
  printf "[+] Installing pip ...\n"
  apt-get install python-pip3 -y
  installPipRequeriments
}

function installpipRedHat(){
  printf "[+] Installing pip ...\n"
  rpm -iUvh https://dl.fedoraproject.org/pub/epel/9/Everything/x86_64/Packages/e/epel-release-9-4.el9.noarch.rpm; yum -y update
  yum install python-pip3 -y
  installPipRequeriments
}

if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ] ; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  apt-get install unzip libreadline-gplv2-dev build-essential checkinstall unzip sqlite3 libsqlite3-dev python3-pyqt5 python3-pyqt5.qtwebkit -y  
  exit
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    apt-get install nmap -y
  fi

  if [[ $paythonversion ]]; then
    printf "[+] Python is already installed :D\n"
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments
    else
      installpipDebian
    fi
  else
    echo "Installing python3 ..."
    apt-get install python3 -y
    installpipDebian
  fi
  create_config_file
elif [ -f /etc/redhat-release ]; then
  printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
  yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel xz-devel python3-pyqt5 python3-pyqt5.qtwebkit -y
  if [[ $nmapversion ]]; then
    printf "\n[+] Nmap already installed :D \n"
  else
    echo "[+] Installing nmap .... "
    yum install nmap -y
  fi

  if [[ $paythonversion ]]; then
    printf "[+] Python is already installed :D\n"
    if [[ $pipversion ]]; then
      printf "[+] Pip3 is already installed :D\n"
      installPipRequeriments
    else
      installpipRedHat
    fi
  else
    echo "Installing python ..."
    yum install python3 -y
    installpipRedHat
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
  if [[ $paythonversion ]]; then
    printf "[+] Python is already installed :D\n"
    printf "[+] Pip is already installed :D\n"
    installPipRequeriments
  else
    echo "Installing python ..."
    brew install python -v
    printf "[+] Pip is already installed :D\n"
    installPipRequeriments
  fi
  create_config_file
else
  if [[ $nmapversion ]] && [[ $paythonversion ]] && [[ $pipversion ]]; then
    printf "[+] Checking Dependencies for $os ($arch $kernel)....\n"
    installPipRequeriments
    printf "[+] Requirement already satisfied ... \n"
    create_config_file
  else
    echo "[-] Could not find a autoinstall for $os ($arch $kernel)"
  fi
fi
