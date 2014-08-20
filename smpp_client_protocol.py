# -*- coding: utf-8 -*-
from StringIO import StringIO
import chardet

from twisted.internet.protocol import Protocol
from smpp.pdu import operations, pdu_types
from smpp.pdu.pdu_encoding import PDUEncoder

import settings


class SMPPClientProtocol(Protocol):

    def dataReceived(self, data):
        pdu = self._bin2pdu(data)
        print "Date received", pdu, '\n'

        command_id = str(pdu.commandId)

        if command_id == 'bind_transmitter_resp':
            if pdu.status is pdu_types.CommandStatus.ESME_ROK:
                self._submit_sm()

    def connectionMade(self):
        print 'Connection made to', self.transport.getPeer().host, '\n'
        self._auth()

    def connectionLost(self, reason):
        print 'Connection lost', reason

    def _bin2pdu(self, bindata):
        io_pdu = StringIO(bindata)
        return PDUEncoder().decode(io_pdu)

    def _pdu2bin(self, pdu):
        return PDUEncoder().encode(pdu)

    ###############################################
    ## next group of methods is only examples    ##
    ## you can add any method (smpp command_id), ##
    ## for example enquire_link etc              ##
    ###############################################
    def _auth(self):
        # send bind_transmitter pdu
        bind_pdu = operations.BindTransmitter(seqNum=1,
                                              system_id=settings.SYSTEM_ID,
                                              password=settings.PASSWORD,
                                              system_type='sys_type')

        print 'Send bind transmitter request\n'
        self.transport.write(self._pdu2bin(bind_pdu))

    def _submit_sm(self):
        # send submit_sm pdu
        message_text = 'This is message for sms'
        encoding = chardet.detect(message_text)['encoding']
        data_coding = pdu_types.DataCoding(pdu_types.DataCodingScheme.DEFAULT,
                                           pdu_types.DataCodingDefault.UCS2)
        message_text = message_text.decode(encoding).encode('UTF-16')

        sm_pdu = operations.SubmitSM(
            seqNum=1,
            short_message=message_text,
            destination_addr='380632588588',    # do not send messages to me :)
            source_addr_ton=pdu_types.AddrTon.ALPHANUMERIC,
            source_addr_npi=pdu_types.AddrNpi.UNKNOWN,
            source_addr='380632588588',
            dest_addr_ton=pdu_types.AddrTon.INTERNATIONAL,
            dest_addr_npi=pdu_types.AddrNpi.ISDN,
            data_coding=data_coding,
            registered_delivery=pdu_types.RegisteredDelivery(
                pdu_types.RegisteredDeliveryReceipt.SMSC_DELIVERY_RECEIPT_REQUESTED)
        )

        print 'Send submit sm request\n'
        self.transport.write(self._pdu2bin(sm_pdu))