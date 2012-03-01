import re

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from urllib import urlopen

def parse_mails(stream):
	result = []
	for line in stream:
		result.extend(re.findall('\w*@\w*\.\w*', line))
		
	return result

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
		
		self.join(self.channel)
		
	def privmsg(self, user, channel, msg):
		'''
		this will get called when the bot receives a message. it doesn't matter 
		if this is a message in a channel or a private message
		'''
		
		# ignore all messages except !harvest calls
		if msg.startswith('!harvest'):
			# get url from message
			url = msg.split()[1]
			
			# find all mail addresses and print them one per line
			for mail in re.findall('\w*@\w*\.\w*', urlopen(url).read()):
				self.msg(channel, '[@] %s' % mail)
			
			# tell we are finished
			self.msg(channel, '[fin]')
			
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

	reactor.connectTCP('irc.freenode.net', 6667, factory)
	reactor.run()