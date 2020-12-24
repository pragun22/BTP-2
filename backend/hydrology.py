from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import re
import glob
import shutil
import zipfile
import subprocess
from pcraster import matplotlib, numpy2pcr, setclone, Scalar, lddcreate, scalar, accuthresholdflux, pcr2numpy, lookupscalar

from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
from os.path import expanduser
import json
from PIL import Image
import rasterio.merge
import rainfall
import uuid
import matplotlib.colors as mcolors

cmap = mcolors.ListedColormap(['white', 'blue', 'orange', 'red'])
# bounds defined for colorcoding in mm
bounds=[0, 310, 1400, 1700, 10000]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

home = expanduser("~")
cwd = os.getcwd()

cityToFile = []
cityToBbox = []
fileToBbox = []
with open('fileMapper.json', 'r') as fp:
    cityToFile = json.load(fp)
with open('boundingBoxMapper.json', 'r') as fp:
    cityToBbox = json.load(fp)
with open('fileBbox.json', 'r') as fp:
    fileToBbox = json.load(fp)

lngmin, lngmax, latmin, latmax = -1, -1, -1, -1

# checks the orientation of dem files for merging 
def check(files):
    coords = []
    for x in files:
        x = x[:-5]
        x = x[-6:]
        coords.append(x)
    # down
    if coords[0][0:2] == coords[1][0:2]:
        return 0
    # side
    return 1


def comparator(file):
    return file[:-5][-6:]

# downscales images if images size is very large. For faster processing
def scale_image(dem, dimension):
    try:
        with rasterio.Env():
            with rasterio.open(dem) as dataset:
                data = dataset.read(1, out_shape=dimension,
                                    resampling=Resampling.bilinear)
                transform = dataset.transform * dataset.transform.scale(
                    (dataset.height / data.shape[0]),
                    (dataset.width / data.shape[1])
                )
                profile = dataset.profile
                profile.update(transform=transform, width=data.shape[
                               1], height=data.shape[0])
                with rasterio.open('scaled.tif', 'w', **profile) as dataset:
                    dataset.write(data, 1)
    except:
        pass

# processes dem file downloaded from bhuvan
def process_file(city):
    files = []
    Bbox = [1e6, 1e6, 0, 0]
    global latmax, latmin, lngmax, lngmin
    latmax = -1
    latmin = 1e6
    lngmax = -1
    lngmin = 1e6
    # computes the bounding box for current city
    for file in cityToFile[city]:
        files.append(file)
        lngmin = min(lngmin, int(fileToBbox[file][0]))
        latmin = min(latmin, int(fileToBbox[file][1]))
        lngmax = max(lngmax, int(fileToBbox[file][2]))
        latmax = max(latmax, int(fileToBbox[file][3]))
    # city lies withing single Bbox so no need to merge
    if len(files) == 1:
        dem = glob.glob('dataset/' + files[0] + '/*/*.tif')[0]
        scale_image(dem, (100, 100))
    # city dem data composed of 4 tiles of bhuvan data
    elif len(files) == 4:
        files = sorted(files, key=comparator)
        dem0 = glob.glob('dataset/' + files[0] + '/*/*.tif')[0]
        dem1 = glob.glob('dataset/' + files[1] + '/*/*.tif')[0]
        dem2 = glob.glob('dataset/' + files[2] + '/*/*.tif')[0]
        dem3 = glob.glob('dataset/' + files[3] + '/*/*.tif')[0]
        mosaic = []
        mosaic.append(rasterio.open(dem0))
        mosaic.append(rasterio.open(dem1))
        mosaic.append(rasterio.open(dem2))
        mosaic.append(rasterio.open(dem3))
        out_meta = mosaic[1].meta.copy()
        mosaic, out_trans = rasterio.merge.merge(mosaic)
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans})
        with rasterio.open("scaled.tif", "w", **out_meta) as dest:
            dest.write(mosaic)
        scale_image('scaled.tif', (200, 200))
    # city dem data composed of 2 tiles of bhuvan data
    else:
        # both tiles side by side
        if check(files):
            files = sorted(files, key=comparator)
            dem0 = glob.glob('dataset/' + files[0] + '/*/*.tif')[0]
            dem1 = glob.glob('dataset/' + files[1] + '/*/*.tif')[0]
            mosaic = []
            mosaic.append(rasterio.open(dem0))
            mosaic.append(rasterio.open(dem1))
            out_meta = mosaic[1].meta.copy()
            mosaic, out_trans = rasterio.merge.merge(mosaic)
            out_meta.update({"driver": "GTiff",
                             "height": mosaic.shape[1],
                             "width": mosaic.shape[2],
                             "transform": out_trans})
            with rasterio.open("scaled.tif", "w", **out_meta) as dest:
                dest.write(mosaic)
            scale_image('scaled.tif', (100, 200))
        # one tile lies above other
        else:
            files = sorted(files, key=comparator)
            dem0 = glob.glob('dataset/' + files[0] + '/*/*.tif')[0]
            dem1 = glob.glob('dataset/' + files[1] + '/*/*.tif')[0]
            mosaic = []
            mosaic.append(rasterio.open(dem0))
            mosaic.append(rasterio.open(dem1))
            out_meta = mosaic[1].meta.copy()
            mosaic, out_trans = rasterio.merge.merge(mosaic)
            out_meta.update({"driver": "GTiff",
                             "height": mosaic.shape[1],
                             "width": mosaic.shape[2],
                             "transform": out_trans})
            with rasterio.open("scaled.tif", "w", **out_meta) as dest:
                dest.write(mosaic)
            scale_image('scaled.tif', (200, 100))


# performs hydrological mapping for custom catchment
def hydrology_mapping1(dem, rain, infiltration=None, soil=None):
    try:
        # create local drain direction
        setclone(dem)
        ldd = lddcreate(dem, 1e31, 1e31, 1e31, 1e31)
        # set infiltration to 0
        infilcap = scalar(0)
        if soil is not None:
            # if infiltration data availble then use it along with soil data
            if infiltration is not None:
                infilcap = lookupscalar(infiltration, soil)
            else:
                infilcap = scalar(soil)
        # calculate runoff by simulating flow
        randomField = scalar(rain)
        runoff = accuthresholdflux(ldd, randomField, infilcap)
        x = pcr2numpy(runoff, 0)
        runoff/=1000
        print(np.max(x))
        filename = "static" + "/" + str(uuid.uuid4()) + ".jpg"
        # create and save plot and return url where plot is stored
        matplotlib.plot(runoff, labels=None, title=None,
                        filename=filename)
        return filename
    except:
        return []

# performs city level hydrological mapping
def hydrology_mapping(dem, rain, infiltration=None, soil=None, flag=0):
    try:
        # load dem data
        x = gdal.Open(dem)
        gdal_band = x.GetRasterBand(1)
        nodataval = gdal_band.GetNoDataValue()
        x = x.ReadAsArray().astype(np.float)
        # replace no val with very large value
        if np.any(x == nodataval):
            x[x == nodataval] = 1e31
        setclone(x.shape[0], x.shape[1], 0.1, -lngmin, latmin)
        x = numpy2pcr(Scalar, x, 0)
        # create local drain direction
        ldd = lddcreate(x, 1e31, 1e31, 1e31, 1e31)
        
        # set infiltration to 0
        infilcap = scalar(0)
        if soil is not None:
            # if infiltration data availble then use it along with soil data
            if infiltration is not None:
                infilcap = lookupscalar(infiltration, soil)
            else:
                infilcap = scalar(soil)
        randomField = scalar(rain)
        # calculate runoff by simulating flow
        runoff = accuthresholdflux(ldd, randomField, infilcap)
        x = pcr2numpy(runoff, 0)
        filename = str(uuid.uuid4()) + ".jpg"
        filename = "static/" + filename
        fig = plt.figure(frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(x, aspect='auto', cmap=cmap, norm=norm)
        # create and save plot and return url where plot is stored
        fig.savefig(filename)
        plt.close(fig)  
        return filename
    except:
        return []

def map_hydrology(city, date):
    try:
        os.remove("static/random.jpg")
    except:
        pass
    city = city.lower()
    # gets rainfall prediction from wunderground
    rain = 5
    # rain = rainfall.get_rainfall(city, date)
    # processes dem data for current city
    process_file(city)
    cityCentre = [(float(cityToBbox[city][0]) + float(cityToBbox[city][2])) / 2,
                  (float(cityToBbox[city][1]) + float(cityToBbox[city][3])) / 2]
    return cityCentre, [lngmin, latmin, lngmax, latmax],  hydrology_mapping("scaled.tif", rain), rain


def custom_hydrology(rain, dem, infiltration=None, soil=None):
    # if dem in map format then not need to rescale
    if dem[-3:] == "map":
        return hydrology_mapping1(dem, rain, infiltration, soil)
    else:
        # downscales image for faster processing
        scale_image(dem, (100, 100))
        return hydrology_mapping("scaled.tif", rain, infiltration, soil, 1)
