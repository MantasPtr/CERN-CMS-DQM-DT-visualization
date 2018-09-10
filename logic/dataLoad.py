"""this module for now delegates all methods to dbController
this is done for easy replacement and usage"""

from database.dbSetup import dbController

def get_matrix_from_DB(identifier: dict, params: dict = {}):
    return dbController.get_single_record_matrix(identifier, params)

def get_fetched_data():
    return dbController.get_all()

def get_scores_data():
    return dbController.get_all_user_scores()

def get_network_scores(limit = 20):
    return dbController.get_all_network_scores(limit)

def get_not_evaluated_network_scores(limit = 20):
    return dbController.get_not_evaluated_network_scores(limit)

def update_user_score(identifier: dict, params: dict, layers: list):
    return dbController.update_user_score(identifier, params, layers)

def mark_as_skipped(identifier: dict, params: dict):
    return dbController.skip_user_score(identifier, params)

def delete(identifier: dict):
    return dbController.delete(identifier)