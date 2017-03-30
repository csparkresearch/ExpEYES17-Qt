import inspect
class test:
	funclist = []
	def __init__(self):
		print ('go')
		def func(*args,**kwargs):
			print (args,kwargs)
			F(*args,**kwargs)
		setattr(self,'set_pv1',func)


P = test()
for a in dir(P):
	attr = getattr(P,a)
	if inspect.ismethod(attr) and a!='__init__':
		print (attr)
P.set_pv1('asd')
