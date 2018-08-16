from dataLoading.requestExecutor import getMatrixFromProtectedUrl, getJsonDataFromProtectedUrl
import gui.plotting.plotUtils as plt
from logic import dataFetch, dataLoad
from dataLoading.urlBuilder import buildUrlFromContainer
from flask import Flask, render_template, request, make_response, jsonify
import gui.plotting.adrian as aplot
import matplotlib
import json
from logic.runContainer import RunContainer

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
    runs = dataFetch.getFetchedData()
    return render_template(FETCH_PAGE_TEMPLATE, runs = runs)
   
@app.route('/fetch/<int:run>')
def fetchRun(run):
    responseData = dataFetch.getDataByIdentifier({"run":run})
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
    container = RunContainer(run, int(wheel) , sector, station)
    url = buildUrlFromContainer(container)
    labels = getMatrixFromProtectedUrl(url)
    imgBytes = plt.getImageBytes(labels)
    response=make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/labels.json")
def labelsJson(run, wheel, sector, station):
    # returns full json from url since it does not need to parse and format json again
    runContainer = RunContainer(run, int(wheel), sector, station)
    url = buildUrlFromContainer(runContainer)
    return getJsonDataFromProtectedUrl(url)

@app.route("/<int:run>/<string:wheel>/<int:sector>/<int:station>/", methods = ['GET'])
def runData(run, wheel, sector, station):
    runContainer = RunContainer(run, int(wheel), sector, station)
    identifier, params  = runContainer.toDicts()
    matrix = dataLoad.getMatrixFromDB(identifier, params)
    if (matrix == None):
        response = make_response("Record not found")
        response.status_code = 404
        return response
    else:
        return jsonify(matrix.get("data")[0].get("matrix"))

@app.route("/save/", methods = ['POST'])
def score():
    # {'run': '300000', 'wheel': '0', 'sector': '1', 'station': '1', 'layers': ['12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']}
    values = request.get_json()
    runContainer = RunContainer(int(values["run"]), int(values["wheel"]), int(values["sector"]), int(values["station"]))
    badLayers = values["layers"]
    identifier, params  = runContainer.toDicts()
    return jsonify(dataLoad.updateUserScore(identifier, params, badLayers))

@app.route("/<int:runNumber>", methods = ['DELETE'])
def delete(runNumber):
    return jsonify(dataLoad.delete({"run":runNumber}))
