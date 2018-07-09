from dataLoading.requestUtils import getLabelsFromProtectedUrl
import plotUtils
from dataLoading.urlBuilder import validateAndBuildUrl
from flask import Flask, redirect, make_response
import plotting
app = Flask(__name__)

@app.route('/')
def default():
    labels = getLabelsFromProtectedUrl()
    imgBytes = plotUtils.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/a')
def a():
    labels = getLabelsFromProtectedUrl()
    imgBytes = plotting.plot_occupancy_hitmap(labels, "title", "a.u.")
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<int:wheel>/<int:sector>/<int:station>/labels.png")
def simple(run, wheel, sector, station):
    url = validateAndBuildUrl(run, wheel, sector, station)
    labels = getLabelsFromProtectedUrl(url)
    imgBytes = plotUtils.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response