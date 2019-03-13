'''
Please execute this code on a Cisco Nexus series switch

Usage: 
    python nexus_vlan_notification.py ip port vrf [-t timer] [-d debug]
Args: 
    ip: ip address
    port: http port number
    vrf: VRF which the interface belongs to
    -t, --time: in secs, which determines the refresh time
    -d, --debug: Default is False, set to True if debug output is needed
'''
from cisco.vrf import *
from cisco.vlan import *
import urllib
import urllib2
from base64 import encodestring
import argparse
import time

parser = argparse.ArgumentParser(description='vlan_notification')
parser.add_argument('ip', metavar='IP', type=str)
parser.add_argument('port', metavar='PORT', type=int)
parser.add_argument('vrf', metavar='VRF', type=str)
parser.add_argument('-t', '--time', dest='timer', type=int, default=5)
parser.add_argument('-d', '--debug', dest='debug', type=bool, default=False)
args = parser.parse_args()
IP = args.ip
PORT = args.port
VRF = args.vrf
TIMER = args.timer
DEBUG = args.debug

url = 'http://%s:%s' % (IP, PORT)
set_global_vrf(VRF)

class VlanWatcher:
    def __init__(self):
        self.init_vlan = ShowVlan().get_vlans()
        self.old_vlans = self._split_list(self.init_vlan)

    def observe(self):
        curr_vlans = self._split_list(ShowVlan().get_vlans())
        newly_created = list(set(curr_vlans) - set(self.old_vlans))
        deleted = list(set(self.old_vlans) - set(curr_vlans))
        message_queue = dict()
        if DEBUG:
            print 'old_vlans ', self.old_vlans
            print 'curr_vlans ', curr_vlans
            print 'newly_created ', newly_created
            print 'deleted ', deleted
        if newly_created != []:
            notification = list()
            for vlan in newly_created:
                notification.append('Vlan ' + vlan[0] + ' was created.')
            message_queue['New_Vlan_Notification'] = notification
            self._send_request(message_queue)
        if deleted != []:
            notification = list()
            for vlan in deleted:
                notification.append('Vlan ' + vlan[0] + ' was deleted.')
            message_queue['Deleted_Vlan_Notification'] = notification
            self._send_request(message_queue)
        
        self.old_vlans = curr_vlans
        

    def observe_forever(self):
        while True:
            self.observe()
            time.sleep(TIMER)

    def _send_request(self, message_queue):
        emessage = urllib.urlencode(message_queue)
        b64message = encodestring((emessage.encode()).decode().replace('\n', ''))
        req = urllib2.Request(url, data=b64message)
        res = urllib2.urlopen(req)

    def _split_list(self, vlan_list):
        list_len = len(vlan_list)
        new_list = list()
        for i in range(0, list_len/2):
            new_list.append(vlan_list[i])
        return new_list

if __name__ == '__main__':
    vlan = VlanWatcher()
    vlan.observe_forever()
