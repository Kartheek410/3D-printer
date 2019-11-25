# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:02:45 2019

@author: Kartheek
"""
import serial

class projector:

	def __init__(self, settings):

		# Internalise settings.
		self['projectorPort'] =	settings(value='/dev/ttyUSB0', valType=str, default='/dev/ttyUSB0',	name='Port', output=self.output)
		self['projectorBaudrate'] = settings(value=9600, valType=int, default=9600, name='Baud rate', output=self.output)
		self['projectorControl'] =	settings(value=False, valType=str, default=False, name='Projector control', output=self.output)
		self['projectorOnCommand'] = settings(value='* 0 IR 001', valType=str, default='* 0 IR 001', name='Projector ON command', output=self.output)
		self['projectorOffCommand'] = settings(value='* 0 IR 002', valType=str, default='* 0 IR 002', name='Projector OFF command', output=self.output)

		# Configure and open serial.
		if not self.debug:
			try:
				self.serial = serial.Serial(
					port=self.settings['projectorPort'].value,
					baudrate=self.settings['projectorBaudrate'].value,
					bytesize = serial.EIGHTBITS, #number of bits per bytes
					parity = serial.PARITY_NONE, #set parity check: no parity
					stopbits = serial.STOPBITS_ONE
					)
			# If serial port does not exist...
			except serial.SerialException:
				# ... define a dummy.
				self.serial = None
		else:
			print("Projector serial in debug mode: not sending.")
			self.serial = None


	def activate(self):
		command = self.settings['projectorOnCommand'].value
		if self.serial != None:
			self.serial.write(command+'\r')

	def deactivate(self):
		command = self.settings['projectorOffCommand'].value
		if self.serial != None:
			self.serial.write(command+'\r')

	def close(self):
		if self.serial != None:
			self.serial.close()
#		print "projector serial closed"