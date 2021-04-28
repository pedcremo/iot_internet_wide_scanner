'''
 Dnspython is a 
 DNS toolkit for Python. It can be used for queries, 
 zone transfers, dynamic updates, nameserver testing, 
 and many other things. https://www.dnspython.org/
'''

import dns.reversename
import dns.resolver
import pandas as pd

data = pd.read_csv("./scanned_hosts.csv") 
print(data)

for index, row in data.iterrows():    
    n = dns.reversename.from_address(row['saddr'])
    #print(n)
    #print(dns.reversename.to_address(n))

    try:
        result = dns.resolver.resolve(n, 'PTR')
        # Printing record
        for val in result:
            print('PTR Record : ', val.to_text())
    except: 
        print(n)