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