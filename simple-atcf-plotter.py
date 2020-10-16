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
from matplotlib.font_manager import FontProperties

#plt.rcParams['axes.facecolor'] = '#0e1111'
print('a.)NW Pacific \nb.)N Indian Ocean')
basin = input('Select a basin: ')

if basin == 'A' or basin == 'a':
    limits = [98.0, 152.0, -0.5, 46.0] # minlon, maxlon, minlat, maxlat
elif basin == 'B' or basin == 'b':
    limits = [38.0, 102.0, -0.5, 32.0]
	
fig = plt.figure(figsize=(12.80,7.20)) #WxH 1280x720
#fig,ax = plt.subplots()

ax = plt.axes(projection=ccrs.PlateCarree())

plt.title('Title')


ax.set_extent(limits)

resol = '10m'
land = cfeature.NaturalEarthFeature('physical', 'land', \
    scale=resol, edgecolor='darkgreen', facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature('physical', 'ocean', \
    scale=resol, edgecolor='none', facecolor='lightseagreen')
lakes = cfeature.NaturalEarthFeature('physical', 'lakes', \
    scale=resol, edgecolor=cfeature.COLORS['water'], facecolor=cfeature.COLORS['water'])
rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
    scale=resol, edgecolor=cfeature.COLORS['water'], facecolor='none')

ax.add_feature(land, facecolor='forestgreen', lw=0.5, zorder=0)
ax.add_feature(ocean, zorder=-1)
ax.add_feature(lakes)
ax.add_feature(rivers, lw=0.5)
ax.add_feature(cfeature.BORDERS, color='darkgreen', lw=0.8)

gl = ax.gridlines(draw_labels=True, lw=1, color='gray', alpha=0.5, linestyle=':')
gl.top_labels = False
gl.right_labels = False

# Draw PAR line
if basin == 'A' or basin == 'a':
	x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
	y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
	plt.plot(x_values, y_values, lw=0.8, zorder=1, color='red')
	plt.text(125.0, 4.0, 'PHL Area of Responsibility', fontsize=8, color='red')

markersize=25
marker='o'
lpacol='gray'
tdcol='deepskyblue'
tscol='royalblue'
ty1col='khaki'
ty2col='yellow'
ty3col='orange'
ty4col='orangered'
ty5col='darkred'
ptoutl='lightgray'

fontP = FontProperties()
fontP.set_size('small')

# Plot legends
lpa = mlines.Line2D([], [], color=lpacol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Invest / Low Pressure Area')
td = mlines.Line2D([], [], color=tdcol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='(Sub)Tropical Depression')
ts = mlines.Line2D([], [], color=tscol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='(Sub)Tropical Storm')
#ty = mlines.Line2D(label='Typhoon:')
ty1 = mlines.Line2D([], [], color=ty1col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 1 Typhoon')
ty2 = mlines.Line2D([], [], color=ty2col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 2 Typhoon')
ty3 = mlines.Line2D([], [], color=ty3col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 3 Typhoon')
ty4 = mlines.Line2D([], [], color=ty4col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 4 Typhoon / SuperTyphoon')
ty5 = mlines.Line2D([], [], color=ty5col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 5 SuperTyphoon')
                          
plt.legend(handles=[lpa, td, ts, ty1, ty2, ty3, ty4, ty5], facecolor='burlywood', loc='upper left', prop=fontP)

filenames=['data/trackfile-16W.txt', 'data/trackfile-18W.txt']

#with ExitStack() as stack:
#    files = [stack.enter_context(open(fname)) for fname in filenames]
with open('data/trackfile-16W.txt') as f:
    # List to store selected columns from txt file:
    id = [] # system designation
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
    
    plt.scatter(lat, lon, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=2)
    
    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lat)[idx],np.array(lon)[idx], antialiased=True, snap=True, lw=0.5, color='black', zorder=1)
            #ln.set_antialiased(True)
plt.figtext(0.99, 0.01, 'Track and intensity data from JTWC', fontsize=8, horizontalalignment='right')
plt.tight_layout(rect=[2, 0.05, 0, 0])
#plt.tight_layout()
plt.show()
#fig.savefig('myimage.png', format='png', dpi=1200)