from keras import backend as K
import numpy as np

class GradientSaliency():

    def __init__(self, model, output_index = 1):
        # Define the function to compute the gradient
        input_tensors = [model.input]
        gradients = model.optimizer.get_gradients(model.output[0][output_index], model.input)
        self.compute_gradients = K.function(inputs = input_tensors, outputs = gradients)

    def get_gradients(self, input_image):# Execute the function to compute the gradient
        return list(map(self._compute_mask_for_line, input_image))
        
    def _compute_mask_for_line(self, line: list) -> np.ndarray:
        if len(line) == 0:
            return []
        return self.compute_gradients([[line]])[0][0]
        
# # https://github.com/experiencor/deep-viz-keras/blob/master/visual_backprop.py
# class VisualBackprop():
#     def __init__(self, model, output_index = 1):
#         inps = [model.input]           # input placeholder
#         outs = [layer.output for layer in model.layers]    # all layer outputs
#         self.forward_pass = K.function(inps, outs)         # evaluation function
        
#         self.model = model

#     def get_gradients(self, input_image):
#         visual_bpr = None
#         ## test
#         layer_outs = self.forward_pass([[input_image, 0]])

#         for i in range(len(self.model.layers) - 1, -1, -1):
#             if 'Conv1D' in str(type(self.model.layers[i])):  #CHANGED HERE
#                 layer = np.mean(layer_outs[i], axis = 2, keepdims = True)  #CHANGED HERE
#                 layer = layer - np.min(layer)
#                 layer = layer / (np.max(layer) - np.min(layer) + 1e-6)

#                 if visual_bpr is not None:
#                     if visual_bpr.shape != layer.shape:
#                         visual_bpr = self._deconv(visual_bpr)
#                     visual_bpr = visual_bpr * layer
#                 else:
#                     visual_bpr = layer

                    
#         return visual_bpr[0]
    
#     def _deconv(self, feature_map):
#         x = Input(shape = (None, None, 1))
#         y = Conv2DTranspose(filters = 1, 
#                             kernel_size = (3, 3), 
#                             strides = (2, 2), 
#                             padding = 'same', 
#                             kernel_initializer = Ones(), 
#                             bias_initializer = Zeros())(x)

#         deconv_model = Model(inputs=[x], outputs=[y])

#         inps = [deconv_model.input]   # input placeholder                                
#         outs = [deconv_model.layers[-1].output]           # output placeholder
#         deconv_func = K.function(inps, outs)              # evaluation function
        
#         return deconv_func([feature_map, 0])[0]