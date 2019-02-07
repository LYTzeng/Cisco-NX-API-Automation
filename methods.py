"""Basic HTTP and HTTPS methods"""
import urllib3
import json
from base64 import encodestring


class HTTPMethod:
    """HTTP method
    
    Attributes:
        username: The username to login to the Nexus device.
        password: The password to login to the Nexus device.
        ip: The IP address of the management port.
        port: Specify a L4 port number to communicate through HTTP. Default is 80.
    """
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
        """Call this function to send a http post request.
        
        Args:
            req_data: NX-API json request in dictionary format.
            cookie: Whether to use cookie or not.
            timeout: If response exceeds the timeout, urllib fails.

        Returns:
            The response from NX-OS. 
        """
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
            return
        
        return response.data
