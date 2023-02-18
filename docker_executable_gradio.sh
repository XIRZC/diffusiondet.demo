sudo docker run -it --rm \AA
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
# -v ${PWD}/../pics/:/work/pics \
registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-executable-v2.0 \
