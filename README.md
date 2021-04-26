# iot_internet_wide_scanner
It's a simple IOT internet wide scanner. Indeed, currently is only a wide open public IPv4 device scanner. So it scans wathever device behind a public IPv4 specified in general config independently whether is an IoT device or other type of device as a regular server, a workstation .... 

# Prerequisites
- It is suposed that zmap and zgrab2 is installed in your operating system and available in system PATH
- Install scripts libraries dependencies as root(sudoer) `sudo pip3 install -r requirements.txt` 
- Execute manually `sudo python3 scanner_module/scanner.py` and check scanning is working 
- If previous step works run `sudo python3 main.py` it will run all scripts using schedule specified in main.py

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

Insta·lar zgrab2 https://github.com/zmap/zgrab2

- Instal·lem go (llenguatge de programació) En ubuntu 20.04 `sudo apt install golang` . En Ubuntu 18.04 - Com insta·lar go en ubuntu https://www.digitalocean.com/community/tutorials/como-instalar-go-en-ubuntu-18-04-es
- export GOPATH=$HOME/go/
- Una vegada instal·lat go entrem en  https://github.com/zmap/zgrab2 i llegim instruccions:
descarreguem codi font amb ‘go get github.com/zmap/zgrab2’
- Açò instal·larà zgrab2 en $GOPATH/src/github.com/zmap/zgrab2
- cd /home/pedcremo/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/
- make
- ln -s /home/pedcremo/go/pkg/mod/github.com/zmap/zgrab2@v0.1.7/zgrab2 /usr/bin/zgrab2

Prova: zgrab2 ftp -f inputFTP.csv -o outputFTP.csv


# TODO
Per anotar geolocalització
https://github.com/zmap/zannotate

# References
https://github.com/djet-sb/libzmap-python3/blob/master/libzmap/libzmap.py


# Apunts per organitzar

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

