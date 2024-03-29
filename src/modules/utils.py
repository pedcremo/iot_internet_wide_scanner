import configparser
from elasticsearch import helpers,Elasticsearch
import datetime 
from datetime import date, time
import subprocess
import os
import pandas as pd 
import glob2 
import json
import ast

def loadConfigFile():
    configParser = configparser.ConfigParser()   
    configParser.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))
    #configParser.read('config.ini')
    #print(os.path.dirname(__file__))
    return configParser

def generateMultipleIni(gc):    

    f = open(os.path.join(os.path.dirname(__file__), '../../multiple.ini'),'w')
    for (each_key,each_val) in gc.items('BANNER_CONFIG'):        
        port = each_key
        protocols = ast.literal_eval(each_val)
        for item in protocols:            
            if item=='https':
                s= '''
                    [http]
                    trigger="https{port_}"
                    name="https{port_}"
                    port={port_}
                    use-https=True'''.format(port_=port)
            else:
                s= '''
                    [{item_}]
                    trigger="{item_}{port_}"
                    name="{item_}{port_}"
                    port={port_}'''.format(port_=port,item_=item)

            f.write(s+"\n")
    f.close()

gc = loadConfigFile()
endpoint = gc.get('ELASTIC_SERVER', 'endpoint')
username = gc.get('ELASTIC_SERVER', 'username')
password = gc.get('ELASTIC_SERVER', 'password')
index_name = gc.get('ELASTIC_SERVER', 'index_name')
port = gc.get('ELASTIC_SERVER', 'port')
es = Elasticsearch([endpoint],http_auth=(username,password),scheme="https",port=port)
generateMultipleIni(gc)

def putElasticBeat(index_name,json_body,id):
    global es     
    try:
        response = es.index(
            index = index_name,
            doc_type = '_doc',
            body = json_body,
            request_timeout = 45,
            pipeline = 'wifibytes_user_geo',
            id = id
        )
        #print("response:",response)
    except Exception as err:
        print("Elasticsearch index(" + index_name + ") ERROR (in putElasticBeat):", err)

def uploadBannersELK(regex_path_banners):
    global index_name
    timestamp = datetime.datetime.now()
    dateStr = timestamp.strftime("%Y-%m-%d")

    # Delete output temporal .csv files
    files = glob2.glob(regex_path_banners)
    print("UPLOADING FILES "+str(files))
    for f in files:
        file1 = open(f, 'r')
        try:
            tokens = f.split("_")
            print(tokens)
            #service = tokens[2]
            port = tokens[2]
            grabbing_ip_source = tokens[3]

            Lines = file1.readlines()                 
            print("UPLOADING Arxiu "+f)
            for line in Lines:

                try:
                    dict_aux = json.loads(line)
                    #print(dict_aux)
                    if dict_aux['data']:
                       
                        llista = list(dict_aux['data'].keys())
                        print(llista)
                        #print(dict_aux['data'][llista[0]])
                        try:
                            json_body = {
                                "doc": {
                                    "banner.status": dict_aux['data'][llista[0]]['status'],
                                    "banner.protocol": dict_aux['data'][llista[0]]['protocol'],                                
                                    "banner.result": json.dumps(dict_aux['data'][llista[0]]['result']),                                
                                    "banner.timestamp": dict_aux['data'][llista[0]]['timestamp']
                                    
                                }
                            }
                        except KeyError:
                             json_body = {
                                "doc": {
                                    "banner.status": dict_aux['data'][llista[0]]['status'],
                                    "banner.protocol": dict_aux['data'][llista[0]]['protocol'],                                
                                    "banner.error": dict_aux['data'][llista[0]]['error'],
                                    "banner.timestamp": dict_aux['data'][llista[0]]['timestamp']                                    
                                }
                            }                                    
                        upsertElastic(index_name+"-"+dateStr,json_body,getId(dict_aux['ip']+grabbing_ip_source+port)) 
                
                except json.decoder.JSONDecodeError as jerr:
                    print ("Error parsing JSON "+line+" skipping...", jerr)

        except IndexError as errI:
             print("File not valid to index = "+f+" skipping...", errI)

def uploadPortScanELK(csv_path):
    global index_name
    df=pd.read_csv(csv_path)
    
    timestamp = datetime.datetime.now()
    dateStr = timestamp.strftime("%Y-%m-%d")

    for index, row in df.iterrows():               
        doc_body = {
                "destination.ip":row['saddr'],
                "source.ip":row['daddr'],
                "destination.port":str(row['sport']),
                #"protocol":getService(str(row['sport'])),
                "@timestamp": timestamp
        }
        putElasticBeat(index_name+"-"+dateStr,doc_body,getId(row['saddr']+row['daddr']+str(row['sport'])))
    
def getId(targetIp_sourceIp_targetPort):    
    return targetIp_sourceIp_targetPort

def upsertElastic(index_name,json_body,id):
    global es     
    try:
        #timestamp = datetime.datetime.now()
        #dateStr = timestamp.strftime("%Y-%m-%d")
        response = es.update(index=index_name,doc_type = '_doc', body=json_body , request_timeout = 45, id = id)
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index("+index_name+") ERROR (in upsertElasticBeat):", err)

# file_regex is the path with the regex to match .csv files to merge
# meanwhile all registers from merged .csv file is indexed in elasticsearch
def mergeCSV_files(file_regex,output_csv_file):    
    all_filenames = [i for i in glob2.glob(file_regex)]        
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv    
    combined_csv.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

# Merge several .txt files in ONE
def merge_files(file_regex,output_csv_file):    
    all_filenames = [i for i in glob2.glob(file_regex)]
    print("MERGING ",all_filenames)
    with open(output_csv_file, 'w') as outfile:
        for fname in all_filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
