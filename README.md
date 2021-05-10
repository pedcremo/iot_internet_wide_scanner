IMPORTANT: Change config_template.ini name to config.ini and fill real elasticsearch cretendials

# iot_internet_wide_scanner
It's a simple IOT internet wide scanner. Indeed, currently is only a wide open public IPv4 device scanner. So it scans wathever device behind a public IPv4 specified in general config.ini file independently whether is an IoT device or other type of device as a regular server, a workstation .... 

Similar to https://github.com/nray-scanner/nray

# Prerequisites
- It is suposed that zmap and zgrab2 is installed in your operating system and available in system PATH (Instructions in document)
- It is suposed we have an instance of elasticsearch and kibana installed and ready to use
- Install scripts python libraries dependencies as root(sudoer) `sudo pip3 install -r requirements.txt` 
- Execute manually `sudo python3 scanner_module/scanner.py` and check scanning is working (NOTE )
- If previous step works run `sudo python3 main.py` it will run all scripts using schedule specified in main.py

# RUN
- port scanner -> `sudo python3 src/modules/port_scanner/scanner.py`
- banner grabber(depends on port scanner) -> `sudo python3 src/modules/banner_grabber/banner.py`

## INSTALL ZMAP (tool for scanning)
We can find easily zmap as a package ready to install for our Operating system 
In ubuntu 20.04 it will be as:
Ex. `sudo apt install zmap`

Fedora 19+ or EPEL 6+	`sudo yum install zmap`
Debian 8+ or Ubuntu 14.04+	`sudo apt install zmap`
Gentoo	`sudo emerge zmap`
macOS (using Homebrew)	`brew install zmap`
Arch Linux	`sudo pacman -S zmap`

If zmap is not available as an installable package or is a very old version for your OS you always can compile it.
It's open source.

Clone github project `git clone https://github.com/zmap/zmap`
Follow instructions from file https://github.com/zmap/zmap/blob/master/INSTALL.md


## INSTALL ZGRAB2 (tool for banner grabing)

NOTE: zgrab2 is not available for Ubuntu 

Insta·lar zgrab2 des de codi en https://github.com/zmap/zgrab2

Primerament necessitem el llenguatge de programació go i el seu compilador instal·lat al sistema per poder instal·lar zgrab2
Passem d'instal·lar els paquets oficials que venen al sistema operatiu (anem a baixar directament de golang.org go 1.16.3 o superior)
https://golang.org/doc/install

- cd /tmp
- wget -d https://golang.org/dl/go1.16.3.linux-amd64.tar.gz
- sudo rm -rf /usr/local/go
- sudo tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz
- export PATH=$PATH:/usr/local/go/bin (add to the end of file $HOME/.profile)
- source $HOME/.profile
- execute `go version` i ha de coincidir amb la versió descarregada amb wget al segon pas
- Després d'aquestos passos procedim a la instal·lació del zgrab2 amb `go get github.com/zmap/zgrab2`
- `cd $HOME/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7`
- En aquest pas he tingut que passar-me a root `su root` fer `export PATH=$PATH:/usr/local/go/bin`
- `make` (com a root)
- `sudo ln -s $HOME/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/zgrab2 /usr/bin/zgrab2` (com a usuari sudoer)
- Ara el comandament zgrab2 ha d'estar al PATH del sistema i al executar `zgrab2` ens apareixerà quelcom com:

''' Please specify one command of: bacnet, banner, dnp3, fox, ftp, http, imap, ipp, modbus, mongodb, mssql, multiple, mysql, ntp, oracle, pop3, postgres, redis, siemens, smb, smtp, ssh, telnet or tls
FATA[0000] could not parse flags: Please specify one command of: bacnet, banner, dnp3, fox, ftp, http, imap, ipp, modbus, mongodb, mssql, multiple, mysql, ntp, oracle, pop3, postgres, redis, siemens, smb, smtp, ssh, telnet or tls '''    


Prova: zgrab2 ftp -f inputFTP.csv -o outputFTP.csv


# TODO
Per anotar geolocalització
https://github.com/zmap/zannotate

# References
https://github.com/djet-sb/libzmap-python3/blob/master/libzmap/libzmap.py


# Apunts per organitzar
LLEGIR article Abnormal Behavior-Based Detection of Shodan and Censys-Like Scanning


https://www.elastic.co/es/blog/elasticsearch-and-siem-implementing-host-portscan-detection

https://www.elastic.co/es/blog/using-nmap-logstash-to-gain-insight-into-your-network
https://www.elastic.co/guide/en/logstash/2.2/plugins-codecs-nmap.html

Llegir https://elastic.co/guide/en/elasticsearch/reference/master/docs-update.html

INSERT
body = {
    "target_addr":"185.142.11.9",
    "scanning_addr":"test",
    "services":[
        "8080":{
            "port":8080,
            "protocol":"http",
            "lastSeen_timestamp":datetime.datetime.now()
        }
    ],
    "lastScanned_timestamp": datetime.datetime.now()
}

es.index(index='test-scanning',doc_type = '_doc', body=body , request_timeout = 45, id = 1)


UPDATE 
bodyU ={"script":{
    "source":"ctx._source.services.add(params.service)",    
    "params":{
        "service":{
            "port":80,
            "protocol":"http",
            'lastSeen_timestamp': datetime.datetime.now()
          }
      }
    }
}

            
DELETE 
body2 ={"script":{
    "source":"if (ctx._source.services.contains(params.service)) { ctx._source.services.remove(ctx._source.services.indexOf(params.service)) }",    
    "params":{
      "service":{            
        "port": 8080            
       }
      }
    }
}

 
es.update(index='test-scanning',doc_type = '_doc', body=body , request_timeout = 45, id = 1)


Eina en javascript similar a zgrab2 https://github.com/chichou/grab.js


* List of Banner Grabbing Tools

Netcat
telnet
Netcraft
http recon
ID Serve
Recon-ng
Uniscan
SpiderFoot
httprint
Nmap
ScanLine
X probe
P0f
Satori
Thanos
Bannergrab
synscan
Disco
Winfingerprint
NetworkMiner