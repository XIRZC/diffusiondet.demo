sudo docker run -it --rm \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v ${PWD}/../:/work/ \
registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-interactive
