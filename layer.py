# -*- coding: utf-8 -*-
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

def enviarWhats(missatge, numero, self):
	try:
		missatge = missatge.encode('utf8')
	except:
		pass
	self.toLower(TextMessageProtocolEntity(missatge, to = numero))