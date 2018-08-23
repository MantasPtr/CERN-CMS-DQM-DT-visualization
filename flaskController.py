from dataLoading.requestExecutor import getMatrixFromProtectedUrl, getJsonDataFromProtectedUrl
from logic import dataFetch, dataLoad
from flask import Flask, render_template, request, make_response, jsonify, redirect
import gui.plotting.adrian as aplot
import json
from logic.dictBuilder import buildDicts
app = Flask(__name__, template_folder="gui/templates", static_folder="gui/static")

MAIN_PAGE_TEMPLATE='eval.html'
FETCH_PAGE_TEMPLATE='fetch.html'
SCORE_PAGE_TEMPLATE='scores.html'

@app.route('/')
def default():
    return render_template(MAIN_PAGE_TEMPLATE)

@app.route('/<int:run>/')
def evalRun(run):
    return render_template(MAIN_PAGE_TEMPLATE, run = run)

@app.route('/<int:run>/<string:wheel>/<int:sector>/<int:station>/')
def evalRunWithParamsk(run, wheel, sector, station):
    return render_template(MAIN_PAGE_TEMPLATE, run = run, wheel = wheel, sector = sector, station = station)

@app.route('/fetch/')
def fetch():
    runs = dataLoad.getFetchedData()
    return render_template(FETCH_PAGE_TEMPLATE, runs = runs)
   
@app.route('/fetch/<int:run>/')
def fetchRun(run):
    responseData = dataFetch.getDataByIdentifier({"run":run})
    if responseData == None:
        return "Started!"
    responseData.pop("_id", None)
    responseData.pop("save_time", None)
    return jsonify(responseData)

@app.route("/data/<int:run>/<string:wheel>/<int:sector>/<int:station>/i")
def get_adrian(run, wheel, sector, station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    data = dataLoad.getMatrixFromDB(identifier, params)
    imgBytes = aplot.plot_occupancy_hitmap(data.get("data")[0].get("matrix"), "title", "a.u.")
    response = make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/data/<int:run>/<string:wheel>/<int:sector>/<int:station>/", methods = ['GET'])
def runData(run, wheel, sector, station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    data = dataLoad.getMatrixFromDB(identifier, params)
    if (data == None):
        return _make_response("Record not found", 404)
    else:
        #TODO move this check somewhere where it belongs
        if (len(data.get("data")) != 1):
            return _make_response("Request with did not return single result", 500)
        return jsonify(data.get("data")[0])
        

@app.route("/save/", methods = ['POST'])
def score():
    # {'run': '300000', 'wheel': '0', 'sector': '1', 'station': '1', 'layers': ['12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']}
    body = request.get_json()
    badLayers = list(map(int,body["layers"]))
    identifier, params = buildDicts(body["run"], body["wheel"], body["sector"], body["station"])
    return jsonify(dataLoad.updateUserScore(identifier, params, badLayers))

@app.route("/data/<int:runNumber>", methods = ['DELETE'])
def delete(runNumber):
    return jsonify(dataLoad.delete({"run":runNumber}))

@app.route("/scores/")
def scores():
    return jsonify(dataLoad.getScoresData())

@app.route("/net_scores.json")
def net_scores_json():
    return jsonify(dataLoad.get_network_scores())

@app.route("/net_scores/")
def net_scores():
    scores = dataLoad.get_network_scores()
    return render_template(SCORE_PAGE_TEMPLATE, scores = scores)

@app.route("/new_net_scores/")
def new_net_scores():
    scores = dataLoad.get_not_evaluated_network_scores()
    return render_template(SCORE_PAGE_TEMPLATE, scores = scores)

@app.route("/next/")
def get_uncertain_matrix():
    scores = dataLoad.get_not_evaluated_network_scores(1)
    if (len(scores) == 1):
        run = scores[0].get("identifier").get("run")
        wheel = scores[0].get("data").get("params").get("wheel")
        sector = scores[0].get("data").get("params").get("sector")
        station = scores[0].get("data").get("params").get("station")
        return redirect(f"/{run}/{wheel}/{sector}/{station}/")
    return _make_response("query did not return 1 unevaluated result",500)


@app.route("/skip/<int:run>/<string:wheel>/<int:sector>/<int:station>/")
def skip(run,wheel,sector,station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    dataLoad.mark_as_skipped(identifier, params)
    return get_uncertain_matrix()

def _make_response(data, code: int):
    response = make_response(data)
    response.status_code = code
    return response