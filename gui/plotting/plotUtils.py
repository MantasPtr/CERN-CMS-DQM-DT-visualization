import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def drawPlot(matrix):
    __plot(matrix)
    __showPlot()

def __plot(matrix):
    fig ,ax = plt.subplots()
    #ax.set_xticks(np.arange(len(matrix[0]))[::2]+1)
    ax.set_yticks(np.arange(len(matrix))[::2])    
    # ax.set_xticks(np.arange(len(matrix[0]))[::2] - 0.5, minor=True)
    ax.set_yticks(np.arange(len(matrix))[::2] - 0.5, minor=True)
    im = ax.imshow(matrix)
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("colors", rotation=-90, va="bottom")

def getImageBytes(matrix):
    fig=Figure()
    ax=fig.add_subplot(111)
    ax.imshow(matrix)
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    return png_output

def __getPlotBytes() ->  io.BytesIO: 
    imgStream = io.BytesIO()
    plt.savefig(imgStream, format="PNG")
    return imgStream

def __showPlot():
    plt.draw()
    plt.show()