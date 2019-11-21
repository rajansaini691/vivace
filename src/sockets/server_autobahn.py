from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

"""
Implements a server using autobahn
"""


class SocketProtocol(WebSocketServerProtocol):
    """
    Sends info to client
    """
    def onConnect(self, request):
        # TODO Send client the HTML
        print("some request connected {}".format(request))

    def onOpen(self, request):
        # TODO Spawn new thread pushing data from main thread to the client
        print("Connection Opened")

    def onMessage(self, payload, isBinary):
        self.sendMessage("message received")
