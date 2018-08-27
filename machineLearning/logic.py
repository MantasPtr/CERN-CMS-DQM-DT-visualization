import machineLearning.model as model

def _append_model_estimation_scores(result: dict) -> dict:
    matrix = result.get("matrix")
    result["scores"] = model.get_network_score(matrix).tolist()
    return result


def append_estimation(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return [_append_model_estimation_scores(x) for x in data]

def _append_model_saliency(result: dict) -> dict:
    matrix = result.get("matrix")
    result["saliency"] = model.get_saliency_map(matrix)
    return result

def append_saliency(data: list) -> list:
    """Appends scores to field to dict based on matrix field"""
    return [_append_model_saliency(x) for x in data]
