import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

IGNORED_VALUES = [-1,-9999,-9999,-9999,-1]

def plot(matricies: dict):
    fig = Figure(figsize=(3,4), dpi=240)
    max_y = len(matricies)
    font = {'size': 5}
    matplotlib.rc('font', **font)
    for index_y, matrix in enumerate(matricies):
        for key, value in matrix.items():
            ax = fig.add_subplot(max_y, 1, index_y+1)
            max_row_length=len(max(value, key=len))
            value = _extend_rows_to_size(value, max_row_length)
            
            cmap = plt.get_cmap("viridis")
            cmap.set_bad("white", 1.)
            masked_array = np.ma.array (value, mask= np.array(value) == IGNORED_VALUES[index_y])
            
            im = ax.imshow(masked_array, cmap=cmap )
            ax.set_xlim(0, max_row_length-1)
            ax.set_ylim(0,len(value))
            ax.set_title(key, loc="right")
            plt.colorbar(im, ax=ax,
                ticks=[np.min(value),
                    np.max(value)])
    plt.subplots_adjust(hspace=20000)
    png_output = io.BytesIO()
    FigureCanvas(fig).print_png(png_output)
    return png_output

def _extend_rows_to_size(matrix, size):
    for idx,row in enumerate(matrix):
        matrix[idx] = np.append(row, [-9999 for _ in range(size-len(row))])
    return matrix

def _to_normal_matrix(data):
    if type(data) is np.ndarray:
        data = data.tolist()
    for i,row in enumerate(data):
        if type(row) is np.ndarray:
            data[i] = row.tolist()
    return data
