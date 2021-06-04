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
from matplotlib.transforms import offset_copy
import cartopy.io.img_tiles as cimgt


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
    print('a)NW Pacific \nb)NW Pacific (PAR) \nc)N Indian Ocean \nd)Single Storm Plot\ne)Global')
    basin = input('Select area: ')
    
    if basin == 'A' or basin == 'a':
        plot_nwpac()
    elif basin == 'B' or basin == 'b':
        plot_nwpac_par()
    elif basin == 'C' or basin == 'c':
        plot_nio()
    elif basin  == 'D' or basin == 'd':
        plot_single()
    elif basin  == 'E' or basin == 'e':
        plot_global()
        

def create_map(coordlist):
    plt.rcParams["figure.facecolor"] = 'whitesmoke'
    #fig = plt.figure(figsize=(11, 6.5)) #WxH 1100x650
    
    global fig, ax
    fig, ax = plt.subplots(figsize=(11, 6.5))
    resol = '10m'
    
    mapstyle = input('Use stamen terrain? (Y/N): ')
    if mapstyle == 'Y' or mapstyle == 'y':
        stamen_terrain = cimgt.Stamen('terrain-background')
        ax = plt.axes(projection=stamen_terrain.crs)
        ax.add_image(stamen_terrain, 7) #zoom level
    else:
        ax = plt.axes(projection=ccrs.PlateCarree())
        land = cfeature.NaturalEarthFeature('physical', 'land', \
            scale=resol, edgecolor='darkgreen', facecolor=cfeature.COLORS['land'])
        ax.add_feature(land, facecolor='olivedrab', edgecolor='darkgreen', zorder=1, alpha=0.8)
    
    ax.set_extent(coordlist, crs=ccrs.Geodetic())
    ax.autoscale(False)

    ocean = cfeature.NaturalEarthFeature('physical', 'ocean', \
        scale=resol, edgecolor='none', facecolor='powderblue')
    lakes = cfeature.NaturalEarthFeature('physical', 'lakes', \
        scale=resol, edgecolor=cfeature.COLORS['water'], facecolor=cfeature.COLORS['water'])
    rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
        scale=resol, edgecolor=cfeature.COLORS['water'], facecolor='none')
    
    ax.add_feature(ocean)
    ax.add_feature(lakes)
    ax.add_feature(rivers, lw=0.5)
    ax.add_feature(cfeature.BORDERS, color='darkgreen', lw=0.8)
    ax.add_feature(cfeature.COASTLINE, color='darkgreen', lw=0.5)

    gl = ax.gridlines(draw_labels=True, lw=1, color='gray', alpha=0.5, linestyle=':')
    gl.top_labels = False
    gl.right_labels = False
    gl.n_steps=10
        
    
def read_atcf_file(fileloc):
    #filenames=['data/trackfile-16W.txt', 'data/2021-NWP.txt']

    #with ExitStack() as stack:
    #    files = [stack.enter_context(open(fname)) for fname in filenames]
    with open(fileloc) as f:
        # List to store selected columns from txt file:
        global id
        global name
        global date
        global time
        global lat
        global lat2
        global lon
        global wnd
        global indvSystems
        id = [] # system designation
        name = [] # system name
        date = [] # date UTC
        time = [] # time UTC
        lat = [] # latitude / y-axis
        lat2 = []
        lon = [] # longitude / x-axis
        wnd = [] # winds in knots
        
        for line in f:
            if not line.strip() or line.startswith('@') or line.startswith('#'): 
                continue
            row = line.split()
            id.append(str(row[0]))
            name.append(str(row[1]))
            date.append(str(row[2]))
            time.append(str(row[3]))
            #if row[5][-1] == 'S':
                #print ('south')
            #    lat.append(float(row[5][:-1]))
            #    lat.append([s + '-' for s in mylist])
                
            lat.append(row[4]) # remove last character from coords and add to list
            lon.append(float(row[5][:-1]))
            wnd.append(int(row[7]))
        
        # if/else in list comprehension : check if NHem or SHem
        [lat2.append(float('-'+y[:-1])) if y[-1] == 'S' else lat2.append(float(y[:-1])) for y in lat]
        
        id2 = [item + ' ' for item in id]
        cmbnd = [i + j for i, j in zip(id2, name)]
        indvSystems = set(cmbnd)


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
    create_map([98.0, 180.0, -0.5, 40.0])
    
    # Draw PAR line
    x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
    y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
    plt.plot(x_values, y_values, lw=0.8, zorder=2, color='red', ls='--', transform=ccrs.PlateCarree())
    plt.text(125.0, 4.0, 'PHL Area of Responsibility', fontsize=8, color='red', transform=ccrs.PlateCarree())
    
    read_atcf_file('data/2021-NWP.txt')

    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lon, lat2, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=3)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lon)[idx], np.array(lat2)[idx], lw=0.5, antialiased=True, transform=ccrs.PlateCarree(), color='black', zorder=2)
   
    # place a text box in upper  in right axes coords
    ax.text(1, 1, 'In plot:\n' + '\n'.join(sorted(indvSystems)), transform=ax.transAxes, fontsize=8, verticalalignment='top')
    
    plt.title('2021 Northwest Pacific Tropical Cyclone Tracks')



def plot_nwpac_par():
    create_map([114.0, 136.0, 4.0, 26.0])
    
    # Draw PAR line
    x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
    y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
    plt.plot(x_values, y_values, lw=0.8, zorder=2, color='red', ls='--', transform=ccrs.PlateCarree())
    plt.text(125.0, 4.5, 'Philippine Area of Responsibility', fontsize=8, color='red', transform=ccrs.PlateCarree())
    
    read_atcf_file('data/2021-NWP.txt')
    
    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lon, lat2, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=3)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lon)[idx], np.array(lat2)[idx], lw=0.5, antialiased=True, color='black', transform=ccrs.PlateCarree(), zorder=2)
    
    plt.title('2021 Northwest Pacific Tropical Cyclone Tracks (Philippine Area of Responsibility)')


def plot_nio():
    create_map([38.0, 102.0, -0.5, 32.0])
    
    read_atcf_file('data/1998vsTauktae.txt')

    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lon, lat2, c=cols, edgecolors=ptoutl, s=markersize, transform=ccrs.PlateCarree(), zorder=3)

    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lon)[idx], np.array(lat2)[idx], lw=0.5, antialiased=True, transform=ccrs.Geodetic(), color='black', zorder=2)
    
    # place a text box in upper  in right axes coords
    ax.text(1, 1, 'In plot:\n' + '\n'.join(sorted(indvSystems)), transform=ax.transAxes, fontsize=8, verticalalignment='top')
    
    plt.title('Observed Tracks of Cyclone 03A (1998) and Cyclone Tauktae (2021)')

 
def plot_single():
    read_atcf_file('data/02W-Surigae-2021.txt')
    
    minlat = min(lat2)-2
    maxlat = max(lat2)+2
    minlon = min(lon)-2
    maxlon = max(lon)+2
    
    create_map([minlon, maxlon, minlat, maxlat])
    
    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lon, lat2, c=cols, edgecolors=ptoutl, s=180, transform=ccrs.PlateCarree(), zorder=3)
    plt.plot(lon, lat2, lw=0.8, antialiased=True, color='black', transform=ccrs.PlateCarree(), zorder=2)
        
    for i, txt in enumerate(wnd):
        ax.annotate(str(txt), (lon[i], lat2[i]), transform=ccrs.PlateCarree(), fontsize=5.5, weight='heavy', color='black', horizontalalignment='center', verticalalignment='center', zorder=3)
        #texts.append(ax.text(lablat[i], lon[i], txt))
        #ax.text(1, 1, 'Intensity History:\n' + '\n'.join(sorted(str(txt))), transform=ax.transAxes, fontsize=8, verticalalignment='top')   
    plt.title(str(*indvSystems) + ' Observed Track and Intensity (1-minute Sustained Winds in Knots)\n'
    + date[-1] +' ' + time[-1] + ' - ' + date[0] + ' ' + time[0] + ' UTC')

def plot_global():
    read_atcf_file('data/2020-Global.txt')
    
    plt.rcParams["figure.facecolor"] = 'whitesmoke'
    fig = plt.figure(figsize=(10, 8), constrained_layout=True) #WxH 1100x650
    
    ax = plt.axes(projection=ccrs.Robinson())
    ax.set_global()
    
    ax.stock_img()
    ax.coastlines()

    resol = '50m'
    land = cfeature.NaturalEarthFeature('physical', 'land', \
        scale=resol, edgecolor='darkgreen', facecolor=cfeature.COLORS['land'])
    ocean = cfeature.NaturalEarthFeature('physical', 'ocean', \
        scale=resol, edgecolor='none', facecolor='powderblue')
    lakes = cfeature.NaturalEarthFeature('physical', 'lakes', \
        scale=resol, edgecolor=cfeature.COLORS['water'], facecolor=cfeature.COLORS['water'])
    rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
        scale=resol, edgecolor=cfeature.COLORS['water'], facecolor='none')

    #ax.add_feature(land, facecolor='olivedrab', lw=0.5, zorder=0)
    ax.add_feature(ocean)
    ax.add_feature(lakes)
    ax.add_feature(rivers, lw=0.5)
    ax.add_feature(cfeature.BORDERS, color='darkgreen', lw=0.8)

    gl = ax.gridlines(draw_labels=False, lw=1, color='gray', alpha=0.5, linestyle=':')
    #gl.top_labels = False
    #gl.right_labels = False
    #gl.n_steps=10
    
    # Create the colors list using the function above
    cols = pltcolor(wnd)

    plt.scatter(lon, lat2, c=cols, edgecolors=ptoutl, s=10, transform=ccrs.PlateCarree(), zorder=4)
    # Connect points with same TC id only
    uid = np.array(id)
    for yv in uid:
        if yv != np.nan:
            idx = uid == yv
            plt.plot(np.array(lon)[idx], np.array(lat2)[idx], lw=0.5, antialiased=True, color='black', zorder=3)
    
    
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
                          
plt.legend(handles=[lpa, td, ts, classif, c1, c2, c3, c4, c5], facecolor='antiquewhite', loc='upper left', prop=fontP)

plt.autoscale(False)

plt.figtext(0.99, 0.01, 'Track and intensity data from JTWC | Plotted by Imran Mahmood', fontsize=8, horizontalalignment='right')
#plt.figtext(0.5, 0.01, 'Track and intensity data from JTWC', fontsize=8, ha='center')
#plt.tight_layout(rect=[2, 0.05, 0, 0])
#fig.tight_layout()
plt.tight_layout()
plt.show()
#fig.savefig('myimage2.png', format='png', bbox_inches='tight', pad_inches=0)
