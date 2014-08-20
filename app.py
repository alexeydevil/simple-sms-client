# -*- coding: utf-8 -*-
from twisted.internet import reactor

from smpp_client_factory import SMPPClientFactory
import settings


def app():
    # create client protocol instance
    factory = SMPPClientFactory()
    reactor.connectTCP(settings.HOST, settings.PORT, factory)


reactor.callLater(0, app)
reactor.run()