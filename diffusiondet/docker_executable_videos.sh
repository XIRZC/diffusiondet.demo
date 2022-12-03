sudo docker run -it --rm \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v ${PWD}/../videos/:/work/videos \
c3a2b2af93cb \
--video-input /work/videos/zebras.mp4
