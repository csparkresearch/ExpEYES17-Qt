import expeyes.eyes17, time

p=expeyes.eyes17.open(verbose=True)
print p.get_capacitance()
#while 1:print p.duty_cycle('IN2')
'''
S = MPU6050.connect(p.I2C)

print S.getRaw() #[Ax,Ay,Az,Temperature,Gx,Gy,Gz]
print S.getAccel() #[Ax,Ay,Az]
print S.getGyro() #[Gx,Gy,Gz]
'''
