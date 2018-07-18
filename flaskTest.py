from dataLoading.requestUtils import getLabelsFromProtectedUrl, getDataJsonFromProtectedUrl
import plotting.plotUtils as plt
from dataLoading.urlBuilder import validateAndBuildUrl
from flask import Flask, render_template,  make_response, jsonify
import plotting.adrian as aplot
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
MAIN_PAGE_TEMPLATE='index.html'
FETCH_PAGE_TEMPLATE='fetch.html'
IMAGE_URL='/i'

@app.route('/')
def default():
    return render_template(MAIN_PAGE_TEMPLATE, title = 317111, imageUrl = IMAGE_URL)

@app.route('/')
def fetch():
    return render_template(FETCH_PAGE_TEMPLATE)

@app.route(IMAGE_URL)
def img():
    labels = getLabelsFromProtectedUrl()
    imgBytes = aplot.plot_occupancy_hitmap(labels, "title", "a.u.")
    response = make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/labels.png")
def get(run, wheel, sector, station):
    wheel = int(wheel) 
    url = validateAndBuildUrl(run, wheel, sector, station)
    labels = getLabelsFromProtectedUrl(url)
    imgBytes = plt.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/labels.json")
def labelsJson(run, wheel, sector, station):
    # returns full json from url since it does not need to parse and format json again
    wheel = int(wheel) 
    url = validateAndBuildUrl(run, wheel, sector, station)
    return getDataJsonFromProtectedUrl(url)

@app.errorhandler(ValueError)
def handle_invalid_usage(error: ValueError):
    response = jsonify(str(error))
    response.status_code = 400
    return response

