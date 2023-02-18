# Demonstration App for `DiffusionDet` with Denoising Process Visualization

This is just a simple demo application built by gradio.

## Environment Preparation

You can just refer to [DiffusionDet](https://github.com/ShoufaChen/DiffusionDet) for basic environment preparation, where we just add gradio package additionally.

Specifically,

``` Shell
conda create -n diffusiondet python=3.7
conda activate diffusiondet
pip install 'git+https://ghproxy.com/https://github.com/facebookresearch/detectron2.git'
pip install gradio timm
```

Otherwise, you can just use our docker image hosted on AliYun.

``` Shell
docker pull registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-executable-v2.0
```

## Usage

By local environment:

- In Linux, just run `./gradio_demo.sh`
- In Windows, just run `python gradio_demo.py` under created diffusiondet conda virtual environment

By docker container:

Just run `docker run -it --rm -p 7860:7860 registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-executable-v2.0` in any OS terminal with docker installed.

