# coding = GBK
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# ============================================# read data
muti = False
mutinum = 0
title_name = ''
data = []
names = []
hours = []
pops = []
lats = []
lons = []
TY = []
file = "/Users/hsw/Desktop/historytrack.txt"
inittime = ''
title = ''
save = '/Users/hsw/Desktop/sample.png'
author = ''

# ============================================# input time
inittime = input("Enter Init time:(YYYYMMDDHH)");
author = input("author(can remain blank):");
if author == '':
    author = 'Meteorological Service Center of HSEFZ'
# ============================================# read data
fh = open(file)
for line in fh:
    info = line.split()
    data.append(info[0])
    hours.append(info[3])
    names.append(info[2])
    TY.append(info[1])
    pops.append(float(info[7]))
    lat = float(info[4][:-1])
    if info[2][-1] == 'S': lat = -lat
    lats.append(lat)
    lon = float(info[5][:-1])
    if info[3][-1] == 'W': lon = -lon + 360.0
    lons.append(lon)

# ============================================ #calculate the boarder of the map
maxlon = 0;
minlon = 9999;
maxlat = 0;
minlat = 9999;
for i in range(1, len(lons)):
    if(lons[i] > maxlon):
        maxlon = lons[i]
    if (lons[i] < minlon):
        minlon = lons[i]
    if (lats[i] > maxlat):
        maxlat = lats[i]
    if (lats[i] < minlat):
        minlat = lats[i]

maxlon=maxlon+7
minlon=minlon-7
maxlat=maxlat+7
minlat=minlat-7
print(maxlat)
# ============================================

plt.figure(figsize=(14, 9), dpi=80)
axes = plt.subplot(111)
# set up map projection with
# use low resolution coastlines.
map = Basemap(llcrnrlon=100, llcrnrlat=5, urcrnrlon=170, urcrnrlat=45, \
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
map.drawmeridians(np.arange(0, 360, 10),labels=[0,0,0,1],fontsize=10)
map.drawparallels(np.arange(-90, 90, 10))
map.drawparallels(np.arange(-90, 90, 10),labels=[1,0,0,0],fontsize=10)
# Fill continent wit a different color
map.fillcontinents(color='#FFFFFF', lake_color='#87CEFA', zorder=0)

# ============================================#draw history typhoon track
for i in range(len(lons)-1):
    # ============================================#find if there are new typhoons
    if(data[i]=="00" or data[i+1]=="00"):
        mutinum=mutinum+1
        muti = True
        if data[i]=="00":
            title_name = title_name + ", " +TY[i+1]
        continue
        # ============================================#track for the same typhoon
    else:
        if muti == False:
            title_name = TY[i]
        # nylat, nylon are lat/lon of A
        Alat = lats[i];
        Alon = lons[i]
        # lonlat, lonlon are lat/lon of B.
        Blat = lats[i + 1]
        Blon = lons[i + 1]
        if data[i] == 'T':
            map.drawgreatcircle(Alon,Alat,Blon,Blat,linewidth=0.8,color='b',ls='--')
        else:
            map.drawgreatcircle(Alon, Alat, Blon, Blat, linewidth=0.5, color='black', ls='-')

# compute native map projection coordinates of lat/lon grid.
x, y = map(lons, lats)
max_pop = max(pops)
# Plot each city in a loop.
# Set some parameters
size_factor = 100.0
x_offset = 20.0
y_offset = -20.0
rotation = 0
temp=0

#draw future typhoon point
c="b"
for i, j, k, name, d, h in zip(x, y, pops, names, data, hours):
    temp = temp+1
    size = size_factor * k / max_pop

    if name == "00" and c == "g":
        c = "r"
    if name == "00" and c == "b":
        c = "g"

    if h[len(h)-1:len(h)] == 'T' and h != 'T':
        #plt.text(i + 20,j - 20, name + hours[len(hours)-1],rotation=rotation,fontsize=12)
        plt.text(i + 20, j - 20, name + h, rotation=rotation, fontsize=12)
    if d == 'T':
        plt.text(i + 20, j - 20, name + 'T', rotation=rotation, fontsize=12)
        if name == '12':
            map.scatter(i, j, s = 450, c=c, marker='o', alpha=0.5)
        if name == '24':
            map.scatter(i, j, s = 900, c=c, marker='o', alpha=0.5)
        if name == '36':
            map.scatter(i, j, s = 1350, c=c, marker='o', alpha=0.5)
        if name == '48':
            map.scatter(i, j, s = 1800, c=c, marker='o', alpha=0.5)
        if name == '60':
            map.scatter(i, j, s = 2250, c=c, marker='o', alpha=0.5)
        if name == '72':
            map.scatter(i, j, s = 2700, c=c, marker='o', alpha=0.5)
        if name == '96':
            map.scatter(i, j, s = 3600, c=c, marker='o', alpha=0.5)
        if name == '120':
            map.scatter(i, j, s = 4500, c=c, marker='o', alpha=0.5)
        if name == '144':
            map.scatter(i, j, s = 5400, c=c, marker='o', alpha=0.5)
        if name == '168':
            map.scatter(i, j, s = 6300, c=c, marker='o', alpha=0.5)
        if name == '192':
            map.scatter(i, j, s = 7200, c=c, marker='o', alpha=0.5)
        if name == '206':
            map.scatter(i, j, s = 8100, c=c, marker='o', alpha=0.5)
        if name == '240':
            map.scatter(i, j, s = 10000, c=c, marker='o', alpha=0.5)

#draw future typhoon point
for i, j, k, name, d in zip(x, y, pops, names, data):
    temp = temp+1
    size = size_factor * k / max_pop
    if 0.0 < k and k <= 20:
        cs1 = map.scatter(i, j, s=50, marker='x', color='#708090')
    if 20 < k and k <= 35:
        cs2 = map.scatter(i, j, s=50, marker='x', color='#FFFF00')
    if 35 < k and k <= 50:
        cs3 = map.scatter(i, j, s=50, marker='o', color='#6495ED')
    if 50 < k and k <= 60:
        cs4 = map.scatter(i, j, s=50, marker='o', color='#3CB371')
    if 60 < k and k <= 85:
        cs5 = map.scatter(i, j, s=60, marker='o', color='#FFA500')
    if 85 <= k and k <= 100:
        cs5 = map.scatter(i, j, s=60, marker='o', color='#FF00FF')
    if 100 < k:
        cs6 = map.scatter(i, j, s=60, marker='o', color='#DC143C')

print (lons, lats)

title = 'Typhoon \'' + title_name + '\' history track and forecast\nForecast Initial time: ' + inittime + '00UTC\n' + author



# ============================================#define legends
blue_line = mlines.Line2D([], [], color='blue', marker='o',
                          markersize=5, label='forecast track',ls='--')
black_line = mlines.Line2D([], [], color='black', marker='o',
                          markersize=5, label='history track',ls='-')
a = mlines.Line2D([], [], color='#708090', marker='x',
                          markersize=5, label='Tropical Disturbance',ls='')
b = mlines.Line2D([], [], color='#FFFF00', marker='x',
                          markersize=5, label='Tropical Depression',ls='')
c = mlines.Line2D([], [], color='#6495ED', marker='o',
                          markersize=5, label='Tropical Storm',ls='')
d = mlines.Line2D([], [], color='#3CB371', marker='o',
                          markersize=5, label='Severe Tropical Storm',ls='')
e = mlines.Line2D([], [], color='#FFA500', marker='o',
                          markersize=5, label='Typhoon',ls='')
f = mlines.Line2D([], [], color='#FF00FF', marker='o',
                          markersize=5, label='Severe Typhoon',ls='')
g = mlines.Line2D([], [], color='#DC143C', marker='o',
                          markersize=5, label='Super Typhoon',ls='')
plt.legend(handles=[black_line, blue_line, a, b, c, d, e, f, g])
plt.title(title)

# plt.show()
plt.savefig(save, dpi=100)
plt.show()
