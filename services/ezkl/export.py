import io
import numpy as np
import torch.onnx
import torch
import json
import ezkl_lib

def export(torch_model, input_shape=None, input_array=None, onnx_filename="network.onnx", input_filename="input.json"):
    """Export a PyTorch model.
    Arguments:
    torch_model: a PyTorch model class, such as Network(torch.nn.Module)
    Optional Keyword Arguments:
    - input_shape: e.g. [3,2,3], a random input with these dimensions will be generated.
    - input_array: the given input will be used for the model
    Note: Exactly one of input_shape and input_array should be specified.
    - onnx_filename: Default "network.onnx", the name of the onnx file to be generated
    - input_filename: Defualt "input.json", the name of the json input file to be generated for ezkl

    """
    if input_array is None:
        x = 0.1*torch.rand(1,*input_shape, requires_grad=True)
    else:
        x = input_array

    torch_out = torch_model(x)

    # Export the model
    torch.onnx.export(torch_model,               # model being run
                      x,                   # model input (or a tuple for multiple inputs)
                      onnx_filename,            # where to save the model (can be a file or file-like object)
                      export_params=True,        # store the trained parameter weights inside the model file
                      opset_version=10,          # the ONNX version to export the model to
                      do_constant_folding=True,  # whether to execute constant folding for optimization
                      input_names = ['input'],   # the model's input names
                      output_names = ['output'], # the model's output names
                      dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                                    'output' : {0 : 'batch_size'}})

    data_array = ((x).detach().numpy()).reshape([-1]).tolist()

    data = dict(input_shapes = [input_shape],
                input_data = [data_array],
                output_data = [((o).detach().numpy()).reshape([-1]).tolist() for o in torch_out])

    # Serialize data into file:
    json.dump( data, open( input_filename, 'w' ) )

    # Runs a forward operation to quantize inputs
    # ezkl_lib.forward(input_filename, onnx_filename, input_filename)
