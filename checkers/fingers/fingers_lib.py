from pwn import *
from checklib import *

import random
import string
from gevent import sleep

context.log_level = 'CRITICAL'

PORT = 9999

# global const
TCP_CONNECTION_TIMEOUT = 10
TCP_OPERATIONS_TIMEOUT = 10
alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

class CheckMachine:
	sock = None
	_username = None

	def __init__( self, checker ):
		self.c = checker
		self.port = PORT

	def connection( self ):
		try:
			self.sock = remote( self.c.host, 
				self.port, 
				timeout = TCP_CONNECTION_TIMEOUT 
			)
			self.sock.settimeout( TCP_CONNECTION_TIMEOUT )
		except:
			self.sock = None
			self.c.cquit( Status.DOWN, 
				'Connection error',
				'CheckMachine.connection(): timeout connection!' 
			)

		self.sock.settimeout( TCP_OPERATIONS_TIMEOUT )

	def create_finger(self, fingerName, fingerDesc, fingerKey):
		self.sock.recvuntil(b"> ")
		self.sock.sendline(b"1")
		
		self.sock.recvuntil(b": ")
		self.sock.sendline(fingerName)

		self.sock.recvuntil(b": ")
		self.sock.sendline(fingerDesc)

		self.sock.recvuntil(b": ")
		self.sock.sendline(fingerKey)

	def put_finger(self, assName, isPrivate):
		self.sock.recvuntil(b"> ")
		self.sock.sendline(b"2")
		
		self.sock.recvuntil(b": ")
		self.sock.sendline(assName)

		self.sock.recvuntil(b": ")

		if isPrivate:
			self.sock.sendline(b"yes")
			self.sock.recvuntil(b"to a$$: ")
			privateToken = self.sock.recvline().strip()
			return privateToken
		else:
			self.sock.sendline(b"no")
	
	def get_finger(self, assName, fingerKey):
		self.sock.recvuntil(b"> ")
		self.sock.sendline(b"3")
		
		self.sock.recvuntil(b": ")
		self.sock.sendline(assName)

		self.sock.recvuntil(b": ")
		self.sock.sendline(fingerKey)

		result = self.sock.recvline()
		return result

	def add_ass(self, assName):
		self.sock.recvuntil(b"> ")
		self.sock.sendline(b"4")
		
		self.sock.recvuntil(b": ")
		self.sock.sendline(assName)
	
	def view_ass(self, assName, privateToken):
		self.sock.recvuntil(b"> ")
		self.sock.sendline(b"5")
		
		self.sock.recvuntil(b": ")
		self.sock.sendline(assName)

		self.sock.recvuntil(b": ")
		self.sock.sendline(privateToken)

		result = self.sock.recvline()
		return result

	def safe_close_connection(self):
		self.sock.recvuntil(b"> ")
		self.sock.send("6\n")

		self.sock.close()
		self.sock = None
	
	def close_connect(self):
		try:
			self.sock.close()
			self.sock = None
		except:
			self.sock = None

