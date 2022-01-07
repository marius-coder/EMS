# -*- coding: utf-8 -*-
import pandas as pd
from os.path import exists
from urllib.request import urlretrieve
import urllib.request, json , urllib.parse
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import requests

import numpy as np
import os
import sys
from bokeh import plotting, embed, resources
from bokeh.models import HoverTool, DataRange1d
from bokeh.plotting import figure
from bokeh.io import output_file, show
from PyQt5 import *
#from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import pandas_bokeh
import warnings


class WindowErdwärmeKarte(QWidget):
    


    def __init__(self):
        super().__init__()

       
        self.setWindowTitle("Strom_Nutzungsmischung")

        #Layout
        self.m_output = QtWebEngineWidgets.QWebEngineView()
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.m_output)
        

    def UpdatePlot(self, address, layer):

        def get_gdf_from_wfs(layer):
            """
            Get geopandas.GeoDataFrame from data.wien.gv.at WFS service based on layer name
    
            Parameters
            ----------
            layer : string
                WFS layer name 
            """
            file = f'EMS-Frontend/data/{layer}.json'
            url = f"https://data.wien.gv.at/daten/geo?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:{layer}&srsName=EPSG:4326&outputFormat=json"
            if not exists(file):
                urlretrieve(url, file)
            return gpd.read_file(file)

        warnings.filterwarnings("default")
        pandas_bokeh.output_file("EMS-Frontend/data/ErdwarmeKarte.html")
        gdf = get_gdf_from_wfs("ERDWSONDOGD")

        plot1 = gdf.plot_bokeh(figsize=(1000, 1000),colormap = "Magma",category=layer,show_colorbar = True, alpha = 0.3,
                      return_html = True, show_figure = False)

        df_coordinateAddress = pd.DataFrame(from_address(address))

        #pandas_bokeh.output_file("EMS-Frontend/data/ErdwarmeKarte2.html")
        df_coordinateAddress.plot_bokeh(
                kind="point",size=10,
                marker="x",show_figure = False,return_html = True)

        self.m_output.setHtml(plot1)
        warnings.filterwarnings("error")





def from_address(address_string="Stephansplatz, Wien, Österreich"):
    parsed_address = urllib.parse.quote(address_string)
    url = 'https://nominatim.openstreetmap.org/search/' + parsed_address +'?format=json'
    response = requests.get(url).json()
    location = (float(response[0]["lon"]), float(response[0]["lat"]) )
    return location
    
     
       


def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False


def convert_GeoPandas_to_Bokeh_format(gdf):
    """
    Function to convert a GeoPandas GeoDataFrame to a Bokeh
    ColumnDataSource object.
    
    :param: (GeoDataFrame) gdf: GeoPandas GeoDataFrame with polygon(s) under
                                the column name 'geometry.'
                                
    :return: ColumnDataSource for Bokeh.
    """
    gdf_new = gdf.drop('geometry', axis=1).copy()
    gdf_new['x'] = gdf.apply(getGeometryCoords, 
                             geom='geometry', 
                             coord_type='x', 
                             shape_type='polygon', 
                             axis=1)
    
    gdf_new['y'] = gdf.apply(getGeometryCoords, 
                             geom='geometry', 
                             coord_type='y', 
                             shape_type='polygon', 
                             axis=1)
    
    return ColumnDataSource(gdf_new)


def getGeometryCoords(row, geom, coord_type, shape_type):
    """
    Returns the coordinates ('x' or 'y') of edges of a Polygon exterior.
    
    :param: (GeoPandas Series) row : The row of each of the GeoPandas DataFrame.
    :param: (str) geom : The column name.
    :param: (str) coord_type : Whether it's 'x' or 'y' coordinate.
    :param: (str) shape_type
    """
    
    # Parse the exterior of the coordinate
    if shape_type == 'polygon':
        exterior = row[geom].geoms[0].exterior
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            return list( exterior.coords.xy[0] )    
        
        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return list( exterior.coords.xy[1] )
