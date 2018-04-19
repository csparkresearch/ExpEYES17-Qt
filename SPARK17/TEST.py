#!/usr/bin/python
# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-

"""

::

	This program loads calibration data from a directory, processes it, and loads it into a connected device
	Not for regular users!
	Maybe dont include this in the main package

"""
from __future__ import print_function
import templates.ui_testing as testing

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import sys,functools,os,random,struct,time,string

class AppWindow(QtGui.QMainWindow, testing.Ui_MainWindow):
	RESISTANCE_ERROR = 80
	CCS_ERROR = 150 #150 ohms
	CAPACITANCE_ERROR = 30e-12 #30pF
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)

		try:
			import scipy.optimize as optimize
		except ImportError:
			self.optimize = None
		else:
			self.optimize = optimize

		try:
			import scipy.fftpack as fftpack
		except ImportError:
			self.fftpack = None
		else:
			self.fftpack = fftpack


		self.I=kwargs.get('I',None)
		if not self.I.calibrated: QtGui.QMessageBox.about(self,'Error','Device Not Calibrated. Check.')
		self.I.set_wave(1e3) #1KHz test
		self.I.select_range('A1',8)
		self.I.select_range('A2',8)
		cap_and_pcs=self.I.read_bulk_flash(self.I.CAP_AND_PCS,5+8*4)  #READY+calibration_string
		if cap_and_pcs[:5]=='READY':
			self.scalers = list(struct.unpack('8f',cap_and_pcs[5:]))
		else:
			#self.displayDialog('Cap and PCS calibration invalid')
			self.scalers = [self.I.SOCKET_CAPACITANCE,1,1,1,1,1,1,1] #socket cap , C0,C1,C2,C3,PCS,SEN,CRRC

		from expeyes.analyticsClass import analyticsClass
		if self.I.timestamp:
			self.setWindowTitle(self.I.generic_name + ' : '+self.I.H.version_string.decode("utf-8")+' : '+self.I.timestamp)
		else:
			self.setWindowTitle(self.I.generic_name + ' : Uncalibrated')
		for a in range(50):
			for b in range(3):
				item = QtGui.QTableWidgetItem();self.tbl.setItem(a,b,item);	item.setText('')
		
		self.group1size = 4
		self.group2size = self.group1size+2
		self.tests = [
		#group 1 begins
		['CAP330',330e-12,self.CAP],
		['WG-A1',1e3,self.WGA1],
		['SQR1-IN2',5e3,self.SQR1IN2],
		['SEN',1e3,self.SEN],
		#['CCS',0.9976e3,self.CCS],
		#group 2 begins
		['SQR2-IN2',10e3,self.SQR2IN2],
		['CAP 1uF',1e-6,self.CAP1uF],
		#group 0 begins . This is automatically executed on start up
		['I2C scan',[],self.I2CScan],
		['CAP_SOCK',42e-12,self.CAP_SOCK],
		['A1[1x]','Calibration',self.A1CAL1],
		['A1[32x]','Calibration',self.A1CAL],
		['A2[1x]','Calibration',self.A2CAL1],
		['A2[32x]','Calibration',self.A2CAL],
		]
		self.tbl.setVerticalHeaderLabels([row[0] for row in self.tests])
		self.tbl.setHorizontalHeaderLabels(['Expected','read','','More'])
		self.tbl.setColumnWidth(0, 90)
		self.tbl.setColumnWidth(1, 120)
		self.tbl.setColumnWidth(2, 100)
		self.tbl.setColumnWidth(3, 80)
		
		#Nominal values for calibration constants
		self.CCS_SCALING=1
		self.socket_cap = 0
		self.RESISTANCE_SCALING=1
		self.CR0=1;self.CR1=1;self.CR2=1;self.CR3=1
		self.CRRC = 1.
		
		self.G0Tests = {}
		self.G1Tests = {}
		self.G2Tests = {}
		for n in range(len(self.tests)) :
			self.tbl.item(n,0).setText(str(self.tests[n][1]))
			################# make readback buttons ##############
			fn = functools.partial(self.tests[n][2],n)
			if n<self.group1size: self.G1Tests[self.tests[n][0]]=(fn)
			elif n<self.group2size: self.G2Tests[self.tests[n][0]]=(fn)
			else: self.G0Tests[self.tests[n][0]]=(fn)
			item = QtGui.QPushButton();item.setText('test'); item.clicked.connect(fn)
			self.tbl.setCellWidget(n, 2, item)
			if len(self.tests[n])==4:
				fn = functools.partial(self.tests[n][3],n)
				item = QtGui.QPushButton();item.setText('Recal'); item.clicked.connect(fn)
				self.tbl.setCellWidget(n, 3, item)



		self.DACPLOT=pg.PlotWidget()
		self.plot_area.addWidget(self.DACPLOT)

		self.WPLOT=pg.PlotWidget()
		self.plot_area.addWidget(self.WPLOT)

		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.DACPLOT.setLabel('left','Error -->', units='V',**labelStyle)
		self.DACPLOT.setLabel('bottom','Actual Voltage -->', units='V',**labelStyle)
		self.DACPLOT.setYRange(-.02,.02)
		self.WPLOT.setLabel('left','Voltage -->', units='V',**labelStyle)
		self.WPLOT.setLabel('bottom','time -->', units='V',**labelStyle)
		self.WPLOT.setYRange(-3.3,3.3)
		self.DacCurves={}
		#self.rebuildLegend(self.DACPLOT)
		for a in self.I.DAC.CHANS:
			self.DacCurves[a] = self.addCurve(self.DACPLOT,a)
		self.p1 = self.addCurve(self.DACPLOT,'tmp')

		#self.rebuildLegend(self.WPLOT)
		self.WCurve = self.addCurve(self.WPLOT,'WG')
		
		self.eval_init()

	def addCurve(self,plot,name,col=(255,0,0)):
		C=pg.PlotCurveItem(name = name,pen = col)
		plot.addItem(C)
		return C
		

	def setSuccess(self,item,val):
		if val : item.setBackground(QtCore.Qt.green)
		else:item.setBackground(QtCore.Qt.red)


	def A1CAL1(self,row):
		item = self.tbl.item(row,1)
		source = self.I.analogInputSources['A1']
		item.setText('%.2f'%(source.calibrationCorrection[0]))
		if not source.calibrationError:
			self.setSuccess(item,1) 
		else:
			self.setSuccess(item,0) 

	def A1CAL(self,row):
		item = self.tbl.item(row,1)
		source = self.I.analogInputSources['A1']
		item.setText('%.2f'%(source.calibrationCorrection[7]))
		if not source.calibrationError:
			self.setSuccess(item,1) 
		else:
			self.setSuccess(item,0) 


	def A2CAL1(self,row):
		item = self.tbl.item(row,1)
		source = self.I.analogInputSources['A2']
		item.setText('%.2f'%(source.calibrationCorrection[0]))
		if not source.calibrationError:
			self.setSuccess(item,1) 
		else:
			self.setSuccess(item,0) 

	def A2CAL(self,row):
		item = self.tbl.item(row,1)
		source = self.I.analogInputSources['A2']
		item.setText('%.2f'%(source.calibrationCorrection[7]))
		if not source.calibrationError:
			self.setSuccess(item,1) 
		else:
			self.setSuccess(item,0) 



	def I2CScan(self,row):
		res = self.I.I2C.scan()
		item = self.tbl.item(row,1)
		item.setText(str(res))
		self.setSuccess(item,1) 

	def SQR1IN2(self,row):
		frq = float(self.tbl.item(row,0).text() )
		self.I.set_sqr1(frq)
		res = self.I.get_freq('IN2',0.2)
		item = self.tbl.item(row,1)
		try:
			item.setText('%.3e'%res)
			if abs(res-frq)<20:	 self.setSuccess(item,1)
			else:	 self.setSuccess(item,0)				
		except Exception as e:
			print (e)
			item.setText('failed'); self.setSuccess(item,0)

	def SQR2IN2(self,row):
		frq = float(self.tbl.item(row,0).text() )
		self.I.set_sqr2(frq)
		res = self.I.get_freq('IN2',0.2)
		item = self.tbl.item(row,1)
		try:
			item.setText('%.3e'%res)
			if abs(res-frq)<20:	 self.setSuccess(item,1)
			else:	 self.setSuccess(item,0)				
		except Exception as e:
			print (e)
			item.setText('failed'); self.setSuccess(item,0)


	def eval_init(self):
		for a in self.G0Tests: self.G0Tests[a]()

	def eval1(self):
		for a in self.G1Tests: self.G1Tests[a]()

	def eval2(self):
		for a in self.G2Tests: self.G2Tests[a]()

	def SEN(self,row):
		res = self.I.get_resistance()
		item = self.tbl.item(row,1)
		if res!=np.inf:
			item.setText(pg.siFormat(res, precision=3, suffix=u"\u03A9", space=True, error=None, minVal=1e-25, allowUnicode=True))
			actual = float(self.tbl.item(row,0).text() )
			#print (res, actual)
			if abs(res-actual)<self.RESISTANCE_ERROR :
				self.setSuccess(item,1) #resistance within error margins
				self.RESISTANCE_SCALING = actual/res
			else :
				self.setSuccess(item,0) 
		else:
			item.setText('Open')
			self.setSuccess(item,0) 


	def CCS(self,row):
		self.I.set_state(CCS=1)
		time.sleep(0.1)
		V = self.I.get_voltage('CCS')
		if V<2.5:
			item = self.tbl.item(row,1)
			res = V/1.1e-3 #assume 1.1mA
			print (V,res)
			item.setText(pg.siFormat(res, precision=3, suffix=u"\u03A9", space=True, error=None, minVal=1e-25, allowUnicode=True))
			actual = float(self.tbl.item(row,0).text() )
			if abs(res-actual)<self.CCS_ERROR :
				self.setSuccess(item,1) #resistance within error margins
				self.CCS_SCALING = actual/res
			else :
				self.setSuccess(item,0) 
		else:
			item.setText('Open')
			self.setSuccess(item,0) 



	def get_capacitance(self,CR): #read capacitance using various current ranges
		GOOD_VOLTS=[2.5,2.8]
		CT=10
		iterations = 0
		start_time=time.time()
		try:
			while (time.time()-start_time)<1:
				if CT>65000:
					QtGui.QMessageBox.about(self,'Cap error','CT too high')
					return 0
				V,C = self.I.__get_capacitance__(CR,0,CT)
				if V>GOOD_VOLTS[0] and V<GOOD_VOLTS[1]:
					print ('Done',V,C)
					return C
				elif CT>30000 and V<0.1:
					QtGui.QMessageBox.about(self,'Cap Error','Capacitance too high for this method')
					return 0
				elif V<GOOD_VOLTS[0] and V>0.01 and CT<30000:
					if GOOD_VOLTS[0]/V >1.1 and iterations<10:
						CT=int(CT*GOOD_VOLTS[0]/V)
						iterations+=1
					elif iterations==10:
						return 0
					else:
						print ('Done',V,C,CT)
						return C
		except Exception as  ex:
			QtGui.QMessageBox.about(self,'error',ex.message)

	def CAP_SOCK(self,row):
		#cap = self.I.get_capacitance()
		
		V = self.I.__get_capacitance_voltage__(1,0, 180)
		Charge_Current = self.I.currents[1]
		cap = (Charge_Current*180*1e-6/V )/self.I.currentScalers[1]
		self.I.SOCKET_CAPACITANCE = cap
		#print (V,cap)
		
		item = self.tbl.item(row,1)
		item.setText(pg.siFormat(cap, precision=3, suffix='F', space=True, minVal=1e-25, allowUnicode=True))
		if abs(cap-float(self.tbl.item(row,0).text() ))<self.CAPACITANCE_ERROR :
			self.setSuccess(item,1) #capacitance within error margins
			self.socket_cap = cap
		else :	self.setSuccess(item,0) 

	def CAP(self,row):
		actual = float(self.tbl.item(row,0).text() )
		cap1 = self.get_capacitance(1)
		self.I.__charge_cap__(0,50000)
		cap2 = self.get_capacitance(2)
		if cap1 and cap2:
			item = self.tbl.item(row,1)
			item.setText('%s,%s'%(pg.siFormat(cap1, precision=4, suffix='F', space=True),pg.siFormat(cap2, precision=3, suffix='F', space=True)))
			self.CR1 = cap1/actual
			self.CR2 = cap2/actual
		else:
			QtGui.QMessageBox.about(self,'Cap error',"Capacitance invalid. \nIf a %sF capacitor is plugged correctly into CAP socket, this may be an issue."%actual)

		if abs(cap1-actual)<self.CAPACITANCE_ERROR : self.setSuccess(item,1) #capacitance within error margins
		else :
			self.setSuccess(item,0) 
			QtGui.QMessageBox.about(self,'Cap error',"Capacitance invalid. \nIf a %sF capacitor is plugged correctly into CAP socket, this may be an issue."%actual)


	def CAP1uF(self,row):
		actual = float(self.tbl.item(row,0).text() )
		cap = self.I.capacitance_via_RC_discharge()
		if cap:
			item = self.tbl.item(row,1)
			item.setText('%s'%(pg.siFormat(cap, precision=4, suffix='F', space=True)))
			self.CRRC = actual/cap
		else:
			QtGui.QMessageBox.about(self,'Cap error',"Capacitance invalid. \nIf a 1uF capacitor is plugged correctly into CAP socket, this may be an issue.")

		if abs(cap-actual)<0.1e-6: self.setSuccess(item,1) #capacitance within error margins
		else :	self.setSuccess(item,0) 


	def __PVA__(self,DAC,ADC,row,rng):
		actuals=[];read=[]
		self.I.DAC.setVoltage(DAC,rng[0])
		time.sleep(.1)
		for a in np.linspace(*rng):
			actuals.append( self.I.DAC.setVoltage(DAC,a) )
			time.sleep(0.02)
			read.append (self.I.get_average_voltage(ADC,samples=5) )
		read = np.array(read)
		actuals = np.array(actuals)
		self.DacCurves[DAC].setData(actuals,read-actuals)
		self.tbl.item(row,0).setText(string.join(['%.3f'%a for a in actuals],' '))
		self.tbl.item(row,1).setText(string.join(['%.3f'%a for a in read-actuals],' '))
		if np.any(abs(read-actuals)>20e-3):self.setSuccess(self.tbl.item(row,1),0)
		else: self.setSuccess(self.tbl.item(row,1),1)



	def PV1A1(self,row):
		self.__PVA__('PV1','A1',row,[-4,4,20])
	def PV2A2(self,row):
		self.__PVA__('PV2','A2',row,[-2.5,2.5,20])


	def __WA__(self,ADC,row):
		self.I.set_wave(1e3) #1KHz test

		x,y = self.I.capture1(ADC,1000,5)#get about five cycles
		
		self.WCurve.setData(x,y)
		self.tbl.item(row,0).setText('1 KHz')
		try:
			amp,frq,ph,off = self.sineFit(x,y)
			self.tbl.item(row,1).setText(pg.siFormat(frq, precision=3, suffix='Hz', space=True)+','+pg.siFormat(amp, precision=3, suffix='V', space=True))
			if abs(frq-1e3)>2:
				self.setSuccess(self.tbl.item(row,1),0)
				#print(frq)
			else: self.setSuccess(self.tbl.item(row,1),1)
		except:
			self.tbl.item(row,1).setText('Check Connections')
			self.setSuccess(self.tbl.item(row,1),0)

	def WGA1(self,row):
		self.__WA__('A1',row)


	def correct(self):
		self.scalers[0] = self.socket_cap
		self.scalers[1] *= self.CR0;self.scalers[2]*=self.CR1;self.scalers[3]*=self.CR2;self.scalers[4]*=self.CR3;
		self.scalers[5] *= self.CCS_SCALING  #slope
		self.scalers[6] *= self.RESISTANCE_SCALING
		self.scalers[7] *= self.CRRC
		
		#QtGui.QMessageBox.about(self,'info','loading %s\nPCS SCALING:%s\nCR0 : %.3f\nCR1 : %.3f\nCR2 : %.3f\nCR3 : %.3f\nRES : %.3f\nCap RC : %.3f\n'%(self.scalers,self.CCS_SCALING,self.CR0,self.CR1,self.CR2,self.CR3,self.RESISTANCE_SCALING,self.CRRC))
		cap_and_pcs=self.I.write_bulk_flash(self.I.CAP_AND_PCS,self.I.__stoa__('READY'+struct.pack('8f',*self.scalers)))  #READY+calibration_string
		self.I.SOCKET_CAPACITANCE = self.scalers[0]
		self.I.__calibrate_ctmu__(self.scalers[1:5])
		self.I.resistanceScaling = self.scalers[6]
		self.I.CAP_RC_SCALING = self.scalers[7]
		#self.G2Tests['SEN']()
		#self.G2Tests['PCS-CH3']()


	def __del__(self):
		print ('bye')

	def closeEvent(self, evnt):
		evnt.ignore()
		self.askBeforeQuit()


	def askBeforeQuit(self):
		global app
		reply = QtGui.QMessageBox.question(self, 'Warning', 'Save and Quit?\n\nloading %s\nPCS SCALING:%s\nCR0 : %.3f\nCR1 : %.3f\nCR2 : %.3f\nCR3 : %.3f\nRES : %.3f\nCap RC : %.3f\n'%(self.scalers,self.CCS_SCALING,self.CR0,self.CR1,self.CR2,self.CR3,self.RESISTANCE_SCALING,self.CRRC), QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		if reply == QtGui.QMessageBox.Yes:
			self.running =False
			self.finished=True
			self.save()
			app.quit()
		else:
			self.running =False
			self.finished=True
			print ('Did not save/upload calibration')
			app.quit()



	def save(self):
		self.correct()
		p = QtGui.QPixmap.grabWindow(self.tab1.winId())
		from os.path import expanduser
		home = expanduser("~")
		path = os.path.join(home,'test '+self.I.timestamp+'.png')
		p.save(path)
		#QtGui.QMessageBox.about(self,'saved to ',path)
		print ('saved to ',path)


	def sineFunc(self,x, a1, a2, a3,a4):
	    return a4 + a1*np.sin(abs(a2*(2*np.pi))*x + a3)
	    
	def sineFit(self,xReal,yReal,**kwargs):
		N=len(xReal)
		xReal*=1e3 #convert mS to uS
		OFFSET = (yReal.max()+yReal.min())/2.
		yhat = self.fftpack.rfft(yReal-OFFSET)
		idx = (yhat**2).argmax()
		freqs = self.fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
		frequency = kwargs.get('freq',freqs[idx])  
		frequency/=(2*np.pi) #Convert angular velocity to freq
		amplitude = kwargs.get('amp',(yReal.max()-yReal.min())/2.0)
		phase=kwargs.get('phase',0) #.5*np.pi*((yReal[0]-offset)/amplitude)
		guess = [amplitude, frequency, phase,0]
		try:
			(amplitude, frequency, phase,offset), pcov = self.optimize.curve_fit(self.sineFunc, xReal, yReal-OFFSET, guess)
			offset+=OFFSET
			ph = ((phase)*180/(np.pi))
			if(frequency<0):
				#print ('negative frq')
				return False

			if(amplitude<0):
				ph-=180

			if(ph<0):ph = (ph+720)%360
			freq=1e6*abs(frequency)
			amp=abs(amplitude)
			pcov[0]*=1e6
			#print (pcov)
			if(abs(pcov[-1][0])>1e-6):
				False
			return [amp, freq, offset,ph]
		except:
			return False


if __name__ == "__main__":
    import expeyes.eyes17 as eyes
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=eyes.open(verbose=True))
    myapp.show()
    sys.exit(app.exec_())

