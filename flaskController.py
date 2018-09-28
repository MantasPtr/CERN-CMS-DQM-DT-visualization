
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from flask import Flask, render_template, request, make_response, Response, jsonify, redirect, url_for
app = Flask(__name__, template_folder="gui/templates", static_folder="gui/static")

from logic import dataFetch, dataLoad
import json
from errors.errors import ValidationError
from logic.dbIdentifierBuilder import buildDicts
from utils import numpyUtils
from gui.guiUtils import Pagination
MAIN_PAGE_TEMPLATE='eval.html'
FETCH_PAGE_TEMPLATE='fetch.html'
GENERIC_SCORE_PAGE_TEMPLATE='generic_scores.html'
PAGE_SIZE = 20

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

@app.route('/manage/')
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
            return _make_response(f"Request with did not return single result. Expected: 1, actual: {len(data)}", 500)
        return jsonify(data[0])
        

@app.route("/eval/save_user_scores/", methods = ['PATCH'])
def score():
    # body: { 
    #   'run': '300000',
    #   'wheel': '0', 
    #   'sector': '1',
    #   'station': '1',
    #   'layers': ['0', '1, '0', '0','0', '1, '0', '0', '0', '1' , '1', '1']
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

@app.route("/data/net_scores/", defaults={"page":1})
@app.route('/data/net_scores/page/<int:page>')
def net_scores(page):
    records = dataLoad.get_network_scores(limit=PAGE_SIZE, page=page)
    count = records[0]["count"]
    lines = []      
    for record in records:
        score = record["result"] 
        lines.append({
             "Identifier": {"value": score["identifier"]      , "format": False },
             "Params":     {"value": score["data"]["params"]  , "format": False },
             "Scores":     {"value": score["data"]["scores"]  , "format": True  },
             "Certainty":  {"value": score["rating"]          , "format": True  },
             "User score": {"value": _format_user_score(score), "format": False },
        })
        
    pagination = Pagination(page, per_page=PAGE_SIZE, total_count= count)
    return _render_generic_statistics_template(lines, pagination)

@app.route("/data/contamination/", defaults={"page":1})
@app.route('/data/contamination/page/<int:page>')
def contamination(page):
    records = dataLoad.get_contamination_scores(limit=PAGE_SIZE, page=page)
    count = records[0]["count"]
    lines = []      
    for record in records:
        score = record["result"] 
        lines.append({
             "Identifier":    {"value": score["identifier"]      , "format": False },
             "Params":        {"value": score["data"]["params"]  , "format": False },
             "Scores":        {"value": score["data"]["scores"]  , "format": True  },
             "User score":    {"value": _format_user_score(score), "format": False },
             "Contamination": {"value": score["rating"]          , "format": True  },
        })
        
    pagination = Pagination(page, per_page=PAGE_SIZE, total_count= count)
    return _render_generic_statistics_template(lines, pagination)


def _format_user_score(score):
    if "evaluation" in score["data"]:
        if "skipped" in score["data"]["evaluation"]:
            return "Skipped"
        else:
            return score["data"]["evaluation"]["bad_layers"]
    else:
        return "-"

@app.route("/data/new_net_scores/", defaults={"page":1})
@app.route('/data/new_net_scores/page/<int:page>')
def new_net_scores(page):
    records = dataLoad.get_not_evaluated_network_scores(page=page)
    count = records[0]["count"]
    lines = []
    for record in records:
        score = record["result"] 
        lines.append({
             "Identifier": {"value": score["identifier"]    , "format": False },
             "Params":     {"value": score["data"]["params"], "format": False },
             "Scores":     {"value": score["data"]["scores"], "format": True },
             "Certainty":  {"value": score["rating"]        , "format": True },
             })     

    pagination = Pagination(page, per_page=PAGE_SIZE, total_count= count)
    return _render_generic_statistics_template(lines, pagination)


def _render_generic_statistics_template(values, pagination = None):
    keys = values[0] if values else []  
    return render_template(GENERIC_SCORE_PAGE_TEMPLATE, keys = keys, values = values, pagination = pagination)

@app.route("/eval/next/")
def get_uncertain_matrix():
    container = dataLoad.get_not_evaluated_network_scores(1)
    if (len(container) == 1):
        scores = container[0]["result"]
        run = scores["identifier"]["run"]
        wheel = scores["data"]["params"]["wheel"]
        sector = scores["data"]["params"]["sector"]
        station = scores["data"]["params"]["station"]
        return redirect(f"/eval/{run}/{wheel}/{sector}/{station}/")
    return _make_response(f"Query did not return 1 unevaluated result, It returned: {len(scores)}", 500)


@app.route("/eval/skip/<int:run>/<string:wheel>/<int:sector>/<int:station>/")
def skip(run,wheel,sector,station):
    identifier, params  = buildDicts(run, wheel, sector, station)
    dataLoad.mark_as_skipped(identifier, params)
    return get_uncertain_matrix()

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

def flask_pagination_url_formater(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = flask_pagination_url_formater

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8080)