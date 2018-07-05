from requestUtils import getLabelsFromProtectedUrl
import plotUtils
import base64
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def default():
    labels = getLabelsFromProtectedUrl()
    imgBytes = plotUtils.getImageBytes(labels)
    plot_url = base64.b64encode(imgBytes.getvalue()).decode()
    return '<img src="data:image/png;base64,{}">'.format(plot_url)
