from keras import backend as K
from keras import activations
import numpy as np

# https://github.com/experiencor/deep-viz-keras/blob/master/visual_backprop.py
class GradientSaliency():

    def __init__(self, model, output_index = 0):
        # Define the function to compute the gradient
        model.layers[-1].activation = activations.linear
        model = reload_model(model)
        input_tensors = [model.input]
        gradients = model.optimizer.get_gradients(model.output[0][output_index], model.input)
        self.compute_gradients = K.function(inputs = input_tensors, outputs = gradients)

    def get_gradients(self, input_image):# Execute the function to compute the gradient
        return list(map(self._get_smoothed_mask, input_image))
        
    def _compute_mask_for_line(self, line: list) -> np.ndarray:
        if len(line) == 0:
            return np.array([])
        line =  np.expand_dims(line, axis=0)
        return self.compute_gradients([line])[0][0]

    def _get_smoothed_mask(self, input_image, stdev_spread=.2, nsamples=50):
        if len(input_image) == 0:
            return np.array([])
        stdev = stdev_spread * (np.max(input_image) - np.min(input_image))

        total_gradients = np.zeros_like(input_image, dtype = np.float64)
        for i in range(nsamples):
            noise = np.random.normal(0, stdev, input_image.shape)
            x_value_plus_noise = input_image + noise

            total_gradients += self._compute_mask_for_line(x_value_plus_noise)

        return total_gradients / nsamples
    
    
def reload_model(model):
    import os
    import tempfile
    from keras.models import load_model
    model_path = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + '.h5')
    try:
        model.save(model_path)
        model = load_model(model_path)
    finally:
        os.remove(model_path)
    return model