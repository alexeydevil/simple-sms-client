# -*- coding: utf-8 -*-
from twisted.internet.protocol import ClientFactory

from smpp_client_protocol import SMPPClientProtocol


class SMPPClientFactory(ClientFactory):
    protocol = SMPPClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print 'Failed to connect to:', connector.getDestination()