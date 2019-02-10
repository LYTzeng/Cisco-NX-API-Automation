import json
from pprint import pprint
from methods import HTTPMethod
import exceptions
import time, datetime


class Device:
    """The device object"""
    def __init__(self, mgmt_ip:str, username:str, password:str):
        self.ip = mgmt_ip
        self.username = username
        self.password = password

        self.http_port = "80"
        self.ver = "1.0"  # NX-API ver
        self.response_format = "json"

        self.response = None  # the response message from the device
        self.timeformat = "%Y-%m-%d-%H-%M-%S"  # for backup
        self.backup_files = list()  # List of backup files

    # Basic JSON CLI method

    def show(self, command:str):
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

    def config(self, command:str):
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

    # Methods to copy & backup config via TFTP

    def backup_config(self, tftp_server:str, tftp_directory="", vrf_name="default", source="running-config"):
        """Run the "copy `running-config` tftp:`tftp_server`" command"""
        if tftp_directory != "" and tftp_directory[:1] != "/":
            raise exceptions.FuncInputError('tftp_directory should starts with "/".')
        filename = self.hostname + "-" + self._timestamp
        backup_command = "copy %s tftp://%s%s/%s vrf %s" % (source, tftp_server, tftp_directory, filename, vrf_name)
        self.config(backup_command)
        self._check_status()
        self.backup_files.append(filename)
        return self

    def rollback_config(self, tftp_server:str, filename:str, tftp_directory="", vrf_name="default", destination="running-config"):
        if tftp_directory != "" and tftp_directory[:1] != "/":
            raise exceptions.FuncInputError('tftp_directory should starts with "/".')
        backup_command = "copy tftp://%s%s/%s %s vrf %s" % (tftp_server, tftp_directory, filename, destination, vrf_name)
        self.config(backup_command)
        self._check_status()
        return self

    # Methods to get JSON response from NXOS

    def res(self):
        """Returns a raw json response"""
        self._check_req()
        return self.response

    def dict_res(self):
        """Returns the response in the dictinary format"""
        self._check_req()
        res_in_dict = json.loads("".join(map(chr, self.response)))
        return res_in_dict

    def print_res(self):
        """Print the reponse"""
        self._check_req()
        pprint(self.dict_res())

    def get_outputs(self):
        self._check_req()
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

    @property
    def hostname(self):
        output = self.show("sh hostname").get_outputs()
        hostname = output['output']['body']['hostname']
        return hostname

    # Private methods below

    def _check_req(self):
        if self.response is None:
            raise exceptions.NoPrevRequestError('Call method "show" or "config" first.')

    def _check_status(self):
        if self.status != 200:
            message = "HTTP " + str(self.status)
            raise exceptions.HttpError(message)

    @staticmethod
    def _now(format):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime(format)
        return timestamp

    @property
    def _timestamp(self):
        return self._now(self.timeformat)


if __name__ == "__main__":
    nexus = Device("192.168.0.1", "admin", "P@ssw0rd")
    # pprint(nexus.show("sh run").get_outputs())
    # nexus.config("int eth 1/1 ;no sh").status
    nexus.backup_config("192.168.0.10", "/qWy5IYH72-incoming", "management")
    print(nexus.backup_files)
    nexus.rollback_config("192.168.0.10", "switch-2019-02-09-01-28-02", "/qWy5IYH72-incoming", "management")
    