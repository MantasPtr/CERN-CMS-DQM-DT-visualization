import machineLearning.model as model
import logging


def append_estimation(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return list(map(_append_model_estimation_scores, data))

def append_saliency(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return list(map(_append_model_saliency, data))

def visualize_saliency_steps(data: dict):
    matrix = data.get("data")[0].get("matrix")
    return model.get_saliency_map_steps(matrix)

def _append_model_estimation_scores(result: dict) -> dict:
    matrix = result.get("matrix")
    try:
        result["scores"] = model.get_network_score(matrix)
    except ValueError as v:
        logging.error(result)
        raise v
    return result

def _append_model_saliency(result: dict) -> dict:
    matrix = result.get("matrix")
    try:
        result["saliency"] = model.get_saliency_map(matrix)
    except ValueError as v:
        logging.error(f"{v} Data::{result}")
        raise v
    return result