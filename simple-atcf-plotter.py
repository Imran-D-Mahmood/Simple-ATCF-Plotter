# A simple script to plot storm track data from ATCF.
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
from matplotlib.collections import LineCollection

plt.rcParams["figure.facecolor"] = 'whitesmoke'
fig = plt.figure(figsize=(10, 7), constrained_layout=True) #WxH 1280x720

ax = plt.axes(projection=ccrs.PlateCarree())

resol = '10m'
land = cfeature.NaturalEarthFeature('physical', 'land', \
    scale=resol, edgecolor='darkgreen', facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature('physical', 'ocean', \
    scale=resol, edgecolor='none', facecolor='powderblue')
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

markersize=28
marker='o'
lpacol='gray'
tdcol='royalblue'
tscol='deepskyblue'
ty1col='khaki'
ty2col='yellow'
ty3col='orange'
ty4col='orangered'
ty5col='deeppink'
ptoutl='black'

def show_selection():
    print('a)NW Pacific \nb)NW Pacific (PAR) \nc)N Indian Ocean \nd)Single Storm Plot')
    basin = input('Select area: ')
    
    if basin == 'A' or basin == 'a':
        plot_nwpac()
    elif basin == 'B' or basin == 'b':
        plot_nwpac_par()
    elif basin == 'C' or basin == 'c':
        plot_nio()
    elif basin  == 'D' or basin == 'd':
        plot_single()
        
    
def read_atcf_file(fileloc):
    #filenames=['data/trackfile-16W.txt', 'data/2020-NWP-TC-Tracks.txt']

    #with ExitStack() as stack:
    #    files = [stack.enter_context(open(fname)) for fname in filenames]
    with open(fileloc) as f:
        # List to store selected columns from txt file:
        global id
        global name
        global date
        global time
        global lat
        global lon
        global wnd
        id = [] # system designation
        name = [] # system name
        date = []
        time = []
        lat = [] # latitude
        lon = [] # longitude
        wnd = [] # winds in knots
        
        for line in f:
            if not line.strip() or line.startswith('@') or line.startswith('#'): 
                continue
            row = line.split()
            id.append((row[0]))
            name.append(str(row[1]))
            date.append(str(row[2]))
            time.append(str(row[3]))
            lat.append(float(row[5][:-1])) # remove last character from coords and add to list
            lon.append(float(row[4][:-1]))
            wnd.append(int(row[7]))

# Function to map the colors as a list from the input list of x variables
def pltcolor(lst):
    cols=[]
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

def plot_nwpac():
    ax.set_extent([98.0, 180.0, -0.5, 40.0])
    
    # Draw PAR line
    x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
    y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
    plt.plot(x_values, y_values, lw=0.8, zorder=1, color='red', ls='--')
    plt.text(125.0, 4.0, 'PHL Area of Responsibility', fontsize=8, color='red')
    
    read_atcf_file('data/trackfile-16W.txt')

    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lat, lon, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=2)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lat)[idx], np.array(lon)[idx], lw=0.5, antialiased=True, color='black', zorder=1)
    
    #plt.text(144.4, 11.2, ' GONI', fontsize=8)

    #plt.text(153.0, 5.0, ' ATSANI', fontsize=8)
    plt.title('Northwest Pacific Tropical Cyclone Tracks')
    
    pass

def plot_nwpac_par():
    ax.set_extent([114.0, 136.0, 4.0, 26.0])
    
    # Draw PAR line
    x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
    y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
    plt.plot(x_values, y_values, lw=0.8, zorder=1, color='red', ls='--')
    plt.text(125.0, 4.5, 'Philippine Area of Responsibility', fontsize=8, color='red')
	
    read_atcf_file('data/trackfile-16W.txt')
    
    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lat, lon, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=2)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lat)[idx], np.array(lon)[idx], lw=0.5, antialiased=True, color='black', zorder=1)
    
    plt.title('Tropical Cyclone Tracks within the Philippine Area of Responsibility')

def plot_nio():
    ax.set_extent([38.0, 102.0, -0.5, 32.0])
    
    read_atcf_file('data/2020-NIO-TC-Tracks.txt')

    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lat, lon, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=2)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lat)[idx], np.array(lon)[idx], lw=0.5, antialiased=True, color='black', zorder=1)
    
    plt.title('North Indian Ocean Tropical Cyclone Tracks')
	
def plot_single():
    read_atcf_file('data/22W-Goni.txt')
    
    minlat = min(lat)-5
    maxlat = max(lat)+5
    minlon = min(lon)-5
    maxlon = max(lon)+5
    
    ax.set_extent([minlat, maxlat, minlon, maxlon])
    
    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lat, lon, c=cols, edgecolors=ptoutl, s=40, transform=ccrs.PlateCarree(), zorder=2)
    plt.plot(lat, lon, lw=0.8, antialiased=True, color='black', zorder=1)
    
    #lablat = [2+f for f in lat]
    texts = []
    
    for i, txt in enumerate(wnd):
        ax.annotate(str(txt), (lat[i], lon[i]), xytext=(5,5), textcoords='offset points', fontsize=8)
        #texts.append(ax.text(lablat[i], lon[i], txt))
    
    plt.title(str(id[0]) + ' ' + name[0] + ' Observed Track and Intensity (1-minute Sustained Winds in Knots)\n'
    + date[-1] +' ' + time[-1] + ' - ' + date[0] + ' ' + time[0] + ' UTC')


show_selection()


fontP = FontProperties()
fontP.set_size('small')

# Plot legends
lpa = mlines.Line2D([], [], color=lpacol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Invest / Low Pressure Area')
td = mlines.Line2D([], [], color=tdcol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='(Sub)Tropical Depression')
ts = mlines.Line2D([], [], color=tscol, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='(Sub)Tropical Storm')
classif = mlines.Line2D([], [], color=None, marker=None, linestyle='None', label='Typhoon/Hurricane/Cyclone:')
c1 = mlines.Line2D([], [], color=ty1col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 1')
c2 = mlines.Line2D([], [], color=ty2col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 2')
c3 = mlines.Line2D([], [], color=ty3col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 3')
c4 = mlines.Line2D([], [], color=ty4col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 4')
c5 = mlines.Line2D([], [], color=ty5col, markeredgecolor=ptoutl, marker=marker, linestyle='None',
                          markersize=10, label='Category 5')
                          
plt.legend(handles=[lpa, td, ts, classif, c1, c2, c3, c4, c5], facecolor='burlywood', loc='upper left', prop=fontP)

plt.autoscale(False)

plt.figtext(0.99, 0.01, 'Track and intensity data from JTWC | Plotted by Imran Mahmood', fontsize=8, horizontalalignment='right')
#plt.figtext(0.5, 0.01, 'Track and intensity data from JTWC', fontsize=8, ha='center')
#plt.tight_layout(rect=[2, 0.05, 0, 0])
#plt.tight_layout()
plt.show()
#fig.savefig('myimage.png', format='png', dpi=1200)