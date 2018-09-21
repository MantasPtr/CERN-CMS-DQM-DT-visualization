
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, request, make_response, Response, jsonify, redirect
app = Flask(__name__, template_folder="gui/templates", static_folder="gui/static")

from logic import dataFetch, dataLoad
import gui.plotting.adrian as a_plot
import json
from errors.errors import ValidationError
from logic.dbIdentifierBuilder import buildDicts
from gui.plotting import mutliplot
from utils import numpyUtils
MAIN_PAGE_TEMPLATE='eval.html'
FETCH_PAGE_TEMPLATE='fetch.html'
GENERIC_SCORE_PAGE_TEMPLATE='generic_scores.html'

@app.route('/')
@app.route('/eval/')
def default():
    return render_template(MAIN_PAGE_TEMPLATE)

@app.route('/eval/<int:run>/')
def evalRun(run):
    return render_template(MAIN_PAGE_TEMPLATE, run = run)

@app.route('/eval/<int:run>/<string:wheel>/<int:sector>/<int:station>/')
def evalRunWithParam(run, wheel, sector, station):
    return render_template(MAIN_PAGE_TEMPLATE, run = run, wheel = wheel, sector = sector, station = station)

@app.route('/fetch/')
def fetch():
    runs = dataLoad.get_fetched_data()
    return render_template(FETCH_PAGE_TEMPLATE, runs = runs)
   
@app.route('/fetch/<int:run>/', methods = ['POST'])
def fetchRun(run):
    identifier_dict = {"run":run}
    responseData = dataFetch.fetch_data_by_identifier(identifier_dict)
    if responseData == None:
        return "OK"
    else:
        return _make_response(f"Specified record with identifier {identifier_dict} already exits in database", 409)

@app.route("/eval/<int:run>/<string:wheel>/<int:sector>/<int:station>/i")
def get_adrian(run, wheel, sector, station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    data = dataLoad.get_matrix_from_DB(identifier, params)
    imgBytes = a_plot.plot_occupancy_hitmap(data.get("data")[0].get("matrix"), "title", "a.u.")
    response = make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/data/<int:run>/<string:wheel>/<int:sector>/<int:station>/", methods = ['GET'])
def runData(run, wheel, sector, station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    run_data = dataLoad.get_matrix_from_DB(identifier, params)
    if (run_data == None):
        return _make_response("Record not found", 404)
    else:
        data = run_data.get("data")
        if data == None:
            return _make_response(f"Record does not contain any data", 404)
        if len(data) != 1:
            return _make_response(f"Request with did not return single result. Expected: 1, actual: {len(data.get('data'))}", 500)
        return jsonify(data[0])
        

@app.route("/eval/save_user_scores/", methods = ['PATCH'])
def score():
    # body: { 
    #   'run': '300000',
    #   'wheel': '0', 
    #   'sector': '1',
    #   'station': '1',
    #   'layers': ['12', '10', '9', '7', '6', '5', '2', '1']
    # }
    body = request.get_json()
    badLayers = list(map(int,body["layers"]))
    identifier, params = buildDicts(body["run"], body["wheel"], body["sector"], body["station"])
    return jsonify(dataLoad.update_user_score(identifier, params, badLayers))

@app.route("/data/<int:runNumber>", methods = ['DELETE'])
def delete(runNumber):
    return jsonify(dataLoad.delete({"run":runNumber}))

@app.route("/data/user_scores.json/")
def scores():
    return jsonify(dataLoad.get_scores_data())

@app.route("/data/net_scores.json/")
def net_scores_json():
    return jsonify(dataLoad.get_network_scores())

@app.route("/data/net_scores/")
def net_scores():
    scores = dataLoad.get_network_scores()
    lines = []
    for score in scores:
        lines.append({
             "Identifier": {"value": score["identifier"]      , "format": False },
             "Params":     {"value": score["data"]["params"]  , "format": False },
             "Scores":     {"value": score["data"]["scores"]  , "format": True  },
             "Certainty":  {"value": score["rating"]          , "format": True  },
             "User score": {"value": _format_user_score(score), "format": False },
        })    
    return _render_generic_statistics_template(lines)

def _format_user_score(score):
    if score["data"].get("evaluation", False):
        if score["data"]["evaluation"].get("skipped",False):
            return "Skipped"
        else:
            return score["data"]["evaluation"]["bad_layers"]
    else:
        return "-"
    return

@app.route("/data/new_net_scores/")
def new_net_scores():
    scores = dataLoad.get_not_evaluated_network_scores()
    lines = []
    for score in scores:
        lines.append({
             "Identifier": {"value": score["identifier"]    , "format": False },
             "Params":     {"value": score["data"]["params"], "format": False },
             "Scores":     {"value": score["data"]["scores"], "format": True },
             "Certainty":  {"value": score["rating"]        , "format": True },
             })     
    return _render_generic_statistics_template(lines)


def _render_generic_statistics_template(values):
    keys = values[0] if values else []  
    return render_template(GENERIC_SCORE_PAGE_TEMPLATE, keys = keys, values = values)



@app.route("/eval/next/")
def get_uncertain_matrix():
    scores = dataLoad.get_not_evaluated_network_scores(1)
    if (len(scores) == 1):
        run = scores[0].get("identifier").get("run")
        wheel = scores[0].get("data").get("params").get("wheel")
        sector = scores[0].get("data").get("params").get("sector")
        station = scores[0].get("data").get("params").get("station")
        return redirect(f"/eval/{run}/{wheel}/{sector}/{station}/")
    return _make_response(f"Query did not return 1 unevaluated result, It returned: {len(scores)}", 500)


@app.route("/eval/skip/<int:run>/<string:wheel>/<int:sector>/<int:station>/")
def skip(run,wheel,sector,station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    dataLoad.mark_as_skipped(identifier, params)
    return get_uncertain_matrix()

@app.route("/visualize/<int:run>/<string:wheel>/<int:sector>/<int:station>/")
def visualize(run,wheel,sector,station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    data = dataFetch.visualize(identifier, params)
    imgBytes = mutliplot.plot(data)
    response = make_response(imgBytes.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/visualize/<int:run>/<string:wheel>/<int:sector>/<int:station>/json")
def visualize_raw(run,wheel,sector,station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    data = dataFetch.visualize(identifier, params)
    return jsonify([{k:numpyUtils.to_python_matrix(v)} for value in data for k,v in value.items() ])

@app.route('/data/<int:run>/layers.json')
def record_lines(run):
    record = dataLoad.get_one_record({"run":run})
    raw_data = record["data"]
    data = list(_generate_json_lines(raw_data, run))
    return Response(json.dumps(data), 
            mimetype='application/json',
            headers={"Content-Disposition":f"attachment;filename={run}.json"})

def _generate_json_lines(raw_data: list, run: int):
    for combination in raw_data:
        wheel = combination["params"]["wheel"]
        sector = combination["params"]["sector"]
        station = combination["params"]["station"]
        for layer, row in enumerate(combination["matrix"], start=1):
            row = numpyUtils.remove_negatives(row)
            if len(row) == 0:
                continue
            line = {
                "wheel": str(wheel),
                "sector": str(sector),
                "layer": str(layer),
                "run": str(run),
                "contect": str(row),
                "station": str(station),
                "lumi": "-1",
            }
            yield line

@app.route('/data/reevaluate/', methods = ['POST'])
def reevaluate():
    dataFetch.reevaluate_all()
    return "OK"

def _make_response(data, code: int):
    response = make_response(data)
    response.status_code = code
    return response

@app.errorhandler(ValidationError)
def handle_invalid_usage(error: ValidationError):
    return _make_response(jsonify(str(error)), 400)

@app.errorhandler(404)
def page_not_found(e):
    return "Page does not exist! Please check the url!", 404