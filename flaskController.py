from dataLoading.requestExecutor import getMatrixFromProtectedUrl, getJsonDataFromProtectedUrl
import gui.plotting.plotUtils as plt
from logic import dataFetch, dataLoad
from dataLoading.urlBuilder import validateAndBuildUrl
from flask import Flask, render_template,  make_response, jsonify
import gui.plotting.adrian as aplot
import matplotlib
import json

matplotlib.use('Agg')
app = Flask(__name__, template_folder="gui/templates", static_folder="gui/static")

MAIN_PAGE_TEMPLATE='eval.html'
FETCH_PAGE_TEMPLATE='fetch.html'

@app.route('/')
def default():
    return render_template(MAIN_PAGE_TEMPLATE)

@app.route('/<int:run>')
def evalRun(run):
    return render_template(MAIN_PAGE_TEMPLATE, run = run)


@app.route('/fetch')
def fetch():
    runs = dataFetch.getFetchedRuns()
    return render_template(FETCH_PAGE_TEMPLATE, runs = runs)
   
@app.route('/fetch/<int:run>')
def fetchRun(run):
    responseData = dataFetch.getRunData(run)
    if responseData == None:
        return "Started!"
    responseData.pop("_id", None)
    responseData.pop("save_time", None)
    response = make_response(json.dumps(responseData))
    response.headers['Content-Type'] = 'text/json'
    return response
    
@app.route('/i')
def img():
    labels = getMatrixFromProtectedUrl()
    imgBytes = aplot.plot_occupancy_hitmap(labels, "title", "a.u.")
    response = make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/labels.png")
def get(run, wheel, sector, station):
    wheel = int(wheel) 
    url = validateAndBuildUrl(run, wheel, sector, station)
    labels = getMatrixFromProtectedUrl(url)
    imgBytes = plt.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/labels.json")
def labelsJson(run, wheel, sector, station):
    # returns full json from url since it does not need to parse and format json again
    wheel = int(wheel) 
    url = validateAndBuildUrl(run, wheel, sector, station)
    return getJsonDataFromProtectedUrl(url)

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/data")
def runData(run, wheel, sector, station):
    # returns full json from url since it does not need to parse and format json again
    wheel = int(wheel)
    matrix = dataLoad.getMatrixFromDB(run, wheel, sector, station)
    if (matrix == None):
        response = make_response("Record not found")
        response.status_code = 404
        return response
    else:
        return jsonify(matrix.get("data")[0].get("matrix"))

@app.errorhandler(ValueError)
def handle_invalid_usage(error: ValueError):
    response = jsonify(str(error))
    response.status_code = 400
    return response

@app.errorhandler(Exception)
def handle_other_error(error: Exception):
    print("ERROR: ",error)
    response = jsonify(str(error))
    response.status_code = 500
    return response
