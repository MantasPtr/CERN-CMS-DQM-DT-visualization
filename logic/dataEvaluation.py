from machineLearning.logic import append_estimation, append_saliency

def process(data: dict):
    data = append_estimation(data)
    data = append_saliency(data)
    return data