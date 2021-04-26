import configparser
from elasticsearch import helpers,Elasticsearch
import datetime 
from datetime import date
#import csv 
import subprocess


def loadConfigFile():
    configParser = configparser.ConfigParser()   
    configParser.read('./config.ini')
    return configParser

gc = loadConfigFile()
endpoint = gc.get('ELASTIC_SERVER', 'endpoint')
username = gc.get('ELASTIC_SERVER', 'username')
password = gc.get('ELASTIC_SERVER', 'password')
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
        print("Elasticsearch index() ERROR (in putElasticBeat):", err)

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

def upsertElastic(index_name,json_body,id):
    global es     
    try:
        response = es.update(index=index_name,doc_type = '_doc', body=json_body , request_timeout = 45, id = id)
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index() ERROR (in upsertElasticBeat):", err)

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