import gettext
gettext.bindtextdomain("expeyes")
gettext.textdomain('expeyes')
_ = gettext.gettext

import expeyes.eyes17, expeyes.eyeplot17 as eyeplot,sys
VER = sys.version[0]
if VER == '3':
	from tkinter import *
else:
	from Tkinter import *


def update():
	v = p.get_voltage('A1')
	if v == v:   #is it NaN
		A1.config(text=_('A1 = %5.3f volts'%(v)))
	v = p.get_voltage('A2')
	if v == v:   #is it NaN
		A2.config(text=_('A2 = %5.3f volts'%(v)))
	
	v = p.get_voltage('A3')
	if v == v:   #is it NaN
		A3.config(text=_('A3 = %5.3f volts'%(v)))
		
	w.after(500,update)
	
p=expeyes.eyes17.open()
w = Tk()
A1 = Label(text=_(''), font=("Helvetica", 26))
A1.pack(side=TOP)
A2 = Label(text=_(''), font=("Helvetica", 26))
A2.pack(side=TOP)
A3 = Label(text=_(''), font=("Helvetica", 26))
A3.pack(side=TOP)
Button(text=_('QUIT'), command=sys.exit).pack(side=TOP)
w.title(_('EYES-17: Measuring voltage'))
w.after(500,update)
w.mainloop()

