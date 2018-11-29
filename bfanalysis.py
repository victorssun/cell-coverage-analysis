# functions for cell coverage calculations

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:01:14 2018

@author: A
lower the px value, the darker the colour
make white the bg, black the interest: plt white = 1, black = 0
interest - low px, bg - high px

"""

'''
load_img() - in
ax_labeloff() - in
show_imgs() - in
find_thresh() - in
sd_img() - in
entro_img() - in
otsu() - in
threshold_img() - in
threshold_img_cv2() - in
histo_img2() - in
crop_img() - in
y2b_save() - in
ezplot() - in
'''


import numpy as np
from matplotlib import pyplot as plt
import scipy, cv2, os
from scipy.ndimage import label

def load_img(filename, rgb=1, norm=False):
    # load img with cv2. if the geeqie picture is yellow: 0=r, 1=g, 2=b. if blue: 0=b, 1=g, 2=r
    # if geeqie colour is yellow, pylab colour is blue
    img = cv2.imread(filename)
    img = img[:,:,0:3] # get rid of alpha
    img_select = img[:,:,rgb]
    if norm == True:
        img_select = img_select / float(img_select.max()) # won't work with cv2 thresh
    return img, img_select

def ax_labeloff(ax):
    ax.tick_params(
            labelleft=False,
            labelbottom=False,
            left=False,
            bottom=False)
    return ax

def show_imgs(bundle_imgs, titles=['']):
    # always with two rows, requires imgs to be in a list, if run on linux, needs plt.show() at end of script, not function
    fig = plt.figure()
    plt.rcParams['font.size'] = 6
    count_imgs = len(bundle_imgs)
    if len(titles) == 1:
        titles = titles * count_imgs
    if count_imgs == 1:
        ncols = 1
        nrows = 1
    elif count_imgs > 1:
        ncols = int(round(count_imgs / 2.0))
        nrows = 2
    for ea in range(len(bundle_imgs)):
        ax = fig.add_subplot(nrows, ncols, ea+1)
        #ax.imshow(bundle_imgs[ea])
        ax.imshow(bundle_imgs[ea], cmap='gray')
        ax.set_title(titles[ea])
        ax = ax_labeloff(ax)
    plt.tight_layout(True)
    #plt.show()
    return 

def find_thresh(img, bins=0, preview=True, scale=True, img_orig=''):
    # histogram the distribution of px intensity of the img, to roughly guess threshold
    img_flat = img.flatten() # collect histogram
    if bins == 0:
        bins = img_flat.max() - img_flat.min()
    bin_counts, bin_edges = np.histogram(img_flat, bins)
    if preview == True:
        plt.rcParams['font.size'] = 6
        fig = plt.figure() # create plot
        ax1 = fig.add_subplot(222)
        ax1.imshow(img)
        ax1.set_title('img')
        ax2 = fig.add_subplot(212)
        if type(img_orig) == type(np.array([])):
            ax3 = fig.add_subplot(221)
            ax3.imshow(img_orig)
            ax3.set_title('original')
            #bin_counts_orig, bin_edges_orig = np.histogram(img_orig.flatten(), bins)
            #ax2.bar(bin_edges_orig[:-1], bin_counts_orig, color='orange')
        ax2.bar(bin_edges[:-1], bin_counts)
        ax2.plot(bin_edges[:-1], bin_counts)
        ax2.set_xlabel('px intensity')
        ax2.set_ylabel('counts')
        if scale == True:
            ax2.set_yscale('log')
        #ax2.hist(img_flat, bins) # same, but only good for plotting
        #ax2.set_ylim([0, 100])
        plt.tight_layout(True)
    return bin_counts, bin_edges

def sd_img(img, norm=True):
    img_flat = img.flatten()
    avg = np.mean(img_flat)
    sd = np.std(img_flat)
    if norm == True:
        sd = sd / float(avg)
    return sd, avg

def entro_img(bin_counts):
    # fake entropy, just favours img with largest single bin
    bin_counts_norm = bin_counts / float(max(bin_counts))
    entro_fake = sum(bin_counts_norm * bin_counts_norm)
    return entro_fake

def otsu(img, blur=False):
    # otsu's can be used to roughly find a good threshold value
    if blur == True:
        img = cv2.GaussianBlur(img, (5,5), 0)
    ret, img_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print('%d otsu threshold' %ret)
    return ret, img_thresh

def threshold_img(img, threshold, norm=False):
    # thresholding, option to normal data first: returns b/w img to plot and data to histogram, and fraction value
    if norm == True:
        img_norm = img/float(img.max())
    else:
        img_norm = img
    img_mask = img_norm < threshold # anything lower than threshold, is of interest. as threshold decreases, interest gets tigheter
    #img_mask = np.invert(img_mask)
    #img_mask = img_mask.astype(int)
    #img_threshold = img_norm * img_mask
    img_threshold = np.invert(img_mask) # since interest is 1, plt wants 1 to be white, need to inversed to be plotted nicely
    img_labelled, num_features = label(img_mask) # count 1's
    frac = (img_mask).sum() / float(len(img)*len(img[0])) * 100
    print('%0.2f%% coverage | %d spots' %(frac, num_features))
    return img_threshold, img_labelled, frac

def threshold_img_cv2(img_slice, threshold, maxvalue=255):
    # only tried if input img is just one rgb slice, would a whole img work?
    ret, img_thresh = cv2.threshold(img_slice, threshold, maxvalue, cv2.THRESH_BINARY) #img is 0's and 255's
    img_prelabel = img_thresh < (maxvalue - 50) # convert 0's and 255's to T/F... -50 as a buffer for some reason
    img_labelled, num_features = label(img_prelabel)
    frac = (100 * (1-(img_thresh/maxvalue).sum() / float(len(img_thresh) * len(img_thresh[0])))) # 100 * # of 255's / tot # of px
    print('%0.2f%% coverage | %d spots - cv2' %(frac, num_features))
    return img_thresh, img_labelled, frac

def histo_img2(img, pxconverter=0.02562347656, bins=0, preview=True, crude=False, title='', img_rgb=''):
    # histogram the size of pixels with a labelled img b/w
    img_flat = img.flatten()
    #pxconverter = 0.160109
    #pxconverter = 0.02562347656 # 50x real
    #pxconverter = 0.00480651855 # 100x real
    counts_list = []
    if crude == True:
        for i in range(1, img_flat.max()+1):
            counts = list(img_flat).count(i) * pxconverter
            print counts
            counts_list.append(counts)
    elif crude == False:
        n_counts, counts_list = np.unique(img, return_counts=True)
        counts_list = counts_list[1:] * pxconverter # list of all labelled spots and their size
    
    if bins == 0:
        print n_counts
        bins = n_counts / 10
    if preview == True:
        plt.rcParams['font.size'] = 7
        fig = plt.figure()
        if type(img_rgb) == type(np.array([])):
            ax3 = fig.add_subplot(221)
            ax3.imshow(img_rgb)
            ax3.set_title('img')
        ax1 = fig.add_subplot(222)
        img2 = np.invert((img>1).astype(int))
        ax1.imshow(img2, cmap='gray') # ignore
        ax1.set_title('threshold')
        ax2 = fig.add_subplot(212)
        ax2.hist(counts_list, bins)
        ax2.set_yscale('log')
        ax2.set_xlim([0, max(counts_list)])
        ax2.set_xlabel('colony size / $\mu$m$^2$')
        ax2.set_ylabel('counts')
        ax2.set_title(title)
        plt.tight_layout(True)
    return counts_list

def crop_img(img, edge):
    # crop rgb image from center
    h = len(img)
    w = len(img[0])
    img = img[edge:h-edge, edge:w-edge, :]
    return img

def y2b_save(filename, img):
    # convert yellow BGR to blue RGB image
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filename, img2)
    print('%s saved.' %filename)

def ezplot(img, title=''):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(img, cmap='gray')
    ax.set_title(title)

def cellcoverage_img(filename, pxconverter, bins=50, preview=True):
    # cell coverage of one image, outputting colony size distribution, and fraction
    img, img_select = load_img(filename, 1)
    ret, img_otsu = otsu(img_select)
    threshold = ret - 7 # offset otsu value by 7
    img_thresh, img_labelled, frac = threshold_img_cv2(img_select, threshold)
    #pxconverter = 0.00480651855 # 100x
    #pxconverter = 0.02562347656 # 50x
    counts_list = histo_img2(img_labelled, pxconverter, bins, title='%0.2f%% coverage | %d threshold' %(frac, threshold), img_rgb=img_select, preview=preview)
    return counts_list, bins, frac

def cellcoverage_multiavg(filenames, pxconverter, bins=50, preview=True):
    # cell coverage of multiple images by outputting an average % coverage from distribution of % coverage from each image
    frac_list = []
    counts_list2 = []
    for f in filenames:
        img, img_select = load_img(f, 1)
        ret, img_otsu = otsu(img_select)
        threshold = ret - 7
        img_thresh, img_labelled, frac = threshold_img_cv2(img_select, threshold)
        frac_list.append(frac)
        counts_list = histo_img2(img_labelled, pxconverter, bins, title='%0.2f%% coverage | %d threshold' %(frac, threshold), img_rgb=img_select, preview=preview)
        counts_list2.extend(counts_list)
    return frac_list, counts_list2

def save_bwimg(filename):
    # save a bw img of an example img
    #filename = '/mnt/cluster-victor/lin_motors/pics/.....png'
    img, img_select = load_img(filename, 1)
    ret, img_otsu = otsu(img_select)
    threshold = ret - 7
    img_thresh, img_labelled, frac = threshold_img_cv2(img_select, threshold) # this is ran twice
    cv2.imwrite('/mnt/cluster-victor/analysis/counting/ecoli_test.png', img_thresh)
    print( 'bw img saved.')
    cellcoverage_img(filename, 0.256235, 100, True)
    plt.show()

def plot_twincurve(duration_od600, od600, duration_coverage, coverage, fig=''):
    # plot od600 + coverage curve
    # od600 should be a np array with replicates
    if fig == '':
        fig = plt.figure(figsize=[3.5, 2])
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    #ax1.plot(duration_od600, od600, marker='.', color='blue', label='OD600')
    ax1.errorbar(duration_od600, od600.mean(axis=1), yerr=od600.std(axis=1), color='blue', fmt='o', mfc='white', linestyle='dashed', label='OD$_{600}$', markersize=6, linewidth=2, elinewidth=2, capsize=5)
    ax2.plot(duration_coverage, coverage, marker='.', color='red', label='% cell coverage')
    #ax2.errorbar(duration_coverage, 
    ax1.set_xlabel('time / h')
    ax1.set_ylabel('OD$_{600}$')
    ax2.set_ylabel('% cell coverage')
    fig,legend(loc=4)
    plt.show()



'''
# check os
if os.name == 'nt':
    direct = 'C:/Users/A/Desktop/K/Chem 599/Work/counting/'
elif os.name == 'posix':
    direct = '/mnt/cluster-victor/analysis/counting/'
### MAIN CODE

# grab all img filenames from directory
files = os.listdir('%s' %direct)
filenames = []
for f in files:
    if f.find('.png') != -1:
        filenames.append(f)

# testing with 100x: 0.070/1024* 0.090/1280 (mm/px)
#filename = '/old/20180625_100x_ecoli_final.png'

# testing with 50x: 0.16/1024 * 0.21/1280 (mm/px)
direct2 = '/mnt/cluster-victor/lin_motors/pics/raster/20180706_zscan/'
filename = direct2 + '00_0129step0.001000_p6.471723.png' # out of focus, blue is focused
#filename = direct2 + '05_0129step0.001000_p6.476679.png' # in focus, green is focused

# load img, find threshold value
img, flat = load_img(filename, 2)
find_thresh(flat, 30, img_orig=img)
ret2, thresh2 = otsu(flat) # compare with otsu/gaussian filter roughly the same
ret3, thresh3 = otsu(flat, True)
#ezplot(thresh2, '%d threshold' %ret2)

# simple threshold
threshold = 55 # decrease threshold for more precision
#threshold = ret2 - 7 # offset otsu value by 7
flat_thresh, img_labelled, coverage = threshold_img(flat, threshold, False) #1st used to plot, 2nd used to analyze
thresh1, img_labelled2, coverage_cv2 = threshold_img_cv2(flat, threshold)

# plot slices of image
imgs = []
imgs.append(img)
print img.sum() # print total pxs and their slices
imgs.append(flat)
imgs.append(flat_thresh)
#imgs.append(thresh1)
try: 
    z = len(img[0,0,:])
    for i in range(z):
        imgs.append(img[:,:,i])
        print img[:,:,i].sum()
except:
    pass
show_imgs(imgs, ['original', 'preprocess', 'bw - %0.2f%%' %coverage, 'r', 'g', 'b'])

counts_list1 = histo_img2(img_labelled, 100, crude=False, title='%0.2f%% coverage | %d threshold' %(coverage, threshold), img_rgb=flat)
counts_list2 = histo_img2(img_labelled2, 100, title='%0.2f%% coverage | %d threshold' %(coverage_cv2, threshold), img_rgb=flat)

if False:
    # compare simple, otsu, otsu w/ filter
    imgs_otsu = [flat_thresh, thresh2, thresh3]
    show_imgs(imgs_otsu, ['simple - %d threshold' %threshold, 'otsu - %d' %ret2, 'otsu w/ filter - %d' %ret3])
 
    # compare original, simple, cv2, difference between the two
    flat_compare = thresh1 > 200
    flat_compare = flat_compare.astype(int) - flat_thresh.astype(int)
    imgs2 = [flat, flat_thresh, thresh1, flat_compare]
    show_imgs(imgs2, ['preprocess', 'simple', 'cv2', 'diff'])

plt.show()
'''
