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


def plot_colourline(x,y,c, plot_colorbar=False, lbl='', c_normed=False):
    '''
    continous color bar is plotted based off values of c
    '''
    fig = plt.figure(1, figsize=(5,5))
    ax  = fig.add_subplot(111)
    cmap = mpl.cm.spring # change this for some fun
    if not c_normed:
        c_norm = plt.cm.spring((c-np.min(c))/(np.max(c)-np.min(c)))
    else:
        c_norm = c
    for i in np.arange(len(x)-1):
        a = ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=c_norm[i])
    if plot_colorbar:
        norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
        plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', label=lbl)
    plt.axis('off') 
    plt.axis('scaled')  # this looks wonky compared to the strava map, but provides some "ground truth"
    return


def plot_group_activities(path, include_keyword=''):
    all_lat = []
    all_lon = []

    arr_z   = np.array([])
    arr_h   = np.array([])
    # get all of the files at the directory that are TCX and contain keyword
    _, _, filenames = next(os.walk(path))
    valid_files = list()
    for f in filenames:
        # get all the tcx files
        split_string = f.split('.')
        if split_string[-1] == 'tcx':
            # check if file includes the desired keyword
            if include_keyword in f:
                tree = ET.parse(path+f)
                root = tree.getroot()
                all_lat.append( get_as_array(root, 'LatitudeDegrees') ) 
                all_lon.append( get_as_array(root, 'LongitudeDegrees'))
                #all_lat = np.hstack( (all_lat, get_as_array(root, 'LatitudeDegrees')) )
                #all_lon = np.hstack( (all_lon, get_as_array(root, 'LongitudeDegrees')))
                arr_z   = np.hstack( (arr_z,   get_as_array(root, 'AltitudeMeters'))  )
                arr_h   = np.hstack( (arr_h,   get_as_array(root, 'Value'))           )
    
    i_want = arr_z
    i_want_norm = plt.cm.spring((i_want-np.min(i_want))/(np.max(i_want)-np.min(i_want)))

    print(len(all_lat))
    print(len(all_lon))
    loc = 0
    for i in range(len(all_lat)):
        left = loc
        right = loc+len(all_lat[i])
        c = i_want_norm[left:right]
        print(len(c))
        print(len(all_lon[i]))
        print(len(all_lat[i]))
        if len(c) != len(all_lon[i]) != len(all_lat[i]):
            print('Error: three arrays are not of the same size')
            return
        plot_colourline(np.array(all_lon[i]), np.array(all_lat[i]), i_want_norm[left:right], plot_colorbar=False, lbl='Altitude', c_normed=True) 
        loc = right
    plt.show()
    return


def plot_one_activity(fname, colorbar=True):
    tree = ET.parse(fname)
    root = tree.getroot()

    # get data of interest
    lat = get_as_array(root, 'LatitudeDegrees')
    lon = get_as_array(root, 'LongitudeDegrees')
    z   = get_as_array(root, 'AltitudeMeters')
    h   = get_as_array(root, 'Value') # strava/garmins's HeartRateBPM has a child called Value for some reason
                                      #  luckily there aren't any other tags called value that I've
                                      #  encountered so far

    norm_z = (z-z.min())/np.max(z-z.min())

    plot_colourline(lon, lat, z, colorbar, lbl='heart rate BPM') 
    plt.show()
    return
    

if __name__ == '__main__':
    fname = 'data/Afternoon_Ride-2.tcx'
    #plot_one_activity(fname)

    # multiple activites
    data_path = 'data/2021-04-07_garmin_connect_export/'
    key = 'St_Louis'
    plot_group_activities(data_path, key)

    
    
    
        

