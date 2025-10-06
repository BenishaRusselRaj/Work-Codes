# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:46:56 2023

@author: IITM
"""
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from matplotlib import cm
import matplotlib
import numpy as np

df=pd.read_csv("D:\\Benisha\\2.8kWh_4D_plot_data.csv")

p_index=['1_2','3_4','5_6']

x_label='Temperature'
y_label='SoH'
z_label='Voltage'
c_label='Current'
cmap_name='winter'



# x=df['Temperature_1_2'].dropna().values
# y=df['SoH_1_2'].dropna().values
# z=df['Voltage_1_2'].dropna().values
# c1=df['Current_1_2'].dropna().values

#%%
# np.outer(z.T,z)
# np.meshgrid()

# ax=fig.gca(projection='3d')
# img=ax.scatter(x,y,z,c=c1)
#%%
for i in p_index:
    x=df[x_label+'_'+i]
    y=df[y_label+'_'+i]
    z=df[z_label+'_'+i]
    c1=df['Current_'+i]
    
    X,Y,Z,C=np.meshgrid(x,y,z,c1)
    
    # fig=plt.figure()
    # ax=plt.subplot(111,projection='3d')
    # img=ax.scatter(x,y,z,c=c1,cmap='winter')
    # ax.set_xlabel(x_label,fontweight='bold')
    # ax.set_ylabel(y_label,fontweight='bold')
    # ax.set_zlabel(z_label,fontweight='bold')
    # # fig.colorbar(img) ,shrink=0.5,aspect=5
    # cbar=plt.colorbar(img)
    # cbar.ax.get_yaxis().labelpad=17
    # cbar.ax.set_ylabel(c_label,rotation=270,fontweight='bold')
    # plt.show()
    
    fig=plt.figure()
    ax=plt.subplot(111,projection='3d')
    img=ax.scatter(X,Y,Z,c=C,cmap='winter')
    ax.set_xlabel(x_label,fontweight='bold')
    ax.set_ylabel(y_label,fontweight='bold')
    ax.set_zlabel(z_label,fontweight='bold')
    # fig.colorbar(img) ,shrink=0.5,aspect=5
    cbar=plt.colorbar(img)
    cbar.ax.get_yaxis().labelpad=17
    cbar.ax.set_ylabel(c_label,rotation=270,fontweight='bold')
    plt.title('Packs_'+i,fontweight='bold',size=13)
    plt.show()
    
    del X,Y,Z,C


#%%

# fig=plt.figure()
# ax=plt.subplot(111,projection='3d')
# img=ax.scatter(X,Y,Z,c=c1,cmap='winter')
# ax.set_xlabel(x_label,fontweight='bold')
# ax.set_ylabel(y_label,fontweight='bold')
# ax.set_zlabel(z_label,fontweight='bold')
# # fig.colorbar(img) ,shrink=0.5,aspect=5
# cbar=plt.colorbar(img)
# cbar.ax.get_yaxis().labelpad=17
# cbar.ax.set_ylabel(c_label,rotation=270,fontweight='bold')
# plt.show()
#%%
# fig=plt.figure()
# ax=fig.gca(projection='3d')
# # img=ax.scatter(x,y,z,c=c1)

# x1,y1=np.meshgrid(x,y)
# z1,C1=np.meshgrid(z,c1)
# # C1=np.meshgrid(c1,c1)[1]

# norm=matplotlib.colors.Normalize(vmin=C1.min().min(), vmax=C1.max().max())
# surf=ax.plot_surface(x,y,z1,facecolors=cm.winter(norm(C1)))


# ax.set_xlabel('Temperature',fontweight='bold')
# ax.set_ylabel('SoH',fontweight='bold')
# ax.set_zlabel('Voltage',fontweight='bold')

# m = cm.ScalarMappable(cmap=plt.cm.winter, norm=norm)
# m.set_array([])
# cbar=plt.colorbar(m)


# # fig.colorbar(surf,ax=ax) #,shrink=0.5,aspect=5
# cbar.ax.get_yaxis().labelpad=17
# cbar.ax.set_ylabel(c_label,rotation=270,fontweight='bold')
# plt.show()
#%%

# triangles=mtri.Triangulation(x,y).triangles
# colors=np.mean([c1[triangles[:,0]], c1[triangles[:,1]], c1[triangles[:,2]]], axis=0)

# # fig=plt.figure()
# # ax=fig.gca(projection='3d')
# triangles_1=mtri.Triangulation(x, y, triangles)
# surf=ax.plot_trisurf(triangles_1,z,cmap=cmap_name,shade=False, linewidth=0.2)
# surf.set_array(colors)
# surf.autoscale()

# cbar=plt.colorbar(surf,shrink=0.5,aspect=5)
# cbar.ax.get_yaxis().labelpad=15
# cbar.ax.set_ylabel(c_label,rotation=270)

# ax.set_xlabel(x_label)
# ax.set_ylabel(y_label)
# ax.set_zlabel(z_label)

# plt.title('Life Extending Algorithm C-rates as a function of Temperature, SoH and Voltage')

# plt.show()

# #%%
# import matplotlib
# from scipy.interpolate import griddata

# # X-Y are transformed into 2D grids. It's like a form of interpolation
# x2, y2 = np.meshgrid(x, y);

# # Interpolation of Z: old X-Y to the new X-Y grid.
# # Note: Sometimes values ​​can be < z.min and so it may be better to set 
# # the values too low to the true minimum value.
# z2 = griddata( (x, y), z, (x2, y2), method='cubic', fill_value = 0);
# z2[z2 < z.min()] = z.min();

# # Interpolation of C: old X-Y on the new X-Y grid (as we did for Z)
# # The only problem is the fact that the interpolation of C does not take
# # into account Z and that, consequently, the representation is less 
# # valid compared to the previous solutions.
# c2 = griddata( (x, y), c1, (x2, y2), method='cubic', fill_value = 0);
# c2[c2 < c1.min()] = c1.min(); 

# #--------
# color_dimension = c2; # It must be in 2D - as for "X, Y, Z".
# minn, maxx = color_dimension.min(), color_dimension.max();
# norm = matplotlib.colors.Normalize(minn, maxx);
# m = plt.cm.ScalarMappable(norm=norm, cmap = cmap_name);
# m.set_array([]);
# fcolors = m.to_rgba(color_dimension);

# # At this time, X-Y-Z-C are all 2D and we can use "plot_surface".
# fig=plt.figure()
# ax=fig.gca(projection='3d')
# img=ax.scatter(x,y,z,c=c1)

# surf = ax.plot_surface(x2, y2, z2, facecolors = fcolors, linewidth=0, rstride=1, cstride=1,
#                         antialiased=False);
# cbar = fig.colorbar(m, shrink=0.5, aspect=5);
# cbar.ax.get_yaxis().labelpad = 15; 
# cbar.ax.set_ylabel(c_label, rotation = 270);
# ax.set_xlabel(x_label)
# ax.set_ylabel(y_label)
# ax.set_zlabel(z_label)
# plt.show();