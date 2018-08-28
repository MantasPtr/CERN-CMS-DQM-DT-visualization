import machineLearning.model as model
import logging

def _append_model_estimation_scores(result: dict) -> dict:
    matrix = result.get("matrix")
    try:
        result["scores"] = model.get_network_score(matrix).tolist()
    except ValueError as v:
        logging.error(result)
        raise v
    return result


def append_estimation(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return [_append_model_estimation_scores(x) for x in data]

def _append_model_saliency(result: dict) -> dict:
    matrix = result.get("matrix")
    try:
        result["saliency"] = model.get_saliency_map(matrix)
    except ValueError as v:
        logging.error(result)
        raise v
    return result

def append_saliency(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return [_append_model_saliency(x) for x in data]
