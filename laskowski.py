from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D 

from PIL import Image

from progress.bar import IncrementalBar
import numpy
import math

sz_x = 101
sz_y = 101

im = Image.open('/home/falcon/Git/map-toy/miller_cyl_world.png')
merc = numpy.array(im)

old = numpy.array(im)
merc[:,:500,:] = old[:, 1500:, :]
merc[:,500:,:] = old[:, :1500, :]

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
reproj = numpy.zeros(merc.shape, dtype=merc.dtype)

bar = IncrementalBar('Transforming points', max=sz_x)
for i in range(sz_x):
    for j in range(sz_y):
        grdX[i,j], grdY[i,j] = transformPoint(l[i], p[j])
    bar.next()
bar.finish()

xRange = grdX.max() - grdX.min()
yRange = grdY.max() - grdY.min()

grdX = (grdX - grdX.min())*((sz_x-1)/xRange)
grdY = (grdY - grdY.min())*((sz_y-1)/yRange)

bar = IncrementalBar('Remapping image    ', max=sz_x)
for i in range(sz_x):
    for j in range(sz_y):
        #err[i,j] = math.sqrt(abs(grdX[i,j] - round(grdX[i,j]))**2 + abs(grdY[i,j] - round(grdY[i,j]))**2)
        hitCount[round(grdX[i,j]),round(grdY[i,j])] += 1
        reproj[round(grdY[i,j]),round(grdX[i,j]),:]=merc[j,i,:]
    bar.next()
bar.finish()

misses = 0
bar = IncrementalBar('Interpolating image', max=sz_x)
for i in range(sz_x):
    for j in range(sz_y):
        if hitCount[i,j] == 0 and 0 < i and i < sz_x-1 and 0 < j and j < sz_y-1 :
            di = i
            dj = j
            if hitCount[i+1,j] != 0:
                di = i+1
            elif hitCount[i,j+1] != 0:
                dj = j+1
            elif hitCount[i-1,j] != 0:
                di = i-1
            elif hitCount[i,j-1] != 0:
                dj = j-1
            else:
                misses += 1
            reproj[j,i,:]=reproj[dj,di,:]
    bar.next()
bar.finish()
print("%d misses" % misses)
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
pyplot.imshow(merc[:,:,0])
pyplot.show()
pyplot.imshow(reproj[:,:,0])
pyplot.show()

