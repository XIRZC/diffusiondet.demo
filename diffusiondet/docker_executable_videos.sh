sudo docker run -it --rm \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v ${PWD}/../videos/:/work/videos \
registry.cn-hangzhou.aliyuncs.com/mrxir/diffusiondet.demo:model-executable \
--video-input /work/videos/zebras.mp4
