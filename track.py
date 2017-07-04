from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# ============================================# read data
names = []
pops = []
lats = []
lons = []
file = ''
title = '@Louis_He'
save = ''
fh = open(file)
for line in fh:
    info = line.split()
    names.append(info[0])
    pops.append(float(info[1]))
    lat = float(info[2][:-1])
    if info[2][-1] == 'S': lat = -lat
    lats.append(lat)
    lon = float(info[3][:-1])
    if info[3][-1] == 'W': lon = -lon + 360.0
    lons.append(lon)

# ============================================
plt.figure(figsize=(14, 9), dpi=80)
axes = plt.subplot(111)
# set up map projection with
# use low resolution coastlines.
map = Basemap(llcrnrlon=100., llcrnrlat=5., urcrnrlon=170., urcrnrlat=50., \
              rsphere=(6378137.00, 6356752.3142), \
              resolution='l', projection='merc', \
              lat_0=40., lon_0=-20., lat_ts=20.)
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='#87CEFA')#689CD2
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0, 360, 10))
map.drawparallels(np.arange(-90, 90, 10))
# Fill continent wit a different color
map.fillcontinents(color='#FFFFFF', lake_color='#87CEFA', zorder=0)

#draw future typhoon track
for i in range(len(lons)-1):
    # nylat, nylon are lat/lon of A
    Alat = lats[i]; Alon = lons[i]
    # lonlat, lonlon are lat/lon of B.
    Blat = lats[i+1]; Blon = lons[i+1]
    map.drawgreatcircle(Alon,Alat,Blon,Blat,linewidth=2,color='b',ls='--')

# compute native map projection coordinates of lat/lon grid.
x, y = map(lons, lats)
max_pop = max(pops)
# Plot each city in a loop.
# Set some parameters
size_factor = 100.0
x_offset = 20.0
y_offset = -20.0
rotation = 0

#draw future typhoon point
for i, j, k, name in zip(x, y, pops, names):
    size = size_factor * k / max_pop

    if 0.0 < k and k <= 10.8:
        cs1 = map.scatter(i, j, s=50, marker='x', color='#708090')
    if 10.8 < k and k < 17.1:
        cs2 = map.scatter(i, j, s=50, marker='x', color='#FFFF00')
    if 17.1 < k and k < 24.4:
        cs3 = map.scatter(i, j, s=50, marker='o', color='#6495ED')
    if 24.4 < k and k < 32.6:
        cs4 = map.scatter(i, j, s=50, marker='o', color='#3CB371')
    if 32.6 < k and k < 41.4:
        cs5 = map.scatter(i, j, s=60, marker='o', color='#FFA500')
    if 41.4 < k and k < 50.9:
        cs5 = map.scatter(i, j, s=60, marker='o', color='#FF00FF')
    if 50.9 < k:
        cs6 = map.scatter(i, j, s=60, marker='o', color='#DC143C')

    plt.text(i + 20,j - 20,name,rotation=rotation,fontsize=12)

print (lons, lats)
blue_line = mlines.Line2D([], [], color='blue', marker='o',
                          markersize=5, label='future typhoon track',ls='--')
a = mlines.Line2D([], [], color='#708090', marker='x',
                          markersize=5, label='Tropical Disturbulance',ls='')
b = mlines.Line2D([], [], color='#FFFF00', marker='x',
                          markersize=5, label='Tropical Depression',ls='')
c = mlines.Line2D([], [], color='#6495ED', marker='o',
                          markersize=5, label='Tropical Storm',ls='')
d = mlines.Line2D([], [], color='#3CB371', marker='o',
                          markersize=5, label='Strong Tropical Storm',ls='')
e = mlines.Line2D([], [], color='#FFA500', marker='o',
                          markersize=5, label='Typhoon',ls='')
f = mlines.Line2D([], [], color='#FF00FF', marker='o',
                          markersize=5, label='Strong Typhoon',ls='')
g = mlines.Line2D([], [], color='#DC143C', marker='o',
                          markersize=5, label='Super Typhoon',ls='')
plt.legend(handles=[blue_line, a, b, c, d, e, f, g])
plt.title(title)

# plt.show()
plt.savefig(save, dpi=100)
plt.show()
