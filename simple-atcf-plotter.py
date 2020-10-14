# A simple script to plot storm track data from ATCF
# Author: Imran Mahmood

from contextlib import ExitStack
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

plt.rcParams['axes.facecolor'] = '#0e1111'

fig = plt.figure(figsize=(8,8)) #WxH 800x800

ax = plt.axes(projection=ccrs.PlateCarree())

plt.title('')
ax.set_extent([98.0, 150.0, -2.0, 37.0], ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.LAKES)
#ax.add_feature(cfeature.OCEAN)

gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle=':')
gl.top_labels = False
gl.right_labels = False

# Draw PAR line
x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
plt.plot(x_values, y_values, linewidth=1)
plt.text(125.0, 4.0, 'PHL Area of Responsibility', fontsize=8, color='skyblue')

markersize=15
lpamarker='^'
marker='o'
lpacol='gray'
tdcol='blue'
tscol='green'
ty1col='#CCCC00'
ty2col='#999900'
ty3col='darkorange'
ty4col='orangered'
ty5col='red'

# Plot legends
lpa = mlines.Line2D([], [], color=lpacol, marker=marker, linestyle='None',
                          markersize=10, label='Invest / LPA')
td = mlines.Line2D([], [], color=tdcol, marker=marker, linestyle='None',
                          markersize=10, label='Tropical Depression')
ts = mlines.Line2D([], [], color=tscol, marker=marker, linestyle='None',
                          markersize=10, label='Tropical Storm')
ty1 = mlines.Line2D([], [], color=ty1col, marker=marker, linestyle='None',
                          markersize=10, label='Category 1 Typhoon')
ty2 = mlines.Line2D([], [], color=ty2col, marker=marker, linestyle='None',
                          markersize=10, label='Category 2 Typhoon')
ty3 = mlines.Line2D([], [], color=ty3col, marker=marker, linestyle='None',
                          markersize=10, label='Category 3 Typhoon')
ty4 = mlines.Line2D([], [], color=ty4col, marker=marker, linestyle='None',
                          markersize=10, label='Category 4 Typhoon / SuperTyphoon')
ty5 = mlines.Line2D([], [], color=ty5col, marker=marker, linestyle='None',
                          markersize=10, label='Category 5 SuperTyphoon')
                          
                          
plt.legend(handles=[lpa, td, ts, ty1, ty2, ty3, ty4, ty5], fontsize=10, facecolor='wheat', loc='best')

filelist=['data/trackfile-16W.txt', 'data/trackfile-18W.txt']


with open('data/trackfile-16W.txt') as f:
    # List to store selected columns from txt file:
    id = [] # TC designation
    lat = [] # latitude
    lon = [] # longitude
    wnd = [] # winds in knots
    
    for line in f:
        if not line.strip() or line.startswith('@') or line.startswith('#'): 
            continue
        row = line.split()
        id.append((row[0]))
        lat.append(float(row[5][:-1])) # remove last character from coords and add to list
        lon.append(float(row[4][:-1]))
        wnd.append(float(row[7]))
    
        
    # Function to map the colors as a list from the input list of x variables
    def pltcolor(lst):
        cols=[]
        mrks=[]
        for l in lst:
            if l < 25:
                cols.append(lpacol)
            elif l in range(25, 35):
                cols.append(tdcol)
            elif l in range(35, 65):
                cols.append(tscol)
            elif l in range(65, 85):
                cols.append(ty1col)
            elif l in range(85, 100):
                cols.append(ty2col)
            elif l in range(100, 115):
                cols.append(ty3col)
            elif l in range(115, 140):
                cols.append(ty4col)
            else:
                cols.append(ty5col)

        return cols
        
    # Create the colors list using the function above
    cols=pltcolor(wnd)
	
    plt.scatter(lat, lon, c=cols, s=markersize, transform=ccrs.PlateCarree(), zorder=2)
    
	# Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lat)[idx],np.array(lon)[idx], color='red', linewidth=0.5, zorder=1)

plt.figtext(0.99, 0.01, 'Track and intensity data from JTWC | Plotted by Imran Mahmood', fontsize=8, horizontalalignment='right')
plt.tight_layout()
plt.show()