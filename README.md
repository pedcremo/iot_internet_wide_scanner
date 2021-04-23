# iot_internet_wide_scanner
It's a simple IOT internet wide scanner


# prerequisits
It is suposed that zmap and zgrab2 is installed on your system and in PATH

FOLLOW Instructions

Si podem instal·lar el zmap i el zgrab2 amb el sistema de paquets del teu sistema operatiu fes-ho.

Ex. En ubuntu fariem `sudo apt install zmap`

`
Fedora 19+ or EPEL 6+	sudo yum install zmap
Debian 8+ or Ubuntu 14.04+	sudo apt install zmap
Gentoo	sudo emerge zmap
macOS (using Homebrew)	brew install zmap
Arch Linux	sudo pacman -S zmap
`

NOTA: zgrab2 no està per a ubuntu 

Com compilar zmap si no tenim el paquet o el binari per al nostre sistema operatiu:
Clonem de github el projecte `git clone https://github.com/zmap/zmap`
Seguim instruccions de https://github.com/zmap/zmap/blob/master/INSTALL.md


Insta·lar zgrab2 https://github.com/zmap/zgrab2

- Una vegada instal·lat go entrem en  https://github.com/zmap/zgrab2 i llegim instruccions:
descarreguem codi font amb ‘go get github.com/zmap/zgrab2’
- export GOPATH=/home/pedcremo/go/
- Açò instal·larà zgrab2 en $GOPATH/src/github.com/zmap/zgrab2
- cd /home/pedcremo/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/
- make
- ln -s /home/pedcremo/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/zgrab2 /usr/bin/zgrab2

Prova: zgrab2 ftp -f inputFTP.csv -o outputFTP.csv


Per poder executar els scripts python del projecte 

Instal·lem llibreries de dependències d'aquests scripts 
sudo pip3 install -r requirements.txt
.......



We get as base
https://github.com/djet-sb/libzmap-python3/blob/master/libzmap/libzmap.py

# TODO
Per anotar geolocalització
https://github.com/zmap/zannotate
