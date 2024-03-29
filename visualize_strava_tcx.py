import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

def find_rec(node, element):
    def _find_rec(node, element, result):
        for el in node:
            _find_rec(el, element, result)
        tag_list = node.tag.split('}')
        descriptive_tag = tag_list[-1]
        if descriptive_tag == element:
            result.append(node)
    result = list()
    _find_rec(node, element, result)
    return result


def get_as_array(r, tag):
    # r must be an array of leaf nodes
    el_list = find_rec(r, tag)
    el_array = [el.text for el in el_list]
    return np.array(el_array).astype(np.float)


def plot_colourline(x,y,c, plot_colorbar=False, lbl=''):
    '''
    continous color bar is plotted based off values of c
    '''
    cmap = mpl.cm.spring # change this for some fun
    c_norm = plt.cm.spring((c-np.min(c))/(np.max(c)-np.min(c)))
    ax = plt.gca()
    for i in np.arange(len(x)-1):
        a = ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=c_norm[i])
    if plot_colorbar:
        norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
        plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', label=lbl)
    return


def plot_group_activities(path, include_keyword=''):
    # get all of the files at the directory that are TCX and contain keyword
    _, _, filenames = next(os.walk(path))
    valid_files = list()
    for f in filenames:
        # get all the tcx files
        split_string = f.split('.')
        if split_string[-1] == 'tcx':
            # check if file includes the desired keyword
            if include_keyword in f:
                # plot it!
                plot_one_activity(path+f, do_show=False, colorbar=False)
    plt.show()
    return


def plot_one_activity(fname, do_show=True, colorbar=True):
    tree = ET.parse(fname)
    root = tree.getroot()

    # get data of interest
    lat = get_as_array(root, 'LatitudeDegrees')
    lon = get_as_array(root, 'LongitudeDegrees')
    z   = get_as_array(root, 'AltitudeMeters')
    h   = get_as_array(root, 'Value') # strava's HeartRateBPM has a child called Value for some reason
                                      #  luckily there aren't any other tags called value that I've
                                      #  encountered so far

    norm_z = (z-z.min())/np.max(z-z.min())

    fig = plt.figure(1, figsize=(5,5))
    ax  = fig.add_subplot(111)
    plot_colourline(lon, lat, z, colorbar, lbl='heart rate BPM')
    plt.axis('off')
    plt.axis('scaled')  # this looks wonky compared to the strava map, but provides some "ground truth"
    if do_show:    
        plt.show()
    return
    

if __name__ == '__main__':
    fname = 'data/Afternoon_Ride-2.tcx'
    #plot_one_activity(fname)

    # multiple activites
    data_path = 'data/2021-04-07_garmin_connect_export/'
    key = 'St_Louis'
    plot_group_activities(data_path, key)

    
    
    
        

