import urllib3
from base64 import encodestring
import json
from pprint import pprint

class HTTPMethod:
    def __init__(
        self, 
        username: str,
        password: str,
        ip: str,
        port: int
        ):

        self.http = urllib3.PoolManager()
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.base64_auth = encodestring( ('%s:%s' % (self.username, self.password)).encode()).decode().replace('\n', '')

    def request(self, req_data, cookie, timeout=10):
        response = None
        json_req = json.dumps(req_data).encode('utf-8')
        try:
            response = self.http.request(
                'POST',
                'http://%s:%s/ins' % (self.ip, self.port),
                body=json_req,
                headers={
                    'content-type': 'application/json',
                    'Authorization': 'Basic %s' % self.base64_auth,
                }
            )
        except urllib3.exceptions.MaxRetryError as MaxRetryError:
            print(MaxRetryError)
            raise
        
        if (response.status != 200 and response.status != 304):
            print('HTTP %s' % response.status)
            print(response.data)
            return
        
        print(response.data)
        return response.data


class NXAPI:
    def __init__(self):
        self.username = 'admin'
        self.password = 'P@ssw0rd'
        self.ip = '192.168.10.1'
        self.port = '80'
        self.timeout = 10

        self.ver = '1.0'
        self.type = 'cli_show'
        self.cmd = 'show version'
        self.output_format = 'json'
        self.chunk = '0'
        self.sid = '1'
        self.cookie = 'no-cookie'
        
        self.response = None

    def _req_data(self, command):
        self.cmd = command
        cli_request = {
            'ins-api': {
                'chunk': self.chunk,
                'input': command,
                'output_format': self.output_format,
                'sid': self.sid,
                'type': self.type,
                'version': self.ver
            }
        }
        return cli_request

    def send_req(self, command="sh ver"):
        self.response = None
        http = HTTPMethod(self.username, self.password, self.ip, self.port)
        self.response = http.request(self._req_data(command=command), self.cookie)

    def set_type(self, __type):
        self.type = __type

    def dict_res(self):

        res_in_dict = json.loads("".join(map(chr, self.response)))
        return res_in_dict


if __name__ == "__main__":
    nexus = NXAPI()
    nexus.send_req()
    res = nexus.dict_res()
    pprint(res)
