
# Pixelformer Fast Inference using TensorRT:


- Used `pixelformer` environment which had cuda-enabled torch. 
- And used system-wide(not able to install in conda env) installed tensorrt from inside the environment using below line.: 
    `export PYTHONPATH="/usr/lib/python3.8/dist-packages:$PYTHON_PATH"` (run it in every terminal, otherwise tensorrt will not be visible from conda env)
- make sure to use `python3` instead of just `python` while running.

### Pytorch to TensorRT conversion pipeline.
1. use `1.pytorch_to_onnx.py` to save pytorch model in onnx format. (I did this in vision04 itself, in jetson it was not working for me(the model was not giving right output). So used torch.onnx.export() function in my eval.py file in visin04)
2. Use `2.onnx_runtime.py` to inference using onnx file(just for sanity check that the model is giving right output or not).
3. Use `3.onnx_to_tensorRT.py` to convert onnx model to tensorRT and also to inference using tensorRT engine(which is saved).


### Time Requirement:
- For one image [of size=(480,640)]:   
    NYUv2:
        pytorch model takes:    0.5 sec  
        onnx model takes:       2.46 sec  
        TensorRT is taking:     **0.25 sec** [Took 9.32 seconds for 60 image!! = **6.5fps**]  
        While I/O demo:         Took 13.10 seconds for 60 image!! = 4.5fps
    Kitti:
        pytorch model takes:    0.5 sec  
        TensorRT is taking:     **0.28 sec** [Took 27.70 seconds for 139 image!!!! = **5fps**]  
        While I/O demo:         Took 13.10 seconds for 60 image!! = 4.5fps

### Sample Depth Outputs:
#### NYUv2 Dataset
![Image](sample_output_images/nyu/000.png)
![Image](sample_output_images/nyu/001.png)
![Image](sample_output_images/nyu/002.png)
![Image](sample_output_images/nyu/003.png)
![Image](sample_output_images/nyu/004.png)
![Image](sample_output_images/nyu/005.png)
![Image](sample_output_images/nyu/006.png)
![Image](sample_output_images/nyu/007.png)
![Image](sample_output_images/nyu/008.png)
![Image](sample_output_images/nyu/009.png)
![Image](sample_output_images/nyu/010.png)
![Image](sample_output_images/nyu/011.png)
![Image](sample_output_images/nyu/012.png)
![Image](sample_output_images/nyu/013.png)
![Image](sample_output_images/nyu/014.png)

#### Kitti Dataset
![Image](sample_output_images/kitti/000.png)
![Image](sample_output_images/kitti/001.png)
![Image](sample_output_images/kitti/010.png)
![Image](sample_output_images/kitti/020.png)
![Image](sample_output_images/kitti/030.png)
![Image](sample_output_images/kitti/040.png)
![Image](sample_output_images/kitti/050.png)
![Image](sample_output_images/kitti/060.png)
![Image](sample_output_images/kitti/070.png)
![Image](sample_output_images/kitti/080.png)
![Image](sample_output_images/kitti/090.png)
![Image](sample_output_images/kitti/100.png)
![Image](sample_output_images/kitti/110.png)
![Image](sample_output_images/kitti/120.png)
![Image](sample_output_images/kitti/130.png)
