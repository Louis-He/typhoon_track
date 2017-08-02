import urllib.request
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# ============================================# read data from EC web
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    print("DATA RECEIVED! ")
    return html

time = input("Enter Init time:(YYYYMMDDHH)");

url = "http://ftp.emc.ncep.noaa.gov/gc_wmb/jpeng/aemn/" + time + "/trak.aemn.atcfunix." + time  #EC
print("REQUESTING..." + url)
html = str(getHtml(url), encoding = "utf-8")

url = "http://ftp.emc.ncep.noaa.gov/gc_wmb/jpeng/aemn/" + time + "/trak.avn.atcfunix." + time  #EC
print("REQUESTING..." + url)
html = html + str(getHtml(url), encoding = "utf-8")

for i in range(1,21):
    if i < 10:
        member = '0' + str(i)
    else:
        member = str(i)
    url = "http://ftp.emc.ncep.noaa.gov/gc_wmb/jpeng/aemn/" + time + "/trak.ap"+ member +".atcfunix." + time  # EC
    print("REQUESTING..." + url)
    html = html + str(getHtml(url), encoding="utf-8")

print('ANALYZING DATA...')
# ============================================# initialize variables
title_name = ''
sea = []
number = []
inittime = []
hours = []
intensity = []
lats = []
lons = []
members = []
file = "/Users/hsw/Desktop/historytrack.txt"
title = ''
save = '/Users/hsw/Desktop/GFS.png'

# ============================================# analyze EC data
while (html.find('\n')!=-1):
    line = html[0 : html.find('\n')]
    print("DECODING.../"+line)
    info = []

    while line.find(",") != -1:
        info.append(line[0:line.find(",")])
        line = line[line.find(",")+2:len(line)]
    sea.append(info[0].replace(' ',''))
    number.append(info[1].replace(' ',''))
    inittime.append(info[2].replace(' ',''))
    members.append(info[4].replace(' ',''))
    hours.append(info[5].replace(' ',''))
    intensity.append(float(info[8].replace(' ','')))

    if (info[6].replace(' ', ''))[:-1] != '':
        lat = float((info[6].replace(' ',''))[:-1])
    if (info[6].replace(' ',''))[-1] == 'S': lat = -lat
    lats.append(lat/10)

    if (info[7].replace(' ', ''))[:-1] != '':
        lon = float((info[7].replace(' ',''))[:-1])
    if (info[7].replace(' ',''))[-1] == 'W': lon = -lon + 360.0
    lons.append(lon/10)

    html = html[html.find('\n')+1 : ]


# ============================================
print('PLOTTING...')
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
print ("PLOTTING DETERMINANT FORECAST...")
for i in range(len(lons)-1):
    # ============================================#find if there are new typhoons
    if(sea[i]=="WP" and members[i]=="AEMN"):
        # nylat, nylon are lat/lon of A
        Alat = lats[i];
        Alon = lons[i]
        # lonlat, lonlon are lat/lon of B.
        Blat = lats[i + 1]
        Blon = lons[i + 1]
        if i == 0 or (number[i] == number[i + 1]):
            map.drawgreatcircle(Alon, Alat, Blon, Blat, linewidth=0.5, color='b', ls='--')

# compute native map projection coordinates of lat/lon grid.
x, y = map(lons, lats)
max_pop = max(intensity)
# Plot each city in a loop.
# Set some parameters
size_factor = 100.0
x_offset = 20.0
y_offset = -20.0
rotation = 0
temp=0

#draw future typhoon point
print ("PLOTTING MEMBERS FORECAST...")
c="b"
lastty = number[0]
for i, j, k, name, s, h ,m in zip(x, y, intensity, number, sea, hours, members):
    temp = temp + 1
    size = size_factor * k / max_pop

    if s == "WP" and number == lastty and c == "g":
        lastty = number
        c = "r"
    if  s == "WP" and name == lastty and c == "b":
        lastty = number
        c = "g"

    if m == "AEMN" and h == "000":
        #plt.text(i + 20,j - 20, name + hours[len(hours)-1],rotation=rotation,fontsize=12)
        plt.text(i + 20, j - 20, name + "W init", rotation=rotation, fontsize=12)
    '''
    else:
        #plt.text(i + 20, j - 20, h + 'T', rotation=rotation, fontsize=12)

        if h == '24':
            map.scatter(i, j, s = 900, c=c, marker='o', alpha=0.5)
        if h == '48':
            map.scatter(i, j, s = 1800, c=c, marker='o', alpha=0.5)
        if name == '60':
            map.scatter(i, j, s = 2250, c=c, marker='o', alpha=0.5)
        if h == '72':
            map.scatter(i, j, s = 2700, c=c, marker='o', alpha=0.5)
        if h == '96':
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
    '''
#draw future typhoon point
print ("PLOTTING FORECAST COORDINATES...")
for i, j, k, name, s, h in zip(x, y, intensity, number, sea, hours):
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

print (" CREATING DIAGRAM...")

title = 'GFS Ensemble Track and Intensitiy Prediction in Western Pacific\nForecast Initial time: ' + inittime[0] + '00UTC\nMeteorological Service Center of HSEFZ'



# ============================================#define legends
blue_line = mlines.Line2D([], [], color='blue', marker='o',
                          markersize=5, label='forecast track',ls='--')
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
plt.legend(handles=[blue_line, a, b, c, d, e, f, g])
plt.title(title)
print ("SAVING DIAGRAM...")
# plt.show()
plt.savefig(save, dpi=100)
plt.show()
print ("COMPLETE!")