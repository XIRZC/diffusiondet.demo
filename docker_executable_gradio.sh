sudo docker run -it --rm \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
# -v ${PWD}/../pics/:/work/pics \
registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-executable-v1.0 \