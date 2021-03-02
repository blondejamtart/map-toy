from matplotlib import pyplot
from PIL import Image
import numpy

sz = 101
hf = 50

im = Image.open('/home/falcon/Downloads/wrld-11/mercrator-grey.png')

# stole this from d3-geo-projections
def transformPoint(lam, phi):
	pt = [
		lam * (0.975534 + phi**2 * (-0.119161 + lam**2 * -0.0143059 + phi**2 * -0.0547009)),
		phi * (1.00384 + lam**2 * (0.0802894 + phi**2 * -0.02855 + lam**2 * 0.000199025) + phi**2 * (0.0998909 + phi**2 * -0.0491032))
	]
	return pt

# l -> -pi to pi, p -> -pi/2 to pi/2 (polar co-ords on surface)
l = (numpy.array(range(sz)) - hf) * numpy.pi * (2.0/(sz-1))
p = (numpy.array(range(sz)) - hf) * numpy.pi * (1.0/(sz-1))

grdX = numpy.zeros((sz,sz))
grdY = numpy.zeros((sz,sz))

for i in range(sz):
	for j in range(sz):
		grdX[i,j], grdY[i,j] = transformPoint(l[i], p[j])

fig = pyplot.figure()
for i in range(0,sz, 10):
	pyplot.plot(grdX[:,i], grdY[:,i])
	pyplot.plot(grdX[i,:], grdY[i,:])

pyplot.show()

merc = numpy.array(im)
