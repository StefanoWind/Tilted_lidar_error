# -*- coding: utf-8 -*-
"""
Calculate the gemoetrical factor of the error standard deviation for DBS and six-beams
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

#Example 1: regular DBS scan
alpha=np.array([0,0,90,180,270])#[deg] azimuth angles
beta=np.array([90,62,62,62,62])#[deg] elevation angles
scan_type='DBS'

#Example 2: regular six-beam scan
alpha=np.array([0,0,72,144,216,288])#[deg] azimuth angles
beta=np.array([90,45,45,45,45,45])#[deg] elevation angles
scan_type='six-beam'

RS_index={0:[0,0],1:[1,1],2:[2,2],3:[0,1],4:[0,2],5:[1,2]}#Reynolds stress index

vel_names=[r'$\overline{U}$',r'$\overline{V}$',r'$\overline{W}$']#names of velocity components (for plotting)

RS_names=[r'$\overline{U^\prime U^\prime}$',
          r'$\overline{V^\prime V^\prime}$',
          r'$\overline{W^\prime W^\prime}$',
          r'$\overline{U^\prime V^\prime}$',
          r'$\overline{U^\prime W^\prime}$',
          r'$\overline{V^\prime W^\prime}$']#names of Reynolds stresses (for plotting)

#%% Initialization
assert len(alpha)==len(beta), 'Number of azimuths does not much number of elevations'
assert (scan_type=='six-beam' and len(alpha)==6) or scan_type=='DBS', 'Six-beam scan must include six azimuths and elevations'

Nb=len(alpha)

#zeroing
err_stdev_vel=np.zeros(3)
err_stdev_RS=np.zeros(6)

#%% Main

#lidar matrix
A=[]
for a,b in zip(alpha,beta):
    A=utl.vstack(A,np.array([utl.cosd(b)*utl.cosd(a),utl.cosd(b)*utl.sind(a),utl.sind(b)]))

#pseudo-inverse matrix
A_plus=np.matmul(np.linalg.inv(np.matmul(A.T,A)),A.T)

#geometrical factor calculation for mean velocity
for i in range(3):
    for j in range(Nb):
        for k in range(3):
            err_stdev_vel[i]+=(A_plus[i,j]*A[j,k])**2
            
err_stdev_vel=err_stdev_vel**0.5   
    
#geometrical factor calculation for Reynolds stresses
if scan_type=='DBS':
                
    for i in range(6):
        j=RS_index[i][0]
        k=RS_index[i][1]
        for l in range(Nb):
            for m in range(Nb):
                for n in range(3):
                    for p in range(3):
                        err_stdev_RS[i]+=(A_plus[j,l]*A_plus[k,m]*A[l,n]*A[m,p])**2
                        
elif scan_type=='six-beam':
    
    #six-beam matrix for Reynolds stresses
    sa=utl.sind(alpha)
    ca=utl.cosd(alpha)
    sb=utl.sind(beta)
    cb=utl.cosd(beta)
    M=np.zeros((Nb,6))
    M[:,0]=cb**2*ca**2
    M[:,1]=cb**2*sa**2
    M[:,2]=sb**2
    M[:,3]=2*cb**2*ca*sa
    M[:,4]=2*cb*sb*ca
    M[:,5]=2*cb*sb*sa
    
    for i in range(6):
        for j in range(Nb):
            for k in range(3):
                for l in range(3):
                    err_stdev_RS[i]+=(M[i,j]*A[j,k]*A[j,l])**2
else:
    raise ValueError('Unknown scan type. It must be DBS or six-beam.')    
        
err_stdev_RS=err_stdev_RS**0.5 
    
#%% Plots
plt.figure(figsize=(18,6))

#draw scan geometry
ax=plt.subplot(1,3,1,projection='3d')
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

plt.subplot(1,3,2)
plt.bar(vel_names,err_stdev_vel,color='k')
plt.ylabel('Geometrical error factor')
plt.grid()
plt.title('Geometrical error st.dev. factors \n for mean velocity')

plt.subplot(1,3,3)
plt.bar(RS_names,err_stdev_RS,color='k')
plt.ylabel('Geometrical error factor')
plt.grid()
plt.title('Geometrical error st.dev. factors \n for Reynolds stresses')

plt.tight_layout()