import json
from pprint import pprint
from methods import HTTPMethod


class Device:
    """The device object"""
    def __init__(self, mgmt_ip:str, username:str, password:str):
        self.ip = mgmt_ip
        self.username = username
        self.password = password

        self.http_port = "80"
        self.ver = "1.0"  #NX-API ver
        self.response_format = "json"

        self.response = None  #the response message from the device

    def show(self, command):
        """Call this method to run the show commamd"""
        cli_request = {
            'ins-api': {
                'chunk': "0",
                'input': command,
                'output_format': self.response_format,
                'sid': "1",
                'type': "cli_show",
                'version': self.ver
            }
        }
        http = HTTPMethod(self.username, self.password, self.ip, self.http_port)
        self.response = http.request(cli_request, "no-cookie")
        return self

    def config(self, command):
        """Call this method to run the configuration commamd"""
        cli_request = {
            'ins-api': {
                'chunk': "0",
                'input': command,
                'output_format': self.response_format,
                'sid': "1",
                'type': "cli_conf",
                'version': self.ver
            }
        }
        http = HTTPMethod(self.username, self.password, self.ip, self.http_port)
        self.response = http.request(cli_request, "no-cookie")
        return self

    def res(self):
        """Returns a raw json response"""
        return self.response

    def dict_res(self):
        """Returns the response in the dictinary format"""
        res_in_dict = json.loads("".join(map(chr, self.response)))
        return res_in_dict

    def print_res(self):
        """Print the reponse"""
        if self.response is None:
            raise ValueError
        pprint(self.dict_res())

    def get_outputs(self):
        if self.response is None:
            raise ValueError
        outputs = self.dict_res()['ins_api']['outputs']
        return outputs

    @property
    def status(self):
        """HTTP status code"""
        outputs = self.get_outputs()['output']
        if type(outputs) is dict:
            return int(outputs['code'])
        elif type(outputs) is list:
            return int(outputs[0]['code'])


if __name__ == "__main__":
    nexus = Device("192.168.0.1", "admin", "P@ssw0rd")
    pprint(nexus.show("sh run").get_outputs())
    nexus.config("int eth 1/1 ;no sh").status
