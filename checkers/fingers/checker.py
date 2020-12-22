#!/usr/bin/env python3

from gevent import monkey, sleep

monkey.patch_all()

import sys
import os
import string
import random
import copy

from checklib import *

argv = copy.deepcopy( sys.argv )
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fingers_lib import *

# my utils
def idg(size=8, chars=alph):
	return ''.join(random.choice(chars) for _ in range(size))

class Checker(BaseChecker):
	uses_attack_data = True
	timeout = 15  # 15 seconds
	vulns = 2  # 2 places for flags

	def __init__(self, *args, **kwargs):	
		super(Checker, self).__init__(*args, **kwargs)
		self.mch = CheckMachine(self)

	def action(self, action, *args, **kwargs):
		try:
			super(Checker, self).action(action, *args, **kwargs)
		except pwnlib.exception.PwnlibException as err:
			self.cquit(Status.DOWN, 
				'Connection error', 
				'Pwntools connection error: Error: {}'.format(err) 
			)

	def check(self):
		self.mch.connection()

		fingerName = idg(random.randint(8, 16))
		fingerDesc = idg(random.randint(8, 16))
		fingerKey  = idg(random.randint(8, 16))
		assName = idg(random.randint(8, 16))

		try:
			self.mch.create_finger(fingerName, fingerDesc, fingerKey)
		except Exception as err:
			self.cquit(Status.MUMBLE, 
				"Can't create finger!", 
				'check(), finger creation! Error: {}'.format(err) 
			)
		
		try:
			self.mch.add_ass(assName)
		except Exception as err:
			self.cquit(Status.MUMBLE, 
				"Can't add a$$!", 
				'check(), add_ass failed! Error: {}'.format(err) 
			)

		privateToken = self.mch.put_finger(assName, True)
		data = self.mch.view_ass(assName, privateToken).decode()
		
		if fingerDesc not in data:
			self.cquit(Status.MUMBLE,
				"Can't get finger description from private a$$!",
				'check(), Data: {}'.format(data) 
			)

		assName = idg(random.randint(8, 16))

		try:
			self.mch.add_ass(assName)
		except Exception as err:
			self.cquit(Status.MUMBLE, 
				"Can't add a$$!", 
				'check(), add_ass failed! Error: {}'.format(err) 
			)

		self.mch.put_finger(assName, False)
		data = self.mch.get_finger(assName, fingerKey).decode()
		
		if fingerDesc not in data:
			self.cquit(Status.MUMBLE,
				"Can't get finger from non private a$$!",
				'check(), Data: {}'.format(data) 
			)

		# sell archived weapon, change status
		self.mch.safe_close_connection()
		self.cquit(Status.OK)

	def put(self, flag_id, flag, vuln):
		self.mch.connection()

		fingerName, fingerKey = idg(random.randint(8, 16)), idg(random.randint(8, 16))
		fingerDesc = flag
		assName = idg(20)

		try:
			self.mch.create_finger(fingerName, fingerDesc, fingerKey)
		except Exception as err:
			self.cquit(Status.MUMBLE, 
				"Can't create finger!", 
				'put(), create_finger failed! Error: {}'.format( err ) 
			)

		try:
			self.mch.add_ass(assName)
		except Exception as err:
			self.cquit(Status.MUMBLE, 
				"Can't add a$$!", 
				'put(), add_add failed! Error: {}'.format(err) 
			)

		if vuln == "1":
			privateToken = self.mch.put_finger(assName, True).decode()
			self.mch.safe_close_connection()
			self.cquit(Status.OK, f'{assName}', f'{assName}:{privateToken}') 
		else:
			self.mch.put_finger(assName, False)
			self.mch.safe_close_connection()
			self.cquit(Status.OK, f'{assName}', f'{assName}:{fingerKey}') 

	def get(self, flag_id, flag, vuln):
		assName, privateToken = flag_id.split(":")

		self.mch.connection()
		data = None

		if vuln == "1":
			data = self.mch.view_ass(assName, privateToken).decode()
		else:
			data = self.mch.get_finger(assName, privateToken).decode()

		self.mch.safe_close_connection()

		if flag not in data:
			self.cquit(Status.CORRUPT, 
				"Can't get flag!", 
				'get(), no flag in out data! Out: {}'.format(data) 
			)

		self.cquit(Status.OK)

if __name__ == '__main__':
	c = Checker(argv[2])

	try:
		c.action(argv[1], *argv[3:])
	except c.get_check_finished_exception():
		cquit(Status(c.status), c.public, c.private)