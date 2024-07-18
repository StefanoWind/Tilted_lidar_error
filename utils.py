# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:10:21 2024

@author: sletizia
"""
import numpy as np
from matplotlib import pyplot as plt

def vstack(a,b):
    '''
    Stack vertically vectors
    '''
    if len(a)>0:
        ab=np.vstack((a,b))
    else:
        ab=b
    return ab   

def cosd(x):
    return np.cos(x/180*np.pi)

def sind(x):
    return np.sin(x/180*np.pi)

def axis_equal():
    '''
    Makes axis of plot equal
    '''
    from mpl_toolkits.mplot3d import Axes3D
    ax=plt.gca()
    is_3d = isinstance(ax, Axes3D)
    if is_3d:
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        zlim=ax.get_zlim()
        ax.set_box_aspect((np.diff(xlim)[0],np.diff(ylim)[0],np.diff(zlim)[0]))
    else:
        xlim=ax.get_xlim()
        ylim=ax.get_ylim()
        ax.set_box_aspect(np.diff(ylim)/np.diff(xlim))
        