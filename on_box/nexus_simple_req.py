'''
Please execute this code on a Cisco Nexus series switch
'''
from cisco.vrf import *
import urllib
import urllib2
from base64 import encodestring

url = 'http://172.30.3.144:8002'
set_global_vrf('default')
req = urllib2.Request(url)

# For GET method, call this directily
# res = urllib2.urlopen()

# POST method
data = {'hello': 'world'}
edata = urllib.urlencode(data)
b64data = encodestring((edata.encode()).decode().replace('\n', ''))
req = urllib2.Request(url, data=b64data)
res = urllib2.urlopen(req)
