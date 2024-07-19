# -*- coding: utf-8 -*-
"""
Calculate bias due to cross-contamination based on difference between wide scan approximation and DBS hypothesis
"""
import numpy as np
import utils as utl
from matplotlib import pyplot as plt
import warnings
import matplotlib
warnings.filterwarnings('ignore')
plt.close('all')

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.size'] = 16

#%% Inputs

#Example 1: regular DBS
alpha=np.array([0,0,90,180,270])#[deg] azimuth angles
beta=np.array([90,62,62,62,62])#[deg] elevation angles

# #Example 2: severely inclined DBS
# alpha=np.array([0,0,19.1,340.9])#[deg] azimuth angles
# beta=np.array([25.9,45,31.7,31.7])#[deg] elevation angles

RS=np.array([[1,0,-0.1],
             [0,0.7,0],
             [-0.1,0,0.5]])#[m/s] Reynolds stress tensors

RS_index={0:[0,0],1:[1,1],2:[2,2],3:[0,1],4:[0,2],5:[1,2]}#Reynolds stress index

RS_names=[r'$\overline{U^\prime U^\prime}$',
          r'$\overline{V^\prime V^\prime}$',
          r'$\overline{W^\prime W^\prime}$',
          r'$\overline{U^\prime V^\prime}$',
          r'$\overline{U^\prime W^\prime}$',
          r'$\overline{V^\prime W^\prime}$']#names of Reynolds stresses (for plotting)

#%% Initialization
assert len(alpha)==len(beta), 'Number of azimuths does not match number of elevations'

Nb=len(alpha)

#zeroing
bias=np.zeros(6)

#%% Main

#lidar matrix
A=[]
for a,b in zip(alpha,beta):
    A=utl.vstack(A,np.array([utl.cosd(b)*utl.cosd(a),utl.cosd(b)*utl.sind(a),utl.sind(b)]))

#pseudo-inverse matrix
A_plus=np.matmul(np.linalg.inv(np.matmul(A.T,A)),A.T)

#bias calculation
for i in range(6):
    j=RS_index[i][0]
    k=RS_index[i][1]
    for l in range(Nb):
        for m in range(Nb):
            for n in range(3):
                for p in range(3):
                    bias[i]+=A_plus[j,l]*A_plus[k,m]*A[l,n]*A[m,p]*RS[n,p]*((l==m)-1)
                    
#%% Plots
plt.figure(figsize=(18,8))

#draw scan geometry
ax=plt.subplot(1,2,1,projection='3d')
for a,b in zip(alpha,beta):
    r=1/utl.sind(b)
    x=r*utl.cosd(b)*utl.cosd(a)
    y=r*utl.cosd(b)*utl.sind(a)
    z=r*utl.sind(b)

    plt.plot([0,x],[0,y],[0,z],'-k',linewidth=1,alpha=0.75)
    plt.plot(x,y,z,'.k',alpha=1,markersize=7)
    plt.plot(x,y,z*0,'.k',alpha=0.25,markersize=7)

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_zlabel(r'$z$')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.patch.set_alpha(0)   
utl.axis_equal()
plt.title('Scan geometry')

plt.subplot(1,2,2)
plt.bar(RS_names,bias,color='k')
plt.ylabel(r'$\Delta \Sigma_i$ [m s$^{-1}$]')
plt.grid()
plt.title('Cross-contamination bias')
plt.tight_layout()