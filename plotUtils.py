import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

def plot(matrix):
   
    _,ax = plt.subplots()
    ax.imshow(matrix)

     
    #ax.set_xticks(np.arange(len(matrix[0]))[::2]+1)
    ax.set_yticks(np.arange(len(matrix))[::2])    
    # ax.set_xticks(np.arange(len(matrix[0]))[::2] - 0.5, minor=True)
    ax.set_yticks(np.arange(len(matrix))[::2] - 0.5, minor=True)
    im = ax.imshow(matrix)
    cbar = ax.figure.colorbar(im,  ax=ax)
    cbar.ax.set_ylabel("colors", rotation=-90, va="bottom")
    plt.draw()
    plt.show()