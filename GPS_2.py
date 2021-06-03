
import time
import h5py 
import pytz
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone    

def get_sites(f):
    sites = [site for site in f]
    return sites


def get_sats(f, site):
    if site in f:
        sats = [sat for sat in f[site]]
    return sats


def get_data(f, site, sat, field):
    if site in f and sat in f[site]:
        times = f[site][sat][field][:]
    return times


def get_series(pth, site, sat, field):
    ts = get_data(pth, site, sat, 'timestamp')
    data = get_data(pth, site, sat, field)
    return ts, data



def get_map(pth, time, field):
    sfn=str(pth)+str(time)+str(field)
    save_file_name=''
    for i in range(len(sfn)):
        if(sfn[i] in ['.',':','-','+']):
            save_file_name=save_file_name+'_'
        else:
            save_file_name=save_file_name+sfn[i]
    try:
        result=np.load(save_file_name+'.npy')
    except:
        result = []
        timestamp = time.timestamp()
        start = timestamp
        end = timestamp
        f = h5py.File(pth, 'r')
        sites = get_sites(f)
        for site in sites:
            lat = np.degrees(f[site].attrs['lat'])
            lon = np.degrees(f[site].attrs['lon'])
            sats = get_sats(f, site)
            for sat in sats:
                timestamps = get_data(f, site, sat, 'timestamp')
                data = get_data(f, site, sat, field)
                match = np.where((timestamps >= start) & (timestamps <= end))
                data_match = data[match]
                for d in data_match:
                    result.append((d, lon, lat))
        result=np.array(result)
    if not result.any():
        return None
    else:
        np.save(save_file_name,result)
        return result



if __name__ == '__main__':
    plot_map = True
    pth = '2020-05-20.h5'
    if not plot_map:
        timestamps, data = get_series(pth, 'arsk', 'G03', 'dtec_20_60')
        times = [datetime.fromtimestamp(t, pytz.utc) for t in timestamps]
        plt.scatter(times, data)
        plt.xlim(times[0], times[-1])
        plt.show()
    else:
        epoch = datetime(2020, 5, 20, 12, 30, 0, tzinfo=timezone.utc)
        before = time.time()
        data = get_map(pth, epoch, 'dtec_20_60')
        print(f'It took {time.time() - before} sec. to retrieve a map')
        val = data[:, 0]
        x = data[:, 1]
        y = data[:, 2]
        plt.scatter(x, y, c=val)
        plt.xlim(-180, 180)
        plt.ylim(-90, 90)
        plt.show()
"""
import os
import numpy as np
import pytz
import matplotlib.pyplot as plt
import h5py
import time
from datetime import datetime, timezone



def get_file(path):
    if os.path.exists(path):
        f = h5py.File(path, 'r')
        return f;
    else:
        return None



def get_sites(file):
    sites = [site for site in file]
    return sites



def get_sats(file, site):
    if site in file:
        sats = [sat for sat in file[site]]
    return sats



def get_data(file, site, sat, field):
    if site in file and sat in file[site]:
        times = file[site][sat][field][:]
    return times



def prepare_data(file, field):
    results = [[] for _ in range(60*60*24)]

    sites = get_sites(file)
    for site in sites:
        lat = np.degrees(file[site].attrs['lat'])
        lon = np.degrees(file[site].attrs['lon'])
        sats = get_sats(file, site)
        for sat in sats:
            timestamps = get_data(file, site, sat, 'timestamp')
            data = get_data(file, site, sat, field)
            if (len(timestamps) != len(data)):
                continue
            for i in range(len(timestamps)):
                t = int(timestamps[i]) % (60 *60 * 24)
                results[t].append((data[i], lon, lat))
    return results



def get_map(data, time, value):
    results = [];
    timestamp = time.timestamp()
    t = int(timestamp) % (60 *60 * 24)
    return np.array(data[t])

    return np.array(results)



file = get_file('2020-05-20.h5')
field = 'dtec_20_60'
before = time.time()
data = prepare_data(file, field)
print(f'It took {time.time() - before} sec. to prepare a map')



epoch = datetime(2020, 5, 20, 12, 30, 0, tzinfo=timezone.utc)
before = time.time()
map_data = get_map(data, epoch, field)
print(f'It took {time.time() - before} sec. to retrieve a map')
print(type(map_data))

val = map_data[:, 0]
x = map_data[:, 1]
y = map_data[:, 2]
plt.scatter(x, y, c=val)
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.show()
"""