# A simple script to plot storm tracks

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
#ax.coastlines(resolution='10m')
# Put a background image on for nice sea rendering.
#ax.stock_img()

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle=':')
gl.top_labels = False
gl.right_labels = False

# Draw PAR line
x_values = [120.0, 135.0, 135.0, 115.0, 115.0, 120.0, 120.0]
y_values = [25.0, 25.0, 5.0, 5.0, 15.0, 21.0, 25.0]
plt.plot(x_values, y_values, linewidth=1)
plt.text(120.0, 4.5, 'PHL Area of Responsibility', fontsize=8);

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
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

#16W Chan-hom
plt.text(142.8, 19.3, ' Chan-hom', fontsize=10, transform=ccrs.Geodetic());
plt.plot(142.8, 19.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(142.3, 19.6,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(141.8, 20.0,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(141.4, 20.3,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(141.0, 20.7,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(140.5, 20.9,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(140.1, 21.6,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(139.9, 22.0,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(139.8, 22.1,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(139.6, 22.2,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(139.5, 22.2,  markersize=markersize, marker='o', color=lpacol, transform=ccrs.Geodetic())
plt.plot(139.3, 22.3,  markersize=markersize, marker='o', color=tdcol, transform=ccrs.Geodetic())
plt.plot(139.2, 22.4,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(139.3, 22.6,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
plt.plot(139.4, 23.2,  markersize=markersize, marker='o', color=tscol, transform=ccrs.Geodetic())
#--active

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