import subprocess
import shlex
import pandas as pd
import datetime 
import os 
import sys
import glob2
import configparser

PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from src.modules.utils import loadConfigFile, uploadPortScanELK,mergeCSV_files 
from src.modules.utils import putElasticBeat,getService

# IMPORTANT NOTE: This script doesn't work without zmap installed on our system and available in system PATH # 

# Scan port (only one) in all networks supplied in networks parameter
# as a result we get a .csv outputfile with a line containing saddr,daddr,sport on opened host/port
def scan(port,networks,local_interface_name, outputfile):
    try:
        if local_interface_name is None:
            cmdline = 'zmap -p '+str(port)+' '+networks+' -f "saddr,daddr,sport"  --output-module=csv -o ' + outputfile
        else:    
            cmdline = 'zmap -i '+local_interface_name +' -p '+str(port)+' '+networks+' -f "saddr,daddr,sport"  --output-module=csv -o ' + outputfile
        
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



def main():
    # Read general config 
    gc = loadConfigFile()
    ports =  gc.get('SCANNER_CONFIG', 'ports')
    networks = gc.get('SCANNER_CONFIG', 'networks')
    try:
        local_interface_name = gc.get('SCANNER_CONFIG', 'local_interface_name')
    except (KeyError, configparser.NoOptionError):
        #We don't have that option enabled
        local_interface_name = None
    
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
        scan(port,networks,local_interface_name, output_scans+'/results'+port+'.csv') 

    # Scanning results merged in one .csv file 
    mergeCSV_files(output_scans+'/results*.csv',output_scans+'/scanned_hosts.csv')

    # Upload all port_scanning information to ElasticSearch
    uploadPortScanELK(output_scans+'/scanned_hosts.csv')

if __name__ == "__main__":
    main()

