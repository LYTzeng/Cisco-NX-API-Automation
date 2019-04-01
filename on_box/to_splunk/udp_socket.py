import json
import socket
from cisco.vrf import *


class SendTo:

    @staticmethod
    def send_json(ip, udp_port, vrf, dict):
        set_global_vrf(vrf)
        addr = (ip, udp_port)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        data = json.dumps(dict)
        s.sendto(data, addr)
        s.close()
