# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:00:41 2018

@author: zilishen

So when you want to create a plot for a new galaxy, there are 3 main
things you need to change. You need to change both paths to the file to 
the appropriate galaxy and you need to change the title of the plot when you
are ready to save it. 
The last possible change you need to make is to change the x limit on the 
limited plots if you exclude different things. If you exclude different
things you will also need to change the list length for the limited plots.

"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

galname = ('Preliminary Star Formation History of UGC1281')
data = np.genfromtxt('/Users/zilishen/core-cusp/10210_UGC1281/out_v5.final', skip_header = 1, unpack = True)

### Create plot object
fig = plt.figure(figsize=(12, 8))
outer = gridspec.GridSpec(1, 1, wspace=0.15, hspace=0.2)

### Plot title and axis labels
bigtitle = (galname)
sidetitle = ('Star Formation Rate (10$^{-3}$ M$_{\odot}$ yr$^{-1}$)')

fig.text(.49, .96, bigtitle, fontsize = 20, horizontalalignment = 'center')
fig.text(.07, .75, sidetitle, fontsize = 18, rotation = 90)

ax_list=[]
for i in range(1):
    inner = gridspec.GridSpecFromSubplotSpec(1, 2,
                    subplot_spec=outer[i], wspace=0.08, hspace=0.1)
    ax_list.append([])

    for j in range(2):
        ax = plt.Subplot(fig, inner[j])
        ax_list[i].append(ax)
        fig.add_subplot(ax)
        
### Define lifetime plot and recent SFH plot
lt_plot = ax_list[0][0]
rc_plot = ax_list[0][1]

### Log space time bins
t_begin = np.array(data[0])
t_end = np.array(data[1])
t_width = t_end - t_begin
t_mid = t_begin + 0.5*t_width

### Linear time bins
lin_t_begin = 10.**t_begin
lin_t_end = 10.**t_end

Gyr_t_begin = lin_t_begin / 1.0e9
Gyr_t_end = lin_t_end / 1.0e9
Gyr_t_width = Gyr_t_end - Gyr_t_begin
Gyr_t_mid = Gyr_t_begin + 0.5*Gyr_t_width

### Get sfr and make life time plot
sfr_msun = np.array(data[3])
sfr = sfr_msun * 1.0e3
err_up = np.array(data[4]* 1.0e3)
err_dn = np.array(data[5]* 1.0e3)

### This is rgb values for the color
poster_red = [0.765625,0.08984375,0.18359]

lt_plot.bar(Gyr_t_begin, sfr, width=Gyr_t_width, color=poster_red, alpha=0.6)
lt_plot.errorbar(Gyr_t_mid, sfr, yerr = [data[5]*10**3, data[4]*10**3], fmt = ' ', color = 'k')
lt_plot.set_xlim(0, 14.15)
lt_plot.invert_xaxis()
lt_plot.set_xlabel('Age (Gyr)',fontsize=18)
lt_plot.tick_params(axis='both', which='major', labelsize=14)

### Calculate avg sfr and starburst sfr, avg chopped at 6Gyr
chopped_t_end = np.array([np.minimum(6.0, t) for t in Gyr_t_end])
chopped_t_width = chopped_t_end - Gyr_t_begin
avg_sfr = np.average(sfr,weights=chopped_t_width)
#avg_sfr = np.average(sfr,weights=Gyr_t_width) ### this is life time avg 
#avg_sfr = np.average(sfr[:-1],weights=Gyr_t_width[:-1]) #avg excluding oldest time bin
burst_sfr = 2.0 * avg_sfr

### Recent SFH plot
rc_plot.bar(Gyr_t_begin[:-2],sfr[:-2],width=Gyr_t_width[:-2],color=poster_red, alpha=0.6)
rc_plot.errorbar(Gyr_t_mid[:-2], sfr[:-2], yerr = [data[5][:-2]*10**3, data[4][:-2]*10**3], fmt = ' ', color = 'k')
rc_plot.set_xlim(0.0001, 1)
rc_plot.set_xlabel('Age (Gyr)',fontsize=18)
rc_plot.tick_params(axis='both', which='major', labelsize=14)

rc_plot.hlines(avg_sfr, xmin = 0, xmax = 1.6, linestyles = '--', color = 'k')
rc_plot.hlines(burst_sfr, xmin = 0, xmax = 1.6, linestyles = '--', color = 'k')
ylow, yhigh = rc_plot.get_ylim()
ylen = yhigh - ylow
rc_plot.text(0.98, avg_sfr+.02*ylen, "$\langle$SFR$\\rangle$$_{0-6\ Gyr}$", fontsize=18)
rc_plot.text(0.98, burst_sfr+.01*ylen, " b = 2", fontsize=18)

rc_plot.invert_xaxis()
rc_plot.axes.get_yaxis().set_ticklabels([])