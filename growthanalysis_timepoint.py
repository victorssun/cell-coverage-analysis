# calclate % cell coverage over time by averaging multiple images from multiple subdirectories

import numpy as np
import bfanalysis as cvr
import scipy
from matplotlib import pyplot as plt
import os, pickle

if os.name == 'posix':
    direct = '/mnt/cluster-victor/lin_motors/pics/raster/20181024_growth1/'
    #direct = '/mnt/cluster-victor/lin_motors/pics/raster/20180825_growth3/'
else:
    ' computer is not linux system, check.'

# parameters
npics = 40 # select how many imgs to analyze per slide
pxconverter = 0.2562347656
savepicklesas = ['0h_data', '4h_data', '5h_data', '6h_data', '7h_data', '24h_data'] # name of pickle files
subdirectsas = [['0h_1/', '0h_2/'],
        ['4h_1/', '4h_2/'],
        ['5h_1/', '5h_2/'],
        ['6h_1/', '6h_2/'],
        ['7h_1/', '7h_2/'],
        ['24h_1/', '24h_2/']]
'''
subdirectsas = [['0h_1/', '0h_2/', '0h_3/'], 
        ['5h_1/', '5h_2/', '5h_3/'], 
        ['8h_1/', '8h_2/'], 
        ['12h_3/', '12h_2/', '12h_3/'], 
        ['15h_1/', '15h_2/'],
        ['25h_1/', '25h_2/']] # subdirectories/per slide
'''
bins = 100 # bin value if plotting with multi=False
preview = False
multi = True # True to run multiple times

if multi == True:
    for i in range(len(savepicklesas)):
        filenames = []
        for sub in subdirectsas[i]:
            files = os.listdir('%s%s' %(direct, sub))
            for f in files[0:npics]:
                if f.find('.png') != -1:
                    filenames.append('%s%s%s' %(direct, sub, f))
        frac_list, counts_list2 = cvr.cellcoverage_multiavg(filenames, pxconverter, bins, preview)
        print('%.2f%% coverage - saved: %s' %(np.mean(frac_list), savepicklesas[i]))
        pickle.dump([frac_list, counts_list2], open('%s%s.pickle' %(direct, savepicklesas[i]), 'wb'))

elif multi == False:
    savepickle = '24hr_data'
    # grab all img filenames from directories
    subdirects = ['24hr_1/', '24hr_2/', '24hr_3/']
    #subdirects = ['0hr/']
    filenames = []
    for sub in subdirects:
        files = os.listdir('%s%s' %(direct, sub))
        for f in files[0:40]:
            if f.find('.png') != -1:
                filenames.append('%s%s%s' %(direct, sub, f))

    frac_list, counts_list2 = cvr.cellcoverage_multiavg(filenames, pxconverter, bins, preview)
    print(np.mean(frac_list))
    #print(np.mean(frac_list), np.mean(frac_list[0:50]), np.mean(frac_list[0:25]))

    fig = plt.figure()
    fig.set_tight_layout(True)
    ax1 = fig.add_subplot(211)
    ax1.hist(frac_list)
    ax1.set_xlabel('% cell coverage')
    ax1.set_ylabel('counts')
    #title_mask = '%% coverage distribution of %d imgs' %len(filenames)
    #ax1.set_title(title_mask)
    ax1.set_title('%% coverage distribution of %d imgs' %len(filenames))

    ax2 = fig.add_subplot(212)
    ax2.hist(counts_list2, bins)
    ax2.set_yscale('log')
    ax2.set_xlabel('colony size / $\mu$m$^2$')
    ax2.set_ylabel('counts')
    ax2.set_title('colony size distribution')

    plt.show()

    # save fraction and colony size distrubtion data
    pickle.dump([frac_list, counts_list2], open('%s%s.pickle' %(direct, savepickle), 'wb'))

