
from elasticsearch import helpers,Elasticsearch
import datetime 

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