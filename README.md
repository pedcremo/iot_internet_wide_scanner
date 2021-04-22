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




Per poder executar els scripts python del projecte 

Instal·lem llibreries de dependències d'aquests scripts 
sudo pip3 install -r requirements.txt
.......



We get as base
https://github.com/djet-sb/libzmap-python3/blob/master/libzmap/libzmap.py