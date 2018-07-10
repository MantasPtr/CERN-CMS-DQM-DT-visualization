from dataLoading.requestUtils import getLabelsFromProtectedUrl, getDataJsonFromProtectedUrl
import plotting.plotUtils as plt
from dataLoading.urlBuilder import validateAndBuildUrl
from flask import Flask, render_template,  make_response, jsonify
import plotting.adrian as aplot

app = Flask(__name__)
MAIN_PAGE='index.html'
IMAGE_URL='/i'

@app.route('/')
def default():
    return render_template(MAIN_PAGE, title = 111111, imageUrl = IMAGE_URL)

@app.route(IMAGE_URL)
def img():
    labels = getLabelsFromProtectedUrl()
    imgBytes = aplot.plot_occupancy_hitmap(labels, "title", "a.u.")
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<int:wheel>/<int:sector>/<int:station>/labels.png")
def simple(run, wheel, sector, station):
    url = validateAndBuildUrl(run, wheel, sector, station)
    labels = getLabelsFromProtectedUrl(url)
    imgBytes = plt.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<int:wheel>/<int:sector>/<int:station>/labels.json")
def labelsJson(run, wheel, sector, station):
        url = validateAndBuildUrl(run, wheel, sector, station)
        return getDataJsonFromProtectedUrl(url)

@app.errorhandler(ValueError)
def handle_invalid_usage(error: ValueError):
    response = jsonify(str(error))
    response.status_code = 400
    return response
