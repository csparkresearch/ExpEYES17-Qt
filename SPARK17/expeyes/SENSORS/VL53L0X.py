# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
'''
'''

from __future__ import print_function
import time

def connect(route,**args):
	return VL53L0X(route,**args)

class VL53L0X: 
	ADDRESS = 0x29 
	name = 'VL53L0X:Light Echo'
	NUMPLOTS=1
	PLOTNAMES = ['Distance']
	def __init__(self, I2C,**args):
		self.ADDRESS = args.get('address',self.ADDRESS)
		self.I2C = I2C  
		self.initialize(None)

	def initialize(self,v):
		print('0xC0==0xEE test : ',self.I2C.readBulk(self.ADDRESS,0xC0,1)[0] == 0xEE)
		print('0xC1==0xAA test : ',self.I2C.readBulk(self.ADDRESS,0xC1,1)[0] == 0xAA)
		#self.I2C.writeBulk(self.ADDRESS,[0x80 | 0x01, 0x01 | 0x10 ])
	
	def getRaw(self):
		#vals = self.I2C.readBulk(self.ADDRESS,0x80 | 0x20 | 0x0C ,4)  # Byte 1, 2 (full range ) . Byte (3,4) Infrared .
		#if vals:
		#	full = (vals[1]<<8)|vals[0]
		#	infra = (vals[3]<<8)|vals[2]
		#	return [full,infra,full-infra]
		#else:
		#	return False
		return [42]

