import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

def getImageBytes(matrix):
    __plot(matrix)
    return __getPlotBytes()
    
def drawPlot(matrix):
    __plot(matrix)
    __showPlot()

def __plot(matrix):
    _,ax = plt.subplots()
    #ax.set_xticks(np.arange(len(matrix[0]))[::2]+1)
    ax.set_yticks(np.arange(len(matrix))[::2])    
    # ax.set_xticks(np.arange(len(matrix[0]))[::2] - 0.5, minor=True)
    ax.set_yticks(np.arange(len(matrix))[::2] - 0.5, minor=True)
    im = ax.imshow(matrix)
    cbar = ax.figure.colorbar(im,  ax=ax)
    cbar.ax.set_ylabel("colors", rotation=-90, va="bottom")
    
def __getPlotBytes() ->  io.BytesIO: 
    imgStream = io.BytesIO()
    plt.savefig(imgStream, format="PNG")
    imgStream.seek(0) # TODO test if needed
    return imgStream

def __showPlot():
    plt.draw()
    plt.show()