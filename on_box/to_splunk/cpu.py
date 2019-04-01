from .udp_socket import SendTo
from cli import *
import re

# splunk server information
splunk_ip = '172.30.3.32'
port = 514
vrf = 'management'

raw = cli('show processes cpu | inc CPU')
cpu_idle = float(re.search(r'[0-9]{1,3}.[0-9]{0,2}(?=% idle.*[\n])', raw).group(0))
cpu_busy = 100 - cpu_idle
data = {"cpu_usage": "%.2f" % cpu_busy}
SendTo.send_json(splunk_ip, port, vrf, data)
