MOST IMPORTANT: Change config_template.ini name to config.ini and fill real elasticsearch cretendials

# IOT internet wide scanner
It's a simple IOT internet wide scanner. Indeed, currently is only a wide open public IPv4 device scanner. So it scans wathever device behind a public IPv4 specified in general config.ini file independently whether is an IoT device or other type of device as a regular server, a workstation .... 

Similar to https://github.com/nray-scanner/nray

# Usar eines de manera ràpida i fàcil

# Usar la imatge directament de hub.docker.com (docker instal·lat al sistema i un elasticsearch en funcionament)
1. `docker pull pedcremo/iot-scanner-image:latest`
2. `git clone https://github.com/pedcremo/iot_internet_wide_scanner`
3. `cd iot_internet_wide_scanner`
4. El config.ini el tenim correctament configurat amb les xarxes/ports a escanejar i la instància Elasticsearch correctament configurada per poder enviar-li la informació dels escanejos i banner grabbing
5. `docker run -v "$(pwd)":/root/iot_wide_scanner/ --name test-container-iot -it pedcremo/iot-scanner-image /bin/bash` (Has d'executar aquest comandament des de l'arrel del projecte)
6. `python3 src/main.py` Executarà tots els dies per la nit. Has de comprovar que les dades arriben bé al teu Elasticsearch. Si aquest pas no funciona cal que executes algun comandament per forçar arp a descobrir la MAC del gateway. Alguna cosa tipus `apt update` 

# RUN manualment des del contenidor docker com a root.  
- Executar solament el port scanner -> `python3 src/modules/port_scanner/scanner.py`
- Executar solament el banner grabber(depends on port scanner) -> `python3 src/modules/banner_grabber/banner.py`
- Executar tot amb un planificador -> `python3 src/main.py`

# Si no volem usar docker el procés per usar aquestes eines és una mica més complex
- Primerament caldrà insta·lar zmap i zgrab2 al nostre sistema operatiu i han d'estar disponibles com a comandament en el PATH del sistema. Ço és, podrem executar comandament `zmap` o `zgrab2` des de qualsevol part del sistema. Mirar com instal·lar ambdós eines en les instruccions de més abaix.
- Hem de tindre instal·lada una instància de Elasticsearch i kibana llesta per usar i que conegam les seves credencials.Configurarem config.ini amb les credebcials d'ambdós eines
- Hem de tindre instal·lat python3 així com pip3 per instal·lar les dependències de llibreries que necessita aquest projecte. Instal·larem les dependències com root(sudoer) `sudo pip3 install -r requirements.txt` 
- Si tot ha funcionat correctament podrem executar el port scanner així `python3 src/modules/port_scanner/scanner.py`. Per l'eixida de consola comprovarem que estigui funcionant sense cap error i que estigui enviant correctament la informació a la nostra instància de Elasticsearch
- Després provarem el mòdul de banner grabbing `python3 src/modules/banner_grabber/banner.py`. Si també ha funcionat correctament procedirem al pas següent
- Si ja hem fet totes les comprovacions anteriors i tot funciona correctament amb `sudo python3 main.py` executarem tots els mòduls de manera periòdica totes les nits per recopilar informació de manera diaria


# INSTALL 
## EASY WAY
### DOCKER https://www.howtoforge.com/tutorial/how-to-create-docker-images-with-dockerfile/
Go to project root folder
With docker properly installed in your system, execute:
`docker build -t iot-scanner-image .`

List images with
`docker image ls`
and check iot-scanner-image appears in list

Execute the container and mount source code from local to execute last changes
`docker run -d -v /src:/opt/iot_wide_scanner --name test-container-iot iot-scanner-image`

Stop and/or remove container instance
`docker container stop test-container-iot` #Stop running container
`docker container rm test-container-iot` #Remove container 

Execute container in interactive mode to do some checkings/testings (PATH root project folder)
`docker run -v "$(pwd)":/root/iot_wide_scanner/ --name test-container-iot -it iot-scanner-image /bin/bash`

Execute scanner/banner grabing/metadata enricher (PATH root project folder)
`docker run -d -v "$(pwd)":/root/iot_wide_scanner/ --name test-container-iot -it iot-scanner-image`

# Pujar imatge a hub.docker.com

1. docker login (credencials de dockerhub)
2. docker tag iot-scanner-image:latest pedcremo/iot-scanner-image:latest (local remot)
3. docker push pedcremo/iot-scanner-image:latest



## HARD WAY DIY (do int yourself from scratch)
### INSTALL ZMAP (tool for scanning)
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


### INSTALL ZGRAB2 (tool for banner grabing)

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

Per detectar cameres amb RTSP
https://github.com/Ullaakut/cameradar

Ex: `docker run -t ullaakut/cameradar -t 185.81.77.235 -p1554`

- Definir TOC del TFM i anar perfilant
- Dockeritzar projecte Python port scanneri banner grabbing
- Fer alguna cosa d'annotació de tags ztag(obsolet) mirar si hi ha alguna eina a elastic
- Millorar codi

# References
https://github.com/djet-sb/libzmap-python3/blob/master/libzmap/libzmap.py


# Apunts per organitzar

Per obtindre certificat openssl s_client --connect 185.142.11.129:443
Per obtenir tots els rangs IPv4 públics del mòn `wget http://www.ipdeny.com/ipblocks/data/countries/cn.zone` 
`zmap -w cn.zone -p 80 -B 100M -o 80.res` #Escanegem tots els servers http del mòn
`/zgrab2 -input-file=80.res --output-file=hk.txt --senders=1000 http` #Extraiem els banner http


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

OJO: cat input.txt |zgrab2 multiple -c multiple.ini -o prova.csv
