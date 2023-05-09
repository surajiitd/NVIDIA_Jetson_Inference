# NVIDIA Jetson Documentation

## Pixelformer
- installing pytorch 
    - Python version:
        made a new conda env named `pixelformer` with python3 version `3.8.16` and python version `3.6.7`.
        (while making a new conda env, it automatically installing above mentioned python versions).
    - CUDA version: output of `/usr/local`  
        ```
        (pixelformer) vision@vision:~$ ls /usr/local
        bin  cuda  cuda-11  cuda-11.4  cuda-11.7  etc  games  include  jetson_stats  jtop  lib  man  sbin  share  src
        ```
        `nvcc -V` gave: 
        ```
        nvcc: NVIDIA (R) Cuda compiler driver
        Copyright (c) 2005-2022 NVIDIA Corporation
        Built on Wed_Jun__8_16:59:16_PDT_2022
        Cuda compilation tools, release 11.7, V11.7.99
        Build cuda_11.7.r11.7/compiler.31442593_0
        ```
    (Now see below for Pytorch installation)
    - [didn't worked] Earlier: using "Build from Source" from [this link](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048).
    - [worked] **Followed [this link](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#prereqs-install)** as mentioned by Pytorch expert [here](https://discuss.pytorch.org/t/how-to-install-pytorch-from-source-on-orin/170970/2).
    - downloaded pytorch v1.14.0 from [this link](https://elinux.org/Jetson_Zoo#PyTorch_.28Caffe2.29).
    - So the commands will be:
    ```
    sudo apt-get -y update; 
    
    sudo apt-get -y install autoconf bc build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev locales moreutils openssl python-openssl rsync scons python3-pip libopenblas-dev;

    # see below to do this in my particular case : export TORCH_INSTALL=path/to/torch-2.0.0a0+fe05266f.nv23.04-cp38-cp38-linux_aarch64.whl

    export TORCH_INSTALL=/home/vision/Downloads/torch-1.14.0a0+44dac51c.nv23.01-cp38-cp38-linux_aarch64.whl
    
    python3 -m pip install --upgrade pip; python3 -m pip install aiohttp numpy=='1.19.4' scipy=='1.5.3' export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"; python3 -m pip install --upgrade protobuf; python3 -m pip install --no-cache $TORCH_INSTALL
    ```
    output of last command was like: 
    ```
    (pixelformer) vision@vision:~/Downloads$ python3 -m pip install --upgrade pip; python3 -m pip install aiohttp numpy=='1.19.4' scipy=='1.5.3' export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"; python3 -m pip install --upgrade protobuf; python3 -m pip install --no-cache $TORCH_INSTALL
    Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
    Requirement already satisfied: pip in /home/vision/miniconda3/envs/pixelformer/lib/python3.8/site-packages (23.1.2)
    ERROR: Invalid requirement: 'LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:/usr/lib/llvm-8/lib:/usr/lib/llvm-8/lib:/usr/local/lib:/usr/local/lib:/usr/local/lib:/usr/local/lib:/usr/local/cuda-11.4/lib64::/usr/local/lib'
    Hint: It looks like a path. File 'LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:/usr/lib/llvm-8/lib:/usr/lib/llvm-8/lib:/usr/local/lib:/usr/local/lib:/usr/local/lib:/usr/local/lib:/usr/local/cuda-11.4/lib64::/usr/local/lib' does not exist.
    Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
    Requirement already satisfied: protobuf in /home/vision/miniconda3/envs/pixelformer/lib/python3.8/site-packages (4.23.0)
    Looking in indexes: https://pypi.org/simple, https://pypi.ngc.nvidia.com
    Processing ./torch-1.14.0a0+44dac51c.nv23.01-cp38-cp38-linux_aarch64.whl
    Requirement already satisfied: networkx in /home/vision/.local/lib/python3.8/site-packages (from torch==1.14.0a0+44dac51c.nv23.01) (3.0)
    Requirement already satisfied: sympy in /home/vision/.local/lib/python3.8/site-packages (from torch==1.14.0a0+44dac51c.nv23.01) (1.11.1)
    Requirement already satisfied: typing-extensions in /home/vision/.local/lib/python3.8/site-packages (from torch==1.14.0a0+44dac51c.nv23.01) (4.5.0)
    Requirement already satisfied: mpmath>=0.19 in /home/vision/.local/lib/python3.8/site-packages (from sympy->torch==1.14.0a0+44dac51c.nv23.01) (1.3.0)
    Installing collected packages: torch
    ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
    torchvision 0.15.1 requires torch==2.0.0, but you have torch 1.14.0a0+44dac51c.nv23.1 which is incompatible.
    Successfully installed torch-1.14.0a0+44dac51c.nv23.1
    ```
    then it worked: 
    ```
    (pixelformer) vision@vision:~/Downloads$ python3
    Python 3.8.16 (default, Mar  2 2023, 03:16:31) 
    [GCC 11.2.0] :: Anaconda, Inc. on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import torch
    >>> torch.Tensor([1,2]).to("cuda")
    tensor([1., 2.], device='cuda:0')
    >>> exit()
    ```

    Also see this : 
    ```
    (pixelformer) vision@vision:~/Downloads$ conda list|grep torch
    pytorch-cuda              11.7                 h67b0de4_2    pytorch
    torch                     1.14.0a0+44dac51c.nv23.1          pypi_0    pypi
    torchvision               0.13.1          cpu_py38heb4ea19_0
    ```
    - above `pytorch-cuda` is installed by some `conda install` command earlier (`conda install pytorch torchvision pytorch-cuda=11.7 -c pytorch -c nvidia`)  which was giving `AssertionError: Torch not compiled with CUDA enabled` when sending a tensor to "cuda".
    - above `torch` is installed right now which is working now.
    