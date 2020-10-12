# A simple script to plot storm track data from ATCF
# Author: Imran Mahmood

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(8,8)) #WxH 800x800

ax = plt.axes(projection=ccrs.PlateCarree())

plt.title('October 2020  NW Pacific Invest and Tropical Cyclone Tracks')
ax.set_extent([98.0, 150.0, 0.0, 35.0], ccrs.PlateCarree())
ax.coastlines(resolution='50m')

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS)

gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle=':')
gl.top_labels = False
gl.right_labels = False

# Draw PAR line
x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
plt.plot(x_values, y_values, linewidth=1)
plt.text(120.0, 4.5, 'PHL Area of Responsibility', fontsize=8)

markersize=3
lpacol='gray'
tdcol='blue'
tscol='yellow'
tycol='red'

textstr = '\n'.join((
	'Legend:',
    'Invest / LPA',
    'Tropical Depression',
    'Tropical Storm',
	'Typhoon'))

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
		

with open('data/trackfile-16W.txt', 'r') as f:
    lat = []
    lon = []
    wnd = []
    for line in f:
        if not line.strip() or line.startswith('@') or line.startswith('#'): 
            continue
        row = line.split()
        lat.append(float(row[5][:-1])) # remove last character from coords and add to list
        lon.append(float(row[4][:-1]))
        wnd.append(float(row[7]))
		
        col = []
  
        for i in range(0, len(wnd)): 
            if wnd[i] < 25: 
                col.append(lpacol)   
            elif wnd[i] in range(25, 35): 
                col.append(tdcol)
            elif wnd[i] in range(35, 65):
                col.append(tscol)
            else:
                col.append(tycol)
				
        for i in range(len(wnd)):
            plt.plot(lat[i], lon[i],  markersize=markersize, marker='o', color=col[i], transform=ccrs.Geodetic())

#91W
plt.text(112.5, 12.3, ' 91W', fontsize=10, transform=ccrs.Geodetic());
plt.plot(112.5, 12.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(112.0, 12.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(111.6, 12.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(111.1, 12.2,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(110.6, 12.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(110.0, 12.2,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(109.3, 12.4,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(108.5, 12.5,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())

#17W Linfa
plt.text(125.7, 13.5, ' Linfa', fontsize=10, transform=ccrs.Geodetic());
plt.plot(125.3, 13.6,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(124.8, 13.7,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(124.4, 13.8,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(124.1, 13.9,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(123.0, 14.0,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(122.1, 13.9,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(120.2, 13.7,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(118.2, 13.2,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(117.4, 13.1,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(116.5, 13.0,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(115.7, 13.1,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(114.8, 13.5,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
plt.plot(114.1, 13.8,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
plt.plot(113.3, 14.3,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
plt.plot(112.2, 14.7,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(110.8, 14.8,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(109.3, 15.0,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(108.3, 15.2,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(107.4, 15.4,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(106.3, 15.0,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
plt.plot(105.6, 14.7,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
#--active

#18W Nangka

plt.figtext(0.99, 0.01, 'Track and intensity data from JTWC | Plotted by Imran Mahmood', fontsize=8, horizontalalignment='right')
plt.tight_layout()
plt.show()