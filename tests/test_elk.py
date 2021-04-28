
from elasticsearch import helpers,Elasticsearch
import datetime 
import pandas as pd

es = Elasticsearch(['https://09e202a3f8d74639b610daccc8dd4608.eu-west-2.aws.cloud.es.io'],http_auth=('elastic','56voSDEDVyVMLUnj7GlPWZ1a'),scheme="https",port=9243)

'''
body = {
    'target_addr':'185.142.11.9',
    'scanning_addr':'test',
    'test':{'id':1,'name':'con'},
    'services':[
        {'port':8080,'protocol':'http','lastSeen_timestamp':datetime.datetime.now()},
        {'port':80,'protocol':'http','lastSeen_timestamp':datetime.datetime.now()},
        {'port':22,'protocol':'ssh','lastSeen_timestamp':datetime.datetime.now()}
    ],
    'lastScanned_timestamp': datetime.datetime.now()
}

es.index(index='test-scanning',doc_type = '_doc', body=body , request_timeout = 45, id = 1)

'''
def upsertElastic(index_name,json_body,id):
    global es     
    try:
        response = es.update(index=index_name,doc_type = '_doc', body=json_body , request_timeout = 45, id = id)
        print("response:",response)
    except Exception as err:
        print("Elasticsearch index() ERROR (in upsertElasticBeat):", err)

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
        
#df=pd.read_csv('scanned_hosts_test.csv')
df=pd.read_csv('scanned_hosts.csv')
#elastic_index_name = 'test-scanning'
elastic_index_name = 'wifibytes_scanned'

for index, row in df.iterrows():        
        
        '''doc_body = {
            "script":{
                "source":"ctx._source.services.add(params.service)",    
                "params":{
                    "service":{
                        "port":str(row['sport']),
                        "protocol":getService(str(row['sport'])),
                        'lastSeen_timestamp': datetime.datetime.now()
                    }
                }
            },
            "upsert":{
                "target_addr":row['saddr'],
                "scanning_addr":row['daddr'],
                "services":[
                    {
                        "port":str(row['sport']),
                        "protocol":getService(str(row['sport'])),
                        "lastSeen_timestamp":datetime.datetime.now()
                    }
                ],
                "lastScanned_timestamp": datetime.datetime.now()
            }
        }        

        upsertElastic(elastic_index_name,doc_body,hash(row['saddr']+row['daddr']+row['sport']))'''
        doc_body = {
                "target_addr":row['saddr'],
                "scanning_addr":row['daddr'],
                "port":str(row['sport']),
                "protocol":getService(str(row['sport'])),
                "lastScanned_timestamp": datetime.datetime.now()
        }
        putElasticBeat(elastic_index_name,doc_body,hash(row['saddr']+row['daddr']+str(row['sport'])))
