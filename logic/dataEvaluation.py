from machineLearning import logic

def process(data: dict):
    data = logic.append_estimation(data)
    data = logic.append_saliency(data)
    return data

def visualize_saliency(record: dict):
    return logic.visualize_saliency_steps(record)
    