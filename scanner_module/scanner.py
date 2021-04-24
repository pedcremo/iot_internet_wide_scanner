

#from libzmap import ZmapProcess
import subprocess
import shlex
#import configparser
import pandas as pd
import glob2
from utils import loadConfigFile 
from utils import putElasticBeat 
import datetime 

def scan(port,networks,outputfile):
    try:
        cmdline = 'zmap -p '+str(port)+' '+networks+' -f "saddr,daddr,sport"  --output-module=csv -o ' + outputfile
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

# file_regex is the path with the regex to match files to merge
def mergeAndIndexCSV_files(file_regex,elastic_index_name):    
    all_filenames = [i for i in glob2.glob(file_regex)]        
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    for index, row in combined_csv.iterrows():        
        doc_body = {
            'saddr':row['saddr'],
            'daddr':row['daddr'],
            'sport':row['sport'],
            'last_seen': datetime.datetime.now()
        }        
        putElasticBeat(elastic_index_name,doc_body,row['saddr']+row['daddr'])        
    #export to csv
    combined_csv.to_csv( "scanned_hosts.csv", index=False, encoding='utf-8-sig')


def main():
    # Llegim arxiu de configuracio general
    gc = loadConfigFile()
    ports =  gc.get('SCANNER_CONFIG', 'ports')
    networks = gc.get('SCANNER_CONFIG', 'networks')
    output_scans = gc.get('OUTPUT_PARTIAL_SCANS', 'path')

    for port in ports.split():
        scan(port,networks,output_scans+'/results'+port+'.csv') 

    mergeAndIndexCSV_files(output_scans+'/results*.csv',gc.get('SCANNER_CONFIG', 'index_name'))

if __name__ == "__main__":
    main()