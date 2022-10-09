from settings import *

import socket
from socket import socket as sc
import json


class Connection(object):

    def __init__(self, address, connected=False):
        self.address = address
        self.connected = connected


class Client(object):
    VALID = 0
    INVALID = 1
    EMPTY = 2

    INCORRECT_MESSAGE_FORMAT = 100

    def __init__(self) -> None:

        self.UDPClientSocket = sc(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )

        self.connections: dict[Connection] = {}

    def listen(self) -> int | tuple[any, any, any]:

        bytes_address_pair = self.UDPClientSocket.recvfrom(BUFFERSIZE)

        if not bytes_address_pair:
            return Client.EMPTY

        message = bytes_address_pair[0]
        address = bytes_address_pair[1]

        try:
            message = json.loads(message)
        except TypeError:
            return Client.INVALID, address, Client.INCORRECT_MESSAGE_FORMAT

        return Client.VALID, address, message

    def send(self, data: any) -> None:

        self.UDPClientSocket.sendto(json.dumps(data).encode(), SERVER_ADDRESS)

