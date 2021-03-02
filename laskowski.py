from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D 

from PIL import Image
import numpy
import math

sz_x = 101
sz_y = 101

im = Image.open('/home/falcon/Downloads/wrld-11/mercrator-grey.png')
merc = numpy.array(im)
print("Image is %d by %d (by %d)" % merc.shape)

sz_x = merc.shape[1]
sz_y = merc.shape[0]

# stole this from d3-geo-projections
def transformPoint(lam, phi):
    pt = [
        lam * (0.975534 + phi**2 * (-0.119161 + lam**2 * -0.0143059 + phi**2 * -0.0547009)),
        phi * (1.00384 + lam**2 * (0.0802894 + phi**2 * -0.02855 + lam**2 * 0.000199025) + phi**2 * (0.0998909 + phi**2 * -0.0491032))
    ]
    return pt

# l -> -pi to pi, p -> -pi/2 to pi/2 (polar co-ords on surface)
l = numpy.linspace(-numpy.pi, numpy.pi, sz_x)
p = numpy.linspace(-0.5*numpy.pi, 0.5*numpy.pi, sz_y)


grdX = numpy.zeros((sz_x,sz_y))
grdY = numpy.zeros((sz_x,sz_y))
err = numpy.zeros((sz_x,sz_y))
hitCount = numpy.zeros((sz_x,sz_y))
reproj = numpy.zeros((sz_x,sz_y))

for i in range(sz_x):
    for j in range(sz_y):
        grdX[i,j], grdY[i,j] = transformPoint(l[i], p[j])

xRange = grdX.max() - grdX.min()
yRange = grdY.max() - grdY.min()

grdX = (grdX - grdX.min())*((sz_x-1)/xRange)
grdY = (grdY - grdY.min())*((sz_y-1)/yRange)

for i in range(sz_x):
    for j in range(sz_y):
        err[i,j] = math.sqrt(abs(grdX[i,j] - round(grdX[i,j]))**2 + abs(grdY[i,j] - round(grdY[i,j]))**2)
        hitCount[round(grdX[i,j]),round(grdY[i,j])] += 1
        reproj[round(grdX[i,j]),round(grdY[i,j])]=numpy.sum(merc[round(grdY[i,j]),round(grdX[i,j]),:3])

fig = pyplot.figure()
#ax = fig.add_subplot(111, projection='3d')

#for i in range(0,sz_y, 10):
#    ax.scatter(grdX[:,i], grdY[:,i], merc[i,:,1])

for i in range(0,sz_y, 100):
    pyplot.plot(grdX[:,i], grdY[:,i])
for i in range(0,sz_x, 100):
    pyplot.plot(grdX[i,:], grdY[i,:])

pyplot.show()
#pyplot.imshow(err)
#pyplot.show()
#pyplot.imshow(hitCount > 0)
pyplot.imshow(reproj)
pyplot.show()

