import pandas as pd
from utils import loadConfigFile 
import subprocess
import shlex

df=pd.read_csv('./scanned_hosts.csv')
print(df)
# Read general config 
gc = loadConfigFile()
ports =  gc.get('SCANNER_CONFIG', 'ports')
output_scans = gc.get('OUTPUT_PARTIAL_SCANS', 'path')


def getServicePort(sport):
    ports_services = {
        '80': 'http',
        '443': 'tls',        
        '21': 'ftp',
        '22': 'ssh',
        '23': 'telnet',        
        '143': 'imap',
        '25': 'smtp'        
    }
    try:
        return ports_services[sport]
    except KeyError as e:
        return ""

def getBanners(daddr,sport,input_file):
    global output_scans
    try:
        #zgrab2 ftp -f inputFTP.csv -o outputFTP.csv
        service = getServicePort(sport)
        cmdline = 'zgrab2 '+service+' -f '+input_file+' -o '+output_scans+'/out_zgrab_'+service+'.csv'  

        zgrab2_proc = subprocess.Popen(args=shlex.split(cmdline), 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True, bufsize=0)
        print(shlex.split(cmdline))
    except OSError as e:
        print(e)
        raise EnvironmentError(1, "zgrab2 is not installed or could not be found in system path")


# For every port specified en general config we perform an scanning on networks supplied too in gc
for port in ports.split():
    dfaux = df[df.sport == int(port)]
    #print(dfaux)
    dfaux['saddr'].to_csv(output_scans+"/input_zgrab_"+str(port)+".csv",index=False,header=False)
    getBanners(df['daddr'][0],port,output_scans+"/input_zgrab_"+str(port)+".csv")
