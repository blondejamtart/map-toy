from matplotlib import pyplot
import numpy

def transformPoint(lam, phi):
	pt = [
		lam * (0.975534 + phi**2 * (-0.119161 + lam**2 * -0.0143059 + phi**2 * -0.0547009)),
		phi * (1.00384 + lam**2 * (0.0802894 + phi**2 * -0.02855 + lam**2 * 0.000199025) + phi**2 * (0.0998909 + phi**2 * -0.0491032))
	]
	return pt

l = (numpy.array(range(100)) - 50) * numpy.pi * 0.02
p = (numpy.array(range(100)) - 50) * numpy.pi * 0.01

grdX = numpy.zeros((100,100))
grdY = numpy.zeros((100,100))

for i in range(100):
	for j in range(100):
		grdX[i,j], grdY[i,j] = transformPoint(l[i], p[j])

fig = pyplot.figure()
for i in range(100):
	pyplot.plot(grdX[:,i], grdY[:,i])

pyplot.show()
