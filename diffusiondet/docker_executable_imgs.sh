sudo docker run -it --rm \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v ${PWD}/../pics/:/work/pics \
c3a2b2af93cb \
--input /work/pics/COCO_val2014_000000000192.jpg*
