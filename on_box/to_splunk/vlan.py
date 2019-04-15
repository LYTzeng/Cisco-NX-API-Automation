from udp_socket import SendTo
from cisco.vlan import *
from cli import *

# splunk server information
splunk_ip = '172.30.3.32'
port = 514
vrf = 'management'

def _split_list(self, vlan_list):
    list_len = len(vlan_list)
    new_list = list()
    for i in range(0, list_len/2):
        new_list.append(vlan_list[i])
    return new_list

curr_vlans = _split_list(ShowVlan().get_vlans())
vlan_count = len(curr_vlans)

hostname = cli('show hostname')
hostname = hostname.replace(' \n', '')

data = {
    "vlan_count": vlan_count,
    "hostname": hostname
    }

SendTo.send_json(splunk_ip, port, vrf, data)
