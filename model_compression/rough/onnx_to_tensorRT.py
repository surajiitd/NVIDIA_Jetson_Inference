
"""
Step 3: Optimize the ONNX Model with TensorRT

Use the TensorRT Python API to optimize the ONNX model. Here's an example command:
"""

import tensorrt as trt
import os
# Create a TensorRT builder and network
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(TRT_LOGGER)
network = builder.create_network(1)

# Create an ONNX parser and parse the ONNX model
onnx_path = "/home/vision/suraj/jetson-documentation/model_compression/onnx_models/from_vision04/nyu_model-64000-best_abs_rel_0.09021.onnx"
trt_path = os.path.join("tensorRT_engines",os.path.basename(onnx_path)[:-5]+".trt")
print(f"TensorRT model will be saved in {trt_path}")
parser = trt.OnnxParser(network, TRT_LOGGER)
with open(onnx_path, 'rb') as model_file:
    model_str = model_file.read()
parser.parse(model_str)

# Set the builder parameters and build the TensorRT engine
#builder.max_workspace_size = 1 << 30  # Set the maximum workspace size
config = builder.create_builder_config()
config.max_workspace_size = 1 << 30

#engine = builder.build_cuda_engine(network)
plan = builder.build_serialized_network(network, config)
with trt.Runtime(TRT_LOGGER) as runtime:
    engine = runtime.deserialize_cuda_engine(plan)

# Serialize and save the TensorRT engine
trt_path = os.path.join("tensorRT_engines",os.path.basename(onnx_path)[:-5]+".trt")
#trt_path = onnx_path[:-5]+'.trt'
with open(trt_path, 'wb') as engine_file:
    engine_file.write(engine.serialize())


