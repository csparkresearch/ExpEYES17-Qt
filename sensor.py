import expeyes.eyes17, time
from expeyes.SENSORS import MPU6050

p=expeyes.eyes17.open()
print p.I2C.scan()

S = MPU6050.connect(p.I2C)
print S.WhoAmI()

print S.WhoAmI_AK8963()

while 1:
	print S.getMag() #[Mx,My,Mz]

