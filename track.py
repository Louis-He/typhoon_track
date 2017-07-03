from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=90.,llcrnrlat=10.,urcrnrlon=160.,urcrnrlat=50.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)

# 读取台风路径
time = []
lon = []
lat = []
intensity = []
fh = open("/Users/hsw/Desktop/typhoon.txt")
for line in fh:
    info = line.split()
    time.append(info[0])
    intensity.append(float(info[1]))
    lat  = float(info[2][:-1])
    if info[2][-1] == 'S': lat = -lat
    lats.append(lat)
    lon  = float(info[3][:-1])
    if info[3][-1] == 'W': lon = -lon + 360.0
    lons.append(lon)

# nylat, nylon are lat/lon of A
Alat = 31.25; Alon = 121.25
# lonlat, lonlon are lat/lon of B.
Blat = 25.55; Blon = 121.55 
# draw great circle route between A & B
m.drawgreatcircle(Alon,Alat,Blon,Blat,linewidth=2,color='b')

m.drawcoastlines()
m.fillcontinents()
# draw parallels
m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# draw meridians
m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
ax.set_title('Great Circle from New York to London')
plt.show()
