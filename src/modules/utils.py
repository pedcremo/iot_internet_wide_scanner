import configparser
from elasticsearch import helpers,Elasticsearch
import datetime 
from datetime import date
import subprocess
import os
import pandas as pd 
import glob2 

def loadConfigFile():
    configParser = configparser.ConfigParser()   
    configParser.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))
    #configParser.read('config.ini')
    #print(os.path.dirname(__file__))
    return configParser

gc = loadConfigFile()
endpoint = gc.get('ELASTIC_SERVER', 'endpoint')
username = gc.get('ELASTIC_SERVER', 'username')
password = gc.get('ELASTIC_SERVER', 'password')
index_name = gc.get('ELASTIC_SERVER', 'index_name')
port = gc.get('ELASTIC_SERVER', 'port')
es = Elasticsearch([endpoint],http_auth=(username,password),scheme="https",port=port)

'''def uploadCsvElastic(index_name, csv_path):
    global es
    dateStr = date.today().strftime("%d.%m.%Y")
    try:
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            helpers.bulk(es, reader, index=index_name+'-'+dateStr)
    except Exception as err:
        print("Elasticsearch index() ERROR (in uploadCsvElastic):", err)
'''
def putElasticBeat(index_name,json_body,id):
    global es     
    try:
        response = es.index(
            index = index_name,
            doc_type = '_doc',
            body = json_body,
            request_timeout = 45,
            id = id
        )
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index(" + index_name + ") ERROR (in putElasticBeat):", err)

def addServiceElasticBeat(index_name,port,protocol,banner,id):
    global es
    try:
        update_query= {
            'script':{
                'source':'ctx._source.services.add(params.service)',    
                'params':{
                    'service':{
                        'port':port,
                        'protocol':protocol,
                        'banner':banner,
                        'lastSeen_timestamp': datetime.datetime.now()
                    }
                }
            }
        }
        response = es.update(index=index_name,doc_type = '_doc', body=update_query , request_timeout = 45, id = id)
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index() ERROR (in putElasticBeat):", err)


def uploadBannersELK(daddr,service,port,fileWithBanners):
    global index_name
    # Using readlines()    
    file1 = open(fileWithBanners, 'r')
    Lines = file1.readlines()
 
    count = 0
    # Strips the newline character
    for line in Lines:
        #count += 1
        #print("Line{}: {}".format(count, line.strip()))
        json_body = {
            "script" : "ctx._source.banner_"+service+" = "+line.strip()
        }
        dict_aux = line
        print(dict_aux['ip'])
        id = hash(line.strip()['ip']+daddr+str(port))
        upsertElastic(index_name,jsdoc,int(id) )


def uploadPortScanELK(csv_path):
    global index_name
    df=pd.read_csv(csv_path)
    
    for index, row in df.iterrows():               
        doc_body = {
                "target_addr":row['saddr'],
                "scanning_addr":row['daddr'],
                "port":str(row['sport']),
                "protocol":getService(str(row['sport'])),
                "lastScanned_timestamp": datetime.datetime.now()
        }
        putElasticBeat(index_name,doc_body,hash(row['saddr']+row['daddr']+str(row['sport'])))
    

def upsertElastic(index_name,json_body,id):
    global es     
    try:
        response = es.update(index=index_name,doc_type = '_doc', body=json_body , request_timeout = 45, id = id)
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index() ERROR (in upsertElasticBeat):", err)

# file_regex is the path with the regex to match .csv files to merge
# meanwhile all registers from merged .csv file is indexed in elasticsearch
def mergeCSV_files(file_regex,output_csv_file):    
    all_filenames = [i for i in glob2.glob(file_regex)]        
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    print("OUTPUT_CSV_FILE = "+output_csv_file)
    combined_csv.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

# Merge several .txt files in ONE
def merge_files(file_regex,output_csv_file):    
    all_filenames = [i for i in glob2.glob(file_regex)]

    with open(output_csv_file, 'w') as outfile:
        for fname in all_filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def getService(port):   
    ports_services = {
        '80': 'http',
        '443': 'https',
        '8080': 'http',
        '8443': 'https',
        '21': 'ftp',
        '22': 'ssh',
        '23': 'telnet',
        '161': 'snmp',
        '143': 'imap',
        '25': 'smtp',
        '5060': 'sip',
        '554': 'rtsp'
    }
          
    return ports_services[port]