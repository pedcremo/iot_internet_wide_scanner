#from libzmap import ZmapProcess
import subprocess
import shlex
import configparser

def scan(port,networks):

    try:
        cmdline = 'zmap -p '+str(port)+' '+networks+' -f "saddr,daddr,sport"  --output-module=csv -o out/results'+str(port)+'.csv'
        zmap_proc = subprocess.Popen(args=shlex.split(cmdline), 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True, bufsize=0)
        print(shlex.split(cmdline))
    except OSError as e:
        print(e)
        raise EnvironmentError(1, "zmap is not installed or could not be found in system path")

    while zmap_proc.poll() is None:
        print("ARRE GAT")
        for streamline in iter(zmap_proc.stdout.readline, ''): 
            print("ARRE GAT 2")               
            print(streamline)
                    
    stderr = zmap_proc.stderr.read()

    print(stderr)
    # print self.__stderr
    zmap_rc = zmap_proc.poll()
    if zmap_rc is None:
        state = 'CANCELLED'
    elif zmap_rc == 0:
        state = 'DONE'
    else:
        state = 'FAILED'

configParser = configparser.ConfigParser()   
configParser.read('config.ini')
ports =  configParser.get('SCANNER_CONFIG', 'ports')
networks = configParser.get('SCANNER_CONFIG', 'networks')


for port in ports.split():
    scan(port,networks) 

'''scan(80,'185.142.10.0/22 185.81.76.0/22 195.181.255.0/24 212.237.255.0/24 80.209.255.0/24 95.214.108.0/22  95.214.109.0/24')
scan(443,'185.142.10.0/22 185.81.76.0/22 195.181.255.0/24 212.237.255.0/24 80.209.255.0/24 95.214.108.0/22  95.214.109.0/24')
scan(21,'185.142.10.0/22 185.81.76.0/22 195.181.255.0/24 212.237.255.0/24 80.209.255.0/24 95.214.108.0/22  95.214.109.0/24')'''
