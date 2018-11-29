# create growth curve from pickled data of % cell coverage

import pickle, os
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import matplotlib
import numpy as np
import bfanalysis as cvr

# import pickled % coverage data 
#direct = '/mnt/cluster-victor/lin_motors/pics/raster/20181024_growth1/'
direct = '/mnt/cluster-victor/lin_motors/pics/raster/20180816_growth2/'

frac_array = [] # a list of a numpy array (vector) of % coverage per image, per timepoint
counts_array = [] # a list of a numpy array (vector) of spot sizes of collected imgs, per timepoint
names = []
files = os.listdir(direct)
files.sort()
for f in files:
    if f.find('.pickle') != -1:
        frac_list, counts_list2 = pickle.load(open(direct + f, 'rb'))
        frac_array.append(frac_list)
        counts_array.append(counts_list2)
        names.append(f)
print names # to know what order is the listed arrays are in 

# create array of mean, stds: have to manually find the correct timepoint order
coverage2 = np.array(frac_array)
means = [np.mean(coverage2[0]), np.mean(coverage2[3]), np.mean(coverage2[4]), np.mean(coverage2[1]), np.mean(coverage2[2])]
#means = [np.mean(coverage2[0]), np.mean(coverage2[2]), np.mean(coverage2[3]), np.mean(coverage2[4]), np.mean(coverage2[5]), np.mean(coverage2[1])]
stds = [np.std(coverage2[0]), np.std(coverage2[3]), np.std(coverage2[4]), np.std(coverage2[1]), np.std(coverage2[2])]
#stds = [np.std(coverage2[0]), np.std(coverage2[2]), np.std(coverage2[3]), np.std(coverage2[4]), np.std(coverage2[5]), np.std(coverage2[1])]

print means
print stds
bins = 50
converter = 10**6 # convert from um to mm
# % cell coverage distrubtion of 0, 5, 8, 12, 15, 25
#fig = plt.figure()
#ax = plt.add_subplot(111)
fig, ((ax01, ax02), (ax11, ax12), (ax21, ax22), (ax31, ax32), (ax41, ax42), (ax51, ax52)) = plt.subplots(nrows=6, ncols=2) # create subplots
fig.figsize = [12, 2]
matplotlib.rc('font', size=6.5)
fontsize = 10
fig.set_tight_layout(True)

def create_subplotpair(ax1, ax2, ax1_data, ax2_data, bins=100, ax1_ylabel='', ax1_title='', ax2_ylabel='', ax2_title=''):
    # ax1 is left subplot, ax2 is right subplot: for size distribution, and coverage distribution
    ax1.hist(ax1_data, bins)
    ax1.set_ylabel(ax1_ylabel)
    ax1.set_title(ax1_title)
    ax2.hist(ax2_data, bins)
    ax2.set_title(ax2_title)

axs_titles = ['0 h', '5 h', '8 h', '12 h', '15 h', '25 h']
ordered_timepoints = [0, 3, 4, 1, 2, 5]
axes = ((ax01, ax02), (ax11, ax12), (ax21, ax22), (ax31, ax32), (ax41, ax42), (ax51, ax52))
counts_array = np.array(counts_array) / converter

for i in range(len(axs_titles)):
    j = ordered_timepoints[i]
    create_subplotpair(axes[i][0], axes[i][1], counts_array[j], frac_array[j]), bins, ax1_ylabel=axs_titles[j], ax1_title='mean colony size: %.2e $\mu$m$^2$' %(np.mean(counts_array[j])), ax2_title='mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(frac_array[j], stds[i])))

# coverage and colony size distribution for each timepoint
ax01.hist(np.array(counts_array[0])/converter, bins)
ax01.set_ylabel('0 h')
ax01.set_title('mean colony size: %.2e $\mu$m$^2$' %np.mean(np.array(counts_array[0])/converter))
ax02.hist(frac_array[0], bins)
ax02.set_title('mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(np.array(frac_array[0])), stds[0]))
#ax.set_xlabel('% cell coverage')
#ax.set_ylabel('counts')
#ax1 = fig.add_subplot(411)
ax11.hist(np.array(counts_array[3])/converter, bins)
ax11.set_ylabel('4.5 h', fontsize=fontsize)
ax11.set_title('%.2f $\mu$m$^2$' %np.mean(np.array(counts_array[3])))
ax12.hist(frac_array[3], bins)
ax12.set_title('mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(np.array(frac_array[3])), stds[1]))
#ax2 = fig.add_subplot(412)
ax21.hist(np.array(counts_array[4])/converter, bins)
ax21.set_ylabel('8 h', fontsize=fontsize)
ax21.set_title('%.2f $\mu$m$^2$' %np.mean(np.array(counts_array[4])))
ax22.hist(frac_array[4], bins)
ax22.set_title('mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(np.array(frac_array[4])), stds[2]))
#ax3 = fig.add_subplot(413)
ax31.hist(np.array(counts_array[1])/converter, bins)
ax31.set_ylabel('12 h', fontsize=fontsize)
ax31.set_title('%.2f $\mu$m$^2$' %np.mean(np.array(counts_array[1])))
ax32.hist(frac_array[1], bins)
ax32.set_title('mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(np.array(frac_array[1])), stds[3]))
#ax4 = fig.add_subplot(414)
ax41.hist(np.array(counts_array[2])/converter, bins)
ax41.set_ylabel('24 h', fontsize=fontsize)
ax41.set_title('%.2f $\mu$m$^2$' %np.mean(np.array(counts_array[2])))
ax42.hist(frac_array[2], bins)
ax42.set_title('mean coverage: %.2f $\pm$ %.2f%%' %(np.mean(np.array(frac_array[2])), stds[4]))

ax41.set_xlabel('colony size / mm$^2$', fontsize=8)
ax42.set_xlabel('% cell coverage', fontsize=8)
axes = [ax01, ax02, ax11, ax12, ax21, ax22, ax31, ax32, ax41, ax42]
for ax in axes:
    pass

axes1 = [ax01, ax11, ax21, ax31, ax41]
for ax in axes1:
    ax.set_xlim([0, 0.30])
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.set_yscale('log')

axes2 = [ax02, ax12, ax22, ax32, ax42]
for ax in axes2:
    ax.set_xlim([0,90])
    ax.tick_params(axis='both', which='major', labelsize=8)
#plt.savefig('/mnt/cluster-victor/growth2/distribution.png', dpi=600)

duration2 = [0.0, 4.5, 8, 12, 24]
coverage1 = [[4.37, 4.37, 4.37],
        [3.91, 3.29, 4.67], 
        [17.11, 15.29, 11.99],
        [13.87, 14.94, 18.52],
        [13.02, 25.25, 21.80]]
coverage1 = np.array(coverage1)


# OD600 data
duration = [0, 2.5, 4.5, 6, 8, 12, 24]
od600_lab = [[0.0411, 0.0446, 0.0372],
        [0.0433, 0.0585, 0.0667],
        [0.10366, 0.111, 0.125],
        [0.230, 0.222, 0.241],
        [0.528, 0.530, 0.534],
        [0.596, 0.564, 0.541],
        [0.832, 0.869, 0.888]]
od600_com = [[0, 0.01, 0],
        [0, 0.01, 0.01],
        [0.10, 0.10, 0.10],
        [0.30, 0.30, 0.30],
        [0.43, 0.43, 0.42],
        [0.50, 0.50, 0.50],
        [0.75, 0.75, 0.76]]
od600_lab = np.array(od600_lab)
od600_com = np.array(od600_com)

###
# plot an example threshold
#fig = plt.figure(figsize=[7, 4])
fig = plt.figure(figsize=[3.5, 4])
matplotlib.rc('font', size=6, weight='bold')
fig.set_tight_layout(True)

#ax3 = fig.add_subplot(121)
ax3 = fig.add_subplot(111)
img = mpimg.imread('/mnt/cluster-victor/growth2/bw2.png')
ax3.imshow(img, cmap='gray')
ax3.set_xlabel('distance / $\mu$m', weight='bold') # .20 mm at 1219 px
ax3.set_ylabel('distance / $\mu$m', weight='bold') # .20 mm at 1219 px
ax3.set_xticks([0, 305, 610, 914, 1219]) # .20 mm at 1219 px
ax3.set_xticklabels([0, 50, 100, 150, 200])
ax3.set_yticks([64, 384, 704, 1024]) # .15 mm at 960 px
ax3.set_yticklabels([150, 100, 50, 0])
#plt.savefig('/mnt/cluster-victor/growth2/bf1.png', dpi=600)
###

# plot example distribution of all three trials
fig = plt.figure(figsize=[3.5, 4])
matplotlib.rc('font', size=6, weight='bold')
fig.set_tight_layout(True)
#ax4 = fig.add_subplot(224)
ax4 = fig.add_subplot(211)
#ax4.hist(frac_array[-1], bins=100, color='dimgray')
counts_plot = np.array(counts_array[2]) / 10**6
ax4.hist(counts_plot, bins=100, color='dimgray')
ax4.set_xlim([0, 0.23])
#ax4.set_ylim([0, 10000])
ax4.set_yscale('log')
#ax4.set_xlabel('colony size / $\mu$m^2', weight='bold')
ax4.set_xlabel('colony size / mm$^2$', weight='bold')
ax4.set_ylabel('counts', weight='bold')

# plot OD600 curve with cell coverage
#ax1 = fig.add_subplot(222)
#ax1 = fig.add_subplot(212)
fig = plt.figure(figsize=[3.5, 2])
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.errorbar(duration, od600_lab.mean(axis=1), yerr=od600_lab.std(axis=1), color='blue', fmt='o', mfc='white', linestyle='dashed', label='OD$_{600}$', markersize=6, linewidth=2, elinewidth=2, capsize=5)
#ax1.errorbar(duration, od600_com.mean(axis=1), yerr=od600_com.std(axis=1), color='cyan', fmt='o', mfc='white', linestyle='dashed', label='OD600 - com', markersize=6, linewidth=2, elinewidth=2, capsize=5)
#ax2.errorbar(duration2, coverage2.mean(axis=1), yerr=coverage1.std(axis=1), color='red', fmt='o', mfc='white', linestyle='dashed', label='% cell coverage', markersize=6, linewidth=2, elinewidth=2, capsize=5)
ax2.errorbar(duration2, means, yerr=stds, color='red', fmt='o', mfc='white', linestyle='dashed', label='% cell coverage', markersize=6, linewidth=2, elinewidth=2, capsize=5)
ax1.set_xticks([0, 4, 8, 12, 16, 20, 24])
ax1.set_xlabel('time / h', weight='bold')
ax1.set_ylabel('OD$_{600}$', weight='bold')
ax2.set_ylabel('% cell coverage', weight='bold')
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
leg = ax1.legend(lines + lines2, labels + labels2, loc=2, prop={'size': 6}, frameon=False)

#plt.savefig('/mnt/cluster-victor/growth2/curve.png', dpi=600)
plt.show()

