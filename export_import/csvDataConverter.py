from typing import Iterable
import pandas
import itertools
import collections
import warnings
#    database record format:
#
#    {
#       data: 
#           evaluation:
#               bad_layers: [<int?>]
#               eval_time:	<datatime>
#               skipped:    <boolean>
#           params:
#               sector:     <int>
#               station:    <int>
#               wheel:      <int>,
#       identifier:
#           run: <int>
#    }

#    file format:
#       [<wheel>,<station>,<sector>,<run>,<layer>,<good>]

def from_record_to_row(data: Iterable):
    for record in data:
        run = record["identifier"]["run"]
        _params = record["data"]["params"]
        sector = _params["sector"] 
        station =_params["station"] 
        wheel = _params["wheel"]
        bad_layers = record["data"]["evaluation"]["bad_layers"]
        for i in range(1,13):
            yield [wheel, station, sector, run, i, int(i not in bad_layers)]

def from_row_to_record(data: Iterable):
    """returns list[identifier][params] = score"""
    identifier_lists = collections.defaultdict(lambda: collections.defaultdict(list))
    for record in data:
        if (len(record) != 6):
            warnings.warn(f"Wrong csv line structure: {record}. Expected array of 6elements")
            continue
        identifier = ("run", int(record[3]))   # tuple since dict is not hashable 
        params = (("wheel"  , int(record[0])),
                  ("station", int(record[1])),
                  ("sector" , int(record[2]))) # tuple since dict is not hashable 
        layer_score = (record[4], record[5])
        identifier_lists[identifier][params].append(layer_score)
    for run, data in identifier_lists.items():
        for params, value_tuples in data.items():
            value_tuples.sort(key = lambda x:x[0])
            identifier_lists[run][params]= list(map(lambda x:abs(int(x[1])-1), value_tuples))
    return identifier_lists