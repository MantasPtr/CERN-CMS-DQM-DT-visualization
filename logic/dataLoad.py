"""this module mostly delegates all methods to dbController
this is done for easy replacement and usage"""

from database.dbSetup import get_db_controller

def get_matrix_from_DB(identifier: dict, params: dict = {}):
    return get_db_controller().get_single_record_matrix(identifier, params)

def get_fetched_data():
    return get_db_controller().get_all()

def get_scores_data():
    return get_db_controller().get_all_user_scores()

def get_network_scores(limit = 20, page = 1):
    skip_count = (page-1) * limit
    return get_db_controller().get_all_network_scores(limit, skip=skip_count)

def get_one_record(identifier: dict):
    return get_db_controller().get_one(identifier)

def get_not_evaluated_network_scores(limit = 20, page = 1):
    skip_count = (page-1) * limit
    return get_db_controller().get_not_evaluated_network_scores(limit, skip=skip_count)

def update_user_score(identifier: dict, params: dict, layers: list):
    return get_db_controller().update_user_score(identifier, params, layers)

def mark_as_skipped(identifier: dict, params: dict):
    return get_db_controller().skip_user_score(identifier, params)

def delete(identifier: dict):
    return get_db_controller().delete(identifier)
