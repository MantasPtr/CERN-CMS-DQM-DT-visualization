from machineLearning import logic

def process(data: dict):
    data = logic.append_estimation(data)
    data = logic.append_saliency(data)
    return data