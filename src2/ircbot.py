from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

class Bot(irc.IRCClient):
	'''
	harvesting irc bot
	'''
	
	nickname = 'harvest-moon'
	channel = '#hackinggroup'
	
	def signedOn(self):
		'''
		called when bot has succesfully signed on to server.
		'''
		
		self.join(channel)
		
	def privmsg(self, user, channel, msg):
		'''
		this will get called when the bot receives a message. it doesn't matter 
		if this is a message in a channel or a private message
		'''
		
		if msg.startswith('!start '):
			# do action
			self.msg(channel, '[starting to harvest]')
			
class Factory(protocol.ClientFactory):
	'''
	factory for harvester bots. a new protocol instance will be created each
	time we connect to the server (in our example once).
	'''
	
	# the class of the protocol to build when new connection is made
	protocol = Bot
	
	def clientConnectionLost(self, connector, reason):
		'''
		called when tcp connection is lost => trying to reconnect
		'''
		
		print "connection lost: %s" % reason
		connector.connect()
		
	def clientConnectionFailed(self, connector, reason):
		'''
		called when tcp connection attemp failed!
		'''
		
		print "connection failed: %s" % reason
		reactor.stop()
		
if __name__ == '__main__':
	factory = protocol.ClientFactory()
	factory.protocol = Bot

	#reactor.connectSSL('irc.freenode.net', 6667, factory)
	reactor.connectTCP('irc.freenode.net', 6667, factory)
	reactor.run()