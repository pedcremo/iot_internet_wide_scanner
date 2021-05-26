import pandas as pd
import os 
import sys

PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from src.modules.utils import loadConfigFile, merge_files, uploadBannersELK
import subprocess
import shlex
import ast

def getBanners(daddr,sport,input_file, output_scans):
    
    try:
        
        catproces = subprocess.Popen(args=shlex.split('cat '+input_file), stdout=subprocess.PIPE)

        cmdline = ' zgrab2 multiple -c multiple.ini -o '+output_scans+'/out_zgrab_'+sport+'_'+daddr+'_.csv'  

        zgrab2_proc = subprocess.Popen(args=shlex.split(cmdline), 
                    stdin=catproces.stdout,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True, bufsize=0)
        
        catproces.wait()
        print(shlex.split(cmdline))    
        
    except OSError as e:
        print(e)
        raise EnvironmentError(1, "zgrab2 is not installed or could not be found in system path")

def main():
    # Read general config 
    gc = loadConfigFile()
    ports =  gc.get('SCANNER_CONFIG', 'ports')
    output_scans = gc.get('OUTPUT_PARTIAL_SCANS', 'path')

    # Get pandas dataframe from CSV
    df=pd.read_csv(output_scans+'/scanned_hosts.csv')
    #print(df)
    
    # For every port specified en general config we perform an scanning on networks supplied too in gc
    for port in ports.split():
        dfaux = df[df.sport == int(port)]
        
        protocols = ast.literal_eval(gc.get('BANNER_CONFIG', port))
        dfObj = pd.DataFrame(columns=['ip', 'empty', 'trigger'])
        
        for protocol in protocols:
            for index,row in dfaux.iterrows():                
                dfObj = dfObj.append({'ip': row['saddr'], 'empty': ' ', 'trigger': protocol+str(port)}, ignore_index=True)
        
        dfObj.to_csv(output_scans+"/input_zgrab_"+str(port)+".csv",index=False,header=False)
        getBanners(df['daddr'][0],port,output_scans+"/input_zgrab_"+str(port)+".csv",output_scans)

    # Scanning results merged in one .csv file 
    merge_files(output_scans+'/out_zgrab_*.csv',output_scans+'/banners_hosts.csv')

    # Upload all banner information to ElasticSearch
    uploadBannersELK(output_scans+'/out_zgrab_*.csv')

if __name__ == "__main__":
    main()


