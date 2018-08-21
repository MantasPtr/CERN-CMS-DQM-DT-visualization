# https://github.com/AdrianAlan/DT-Digi-Occupancy/blob/master/notebooks/local-approach.ipynb
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_occupancy_hitmap(data, title, unit):
    """Visualizes occupancy hitmap"""
    fig, ax = plt.subplots()
    
    ax = plt.gca()
    
    ax.set_xlim([-2, len(data[0])+1])
    ax.set_yticklabels(["1", "5", "9"])
    ax.set_yticks([0, 4, 8])
    ax.set_ylim([13,-2])

    plt.xlabel("Channel", horizontalalignment='right', x=1.0)
    plt.ylabel("Layer", horizontalalignment='right', y=1.0)
    
    np_data = np.array(data)
    masked_array = np.ma.array (np_data, mask=np_data < 0)
    # cmap = copy(plt.cm.viridis)
    #cmap.set_bad("white", 1.)
    im = ax.imshow(masked_array, interpolation="nearest")#, cmap=cmap)  
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    if unit == "a.u.":
        form = '%.2f'
    else:
        form = '%.0f'
    
    plt.colorbar(im,
                 cax=cax,
                 format=form,
                 ticks=[np.min(np.nan_to_num(data)),
                        np.max(np.nan_to_num(data))])
    
    plt.title(title, loc="right")   
    
    ax.text(1.1, 0.75, unit, rotation=90,
        verticalalignment="top", horizontalalignment="right",
        transform=ax.transAxes, color="black", fontsize=16)
    
    ax.text(0, 1.16, "CMS", weight='bold',
        verticalalignment="top", horizontalalignment="left",
        transform=ax.transAxes, color="black", fontsize=18)
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    return png_output