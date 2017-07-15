# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
try:
	from PyQt5 import QtGui,QtCore
except:
	from PyQt4 import QtGui,QtCore

import time,sys,inspect,copy,functools

import expeyes.eyes17 as eyes

class communicationHandler(QtCore.QObject):
	sigStat = QtCore.pyqtSignal(str,bool)
	sigPlot = QtCore.pyqtSignal(object)
	sigConnected = QtCore.pyqtSignal()
	sigDisconnected = QtCore.pyqtSignal()
	sigConnectionDialog = QtCore.pyqtSignal()
	
	sigGeneric = QtCore.pyqtSignal(str,object)
	sigError = QtCore.pyqtSignal(str,str)

	sigExec = QtCore.pyqtSignal(str,object,object)
	execThread = QtCore.pyqtSignal(str,object,object,object)
	connected = False
	menu_entries=[]

	def __init__(self, parent=None,**kwargs):
		super(self.__class__, self).__init__(parent)
		self.connectHandler = kwargs.get('connectHandler',None)
		self.disconnectHandler = kwargs.get('disconnectHandler',None)
		self.connectionDialogHandler = kwargs.get('connectionDialogHandler',None)

		self.sigConnected.connect(self.connectHandler)
		self.sigDisconnected.connect(self.disconnectHandler)
		self.sigConnectionDialog.connect(self.connectionDialogHandler)

		self.sigExec.connect(self.process)
		self.execThread.connect(self.processAndForward)

		#Auto-Detector
		self.shortlist=[]
		self.timer4 = QtCore.QTimer()
		self.timer4.timeout.connect(self.locateDevices)
		self.timer4.start(300)

		#self.tmr = QtCore.QTimer()
		#self.tmr.setSingleShot(True)
		#self.tmr.timeout.connect(self.connectToDevice)
		#self.tmr.start(10)

	def connectToDevice(self):
		self.I = eyes.Interface()
		self.busy=False
		if self.I.connected:
			self.connected = True
			self.I.set_sine(1000)
		else:
			return
		self.evalGlobals = {k: getattr(self.I, k) for k in dir(self.I)}
		
		#Add methods dynamically from I into this threaded module.
		self.functionList = {}
		
		class functionContainer:
			def __init__(self,fname,sig1,sig2):
				self.sigExec = sig1
				self.execThread = sig2
				self.fname = fname
			def func(self,*args,**kwargs):
				self.sigExec.emit(self.fname,args,kwargs)
			def funcForward(self,fwdfunc,*args,**kwargs):
				self.execThread.emit(self.fname,args,kwargs,fwdfunc)
				
		
		for a in dir(self.I):
			attr = getattr(self.I,a)
			if inspect.ismethod(attr) and a!='__init__':
				F = functionContainer(a,self.sigExec,self.execThread)
				self.functionList[a] = F.func
				setattr(self,a,F.func)
				self.functionList[a+'_fwd'] = F.funcForward
				setattr(self,a+'_fwd',F.funcForward)

		
		self.timer = QtCore.QTimer()
		self.buflen = 0
		self.trigPre = 0 # prescaler for trigger waiting for the oscilloscope
		self.channels_enabled=[0,0,0,0]

		self.sigConnected.emit()
		

	def locateDevices(self):
		if not hasattr(self,'I'):
			self.connectToDevice() # May or may not be successful, but it goes through the library and does some init tasks
			return

		try:L = self.I.H.listPorts()
		except Exception as e:print (e)
		total = len(L)
		menuChanged = False
		if L != self.shortlist:
			menuChanged = True
			self.shortlist=L
			
			for a in self.menu_entries:
				pass
				#self.deviceCombo.removeItem(0)
			self.menu_entries=[]
			for a in L:
				#self.deviceCombo.addItem(a)
				self.menu_entries.append(a)

		#Check for, and handle disconnect event
		if menuChanged:
			if self.I.connected:
				if self.I.H.portname not in self.menu_entries:
						print('Device Disconnected',True)
						print('Error : Device Disconnected')
						#QtGui.QMessageBox.warning(self, 'Connection Error', 'Device Disconnected. Please check the connections')
						try:self.I.H.disconnect()
						except:pass
						self.I.H.connected = False
						self.I.connected = False

			elif len(self.menu_entries):
				print ('found new device. prompting user...')
				self.sigConnectionDialog.emit()



		

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
				forwardingFunction = kwargs.pop('forwardingFunction',None)
				nextUp = kwargs.pop('nextUp',None)
				
				self.I.capture_traces(*args,**kwargs)
				self.buflen = args[0]
				self.channels_enabled=kwargs.get('chans',[0,0,0,0])
				self.busy=True ##########  SET A BUSY FLAG
				if nextUp is not None:
					self.timer.singleShot(args[1]*args[2]*1e-3+10+self.trigPre*20,nextUp)
				elif forwardingFunction is not None:
					def newFunc(FF):
						self.sigExec.emit('fetchData',[],{'forwardingFunction':FF})
					partialFunc = functools.partial(newFunc,forwardingFunction)
					#print ('got here',forwardingFunction,newFunc)
					self.timer.singleShot(args[1]*args[2]*1e-3+10+self.trigPre*20,partialFunc)
				else:
					self.timer.singleShot(args[1]*args[2]*1e-3+10+self.trigPre*20,self.fetchData)
			elif name == 'fetchData':	                #non - blocking call. Start acquisition , and fetch data when it's ready.
				n=0
				#print ('here',args,kwargs)
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
							returnData[self.I.achans[a].channel]=[X,self.I.achans[a].get_yaxis()] #returnData is a dict of the form {'A1':[xarray,yarray],'A2':...}

					self.busy=False ##########  CLEAR THE BUSY FLAG
					if 'forwardingFunction' in kwargs:
						kwargs.get('forwardingFunction')(returnData)
					else:
						self.sigPlot.emit(returnData)

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
			print ('ERROR',e)
			self.sigError.emit(name,str(e))


	@QtCore.pyqtSlot(str,object,object,object)
	def processAndForward(self,name,args,kwargs,returnFunction):
		name = str(name)
		if name in self.evalGlobals:
			returnFunction(self.evalGlobals[name](*args,**kwargs))
		else:
			returnFunction(name,None)




	def fetchData(self):
			self.process('fetchData',[],{})

	'''
	def set_pv1(self,val):
		self.sigExec.emit('set_pv1',[val],{})
	'''

