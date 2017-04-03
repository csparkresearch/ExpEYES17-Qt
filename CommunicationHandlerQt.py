# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from PyQt4 import QtGui,QtCore
import time,sys,inspect,copy

import expeyes.eyes17 as eyes

class communicationHandler(QtCore.QObject):
	sigStat = QtCore.pyqtSignal(str,bool)
	sigPlot = QtCore.pyqtSignal(object)
	sigGeneric = QtCore.pyqtSignal(str,object)
	sigError = QtCore.pyqtSignal(str,str)

	sigExec = QtCore.pyqtSignal(str,object,object)
	execThread = QtCore.pyqtSignal(str,object,object,object)
	connected = False
	def __init__(self, parent=None,**kwargs):
		super(self.__class__, self).__init__(parent)
		self.I = eyes.open()
		self.busy=False
		if self.I.connected:self.connected = True
		self.I.set_sine(1000)
		self.sigExec.connect(self.process)
		self.execThread.connect(self.processAndForward)
		self.evalGlobals = {k: getattr(self.I, k) for k in dir(self.I)}
		
		#Add methods dynamically from I into this threaded module.
		self.functionList = {}
		
		class functionContainer:
			def __init__(self,fname,sig):
				self.sigExec = sig
				self.fname = fname
			def func(self,*args,**kwargs):
				self.sigExec.emit(self.fname,args,kwargs)
			def funcForward(self,fwdfunc,*args,**kwargs):
				self.execThread.emit(self.fname,args,kwargs,fwdfunc)
				
		
		for a in dir(self.I):
			attr = getattr(self.I,a)
			if inspect.ismethod(attr) and a!='__init__':
				F = functionContainer(a,self.sigExec)
				self.functionList[a] = F.func
				setattr(self,a,F.func)
				self.functionList[a+'_fwd'] = F.funcForward
				setattr(self,a+'_fwd',F.funcForward)

		
		self.timer = QtCore.QTimer()
		self.buflen = 0
		self.trigPre = 0 # prescaler for trigger waiting for the oscilloscope
		self.channels_enabled=[0,0,0,0]
		
		

	@QtCore.pyqtSlot(str,object,object)
	def process(self,name,args,kwargs):
		name = str(name)
		#print (name,args,kwargs)
		try:
			if name == 'capture1':                          #blocking call . Acquire data , and immediately signal to plot
				x,y = self.I.capture1(*args,**kwargs)
				self.sigStat.emit('acquired data',False)
				self.sigPlot.emit({args[0]:[x,y]})
			elif name == 'capture2':
				x,y,x2,y2 = self.I.capture2(*args,**kwargs)
				self.sigPlot.emit({self.I.achans[0].channel:[x,y],args['A2']:[x2,y2]})
			elif name == 'capture_action':
				x,y = self.I.capture_action(*args,**kwargs)
				self.sigPlot.emit({self.I.achans[0].channel:[x,y]})
			elif name == 'capture_traces':	                #non - blocking call. Start acquisition , and fetch data when it's ready.
				self.I.capture_traces(*args,**kwargs)
				self.buflen = args[0]
				self.channels_enabled=kwargs.get('chans',[0,0,0,0])
				self.busy=True
				self.timer.singleShot(args[1]*args[2]*1e-3+10+self.trigPre*20,self.fetchData)
			elif name == 'fetchData':	                #non - blocking call. Start acquisition , and fetch data when it's ready.
				n=0
				try:
					while(not self.I.oscilloscope_progress()[0]):
						time.sleep(0.1)
						print ('correction required',n)
						n+=1
						if n>15:
							raise Exception

					t=time.time()
					returnData = {}
					X=None
					for a in range(self.buflen):
						if self.channels_enabled[a]:
							self.I.__fetch_channel__(a+1)
							if X is None:X = self.I.achans[a].get_xaxis()*1e-6
							returnData[self.I.achans[a].channel]=[X,self.I.achans[a].get_yaxis()]
					#print ('traces...ordered',time.time()-t)
					self.busy=False
					self.sigPlot.emit(returnData)
					#if self.buflen==1:self.sigPlot.emit([X,self.I.achans[0].get_yaxis()])
					#elif self.buflen==2:self.sigPlot.emit([X,self.I.achans[0].get_yaxis(),X,self.I.achans[1].get_yaxis()])
					#elif self.buflen==3:self.sigPlot.emit([X,self.I.achans[0].get_yaxis(),X,self.I.achans[1].get_yaxis(),X,self.I.achans[2].get_yaxis()])
					#elif self.buflen==4:self.sigPlot.emit([X,self.I.achans[0].get_yaxis(),X,self.I.achans[1].get_yaxis(),X,self.I.achans[2].get_yaxis(),X,self.I.achans[3].get_yaxis()])

				except Exception as e:
					self.sigError.emit(name,e.message)
			elif name == 'HX711':
				res = self.I.HX711.read(*args)
				self.sigGeneric.emit(name,res)


			else:
				if name in self.evalGlobals:
					res = self.evalGlobals[name](*args,**kwargs)
					self.sigGeneric.emit(name,res)
				else:
					self.sigError.emit(name,' : unknown function')
		except Exception as e:
			self.sigError.emit(name,e.message)


	@QtCore.pyqtSlot(str,object,object,object)
	def processAndForward(self,name,args,kwargs,returnFunction):
		name = str(name)
		if name in self.evalGlobals:
			returnFunction(self.evalGlobals[name](*args,**kwargs))
		else:
			returnFunction(None)




	def fetchData(self):
			self.process('fetchData',[],{})

	'''
	def set_pv1(self,val):
		self.sigExec.emit('set_pv1',[val],{})
	'''

