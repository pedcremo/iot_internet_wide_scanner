import subprocess
import shlex
import pandas as pd
import glob2 
import datetime 
import os 
import sys

PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from src.modules.utils import loadConfigFile 
from src.modules.utils import putElasticBeat,getService

# IMPORTANT NOTE: This script doesn't work without zmap installed on our system and available in system PATH # 

# Scan port (only one) in all networks supplied in networks parameter
# as a result we get a .csv outputfile with a line containing saddr,daddr,sport on opened host/port
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
        for streamline in iter(zmap_proc.stdout.readline, ''):                         
            print(streamline)
                    
    stderr = zmap_proc.stderr.read()
    print(stderr)
    
    zmap_rc = zmap_proc.poll()
    if zmap_rc is None:
        state = 'CANCELLED'
    elif zmap_rc == 0:
        state = 'DONE'
    else:
        state = 'FAILED'

# file_regex is the path with the regex to match .csv files to merge
# meanwhile all registers from merged .csv file is indexed in elasticsearch
def mergeAndIndexCSV_files(file_regex,elastic_index_name,output_csv_file):    
    all_filenames = [i for i in glob2.glob(file_regex)]        
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    '''
    for index, row in combined_csv.iterrows():               
        doc_body = {
                "target_addr":row['saddr'],
                "scanning_addr":row['daddr'],
                "port":str(row['sport']),
                "protocol":getService(str(row['sport'])),
                "lastScanned_timestamp": datetime.datetime.now()
        }
        putElasticBeat(elastic_index_name,doc_body,hash(row['saddr']+row['daddr']+str(row['sport'])))
    '''
    #export to csv
    combined_csv.to_csv(output_csv_file, index=False, encoding='utf-8-sig')


def main():
    # Read general config 
    gc = loadConfigFile()
    ports =  gc.get('SCANNER_CONFIG', 'ports')
    networks = gc.get('SCANNER_CONFIG', 'networks')
    output_scans = gc.get('OUTPUT_PARTIAL_SCANS', 'path')
    
    # Create output folder for partial results if not exists
    if not os.path.exists(output_scans):
        os.makedirs(output_scans)

    # Delete output temporal .csv files
    files = glob2.glob(output_scans+'/*.csv')
    print(files)
    for f in files:
        try:            
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


    # For every port specified en general config we perform an scanning on networks supplied too in gc
    for port in ports.split():
        scan(port,networks,output_scans+'/results'+port+'.csv') 

    # Scanning results merged in one .csv file and indexed in elasticsearch cluster
    mergeAndIndexCSV_files(output_scans+'/results*.csv',gc.get('ELASTIC_SERVER', 'index_name'),output_scans+'/scanned_hosts.csv')

if __name__ == "__main__":
    main()

