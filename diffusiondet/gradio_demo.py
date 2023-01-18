# Copyright (c) Facebook, Inc. and its affiliates.
import os
import argparse
import numpy as np
import cv2
import gradio as gr
import matplotlib.pyplot as plt

from detectron2.config import get_cfg
from diffusiondet.predictor import VisualizationDemo
from diffusiondet import DiffusionDetDatasetMapper, add_diffusiondet_config, DiffusionDetWithTTA
from diffusiondet.util.model_ema import add_model_ema_configs, may_build_model_ema, may_get_ema_checkpointer, EMAHook, \
    apply_model_ema_and_restore, EMADetectionCheckpointer

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    # To use demo for Panoptic-DeepLab, please uncomment the following two lines.
    # from detectron2.projects.panoptic_deeplab import add_panoptic_deeplab_config  # noqa
    # add_panoptic_deeplab_config(cfg)
    add_diffusiondet_config(cfg)
    add_model_ema_configs(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg

def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser

def plot_multi_images_grids(args, num_steps, step_options, opencv_visualized_imgs, gallery_mask):

    if num_steps == 0:
        return [(f"{args.output}/EnsembleAllStep.jpg", "Prediction Result")]
    else:
        image_caption_array, image_filename_array, convert_array = [], [], []
        for i in range(num_steps+2):
            if i == 0:
                image_caption_array.append("Generated Random Noise Boxes")
                image_filename_array.append("StartNoise.jpg")
                convert_array.append(0)
            elif i < num_steps+1:
                image_caption_array.extend([f"Step {i} {op}" for op in ['Prediction', 'Filter', 'DDIM', 'Renewal']])
                image_filename_array.extend([f"{op}-SampleStep{i}.jpg" for op in ['Prediction', 'Filter', 'DDIM', 'Renewal']])
                convert_array.extend([i+j for j in [0, num_steps+1, 2*num_steps+1, 3*num_steps+1]])
            else:
                image_caption_array.extend([f"Step {i} Prediction", "All Steps Ensemble NMS Results" if "Ensembling with NMS" in step_options else "Final Iterative Step Result"])
                image_filename_array.extend([f"Prediction-SampleStep{i}.jpg", "EnsembleAllStep.jpg"])
                convert_array.extend([i, i+(3*num_steps+1)])

        # settings
        nrows, ncols = num_steps+1, 4  # array of sub-plots
        figsize = [18, 12]     # figure size, inches

        # create figure (fig), and array of axes (ax)
        fig, ax = plt.subplots(nrows=nrows,ncols=ncols,figsize=figsize)
        ensemble_img = None

        # plot simple raster image on each sub-plot
        for i, axi in enumerate(ax.flat):
            # i runs from 0 to (nrows*ncols-1)
            # axi is equivalent with ax[rowid][colid]
            if i < 4*num_steps+2:
                img = opencv_visualized_imgs[convert_array[i]]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                axi.set_title(image_caption_array[i])
            elif i == 4*num_steps+2:
                img = opencv_visualized_imgs[convert_array[i]]
                axi.set_title(image_caption_array[i])
                ensemble_img = img
            else:
                img = np.full_like(img, 255)
            axi.imshow(img)
            # write row/col indices as axes' title for identification
            axi.axis('off')

        plt.tight_layout()
        plt.savefig(f"{args.output}/summary.jpg")
        # plt.show()
        # plt.imshow(ensemble_img)
        # plt.show()
        new_image_caption_array, new_image_filename_array = [], []
        for i in range(len(gallery_mask)):
            if gallery_mask[convert_array[i]]:
                new_image_caption_array.append(image_caption_array[i])
                new_image_filename_array.append(image_filename_array[i])
        new_image_caption_array.insert(0, "Summary")
        new_image_filename_array.insert(0, "summary.jpg")
        return [(f"{args.output}/{filename}", new_image_caption_array[i]) for i, filename in enumerate(new_image_filename_array)]


def img2detections(num_boxes, num_steps, step_options, filter_threshold, nms_threshold, img):
    args = get_parser().parse_args()
    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)
    _, visualized_output, opencv_visualized_imgs, gallery_mask = demo.run_on_image(num_boxes, num_steps, step_options, filter_threshold, nms_threshold, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    visualized_output.save(os.path.join(args.output, f"EnsembleAllStep.jpg"))
    opencv_visualized_imgs.append(visualized_output.get_image())
    gallery_mask.append(1)
    d = args.output
    for i in range(len(opencv_visualized_imgs)):
        if i < 1:
            cv2.imwrite(f"{d}/StartNoise.jpg", opencv_visualized_imgs[i])
        elif i < 1+(num_steps+1):
            cv2.imwrite(f"{d}/Prediction-SampleStep{i}.jpg", opencv_visualized_imgs[i])
        elif i < 1+(num_steps+1)+num_steps:
            cv2.imwrite(f"{d}/Filter-SampleStep{i-(num_steps+1)}.jpg", opencv_visualized_imgs[i])
        elif i < 1+(num_steps+1)+num_steps+num_steps:
            cv2.imwrite(f"{d}/DDIM-SampleStep{i-(2*num_steps+1)}.jpg", opencv_visualized_imgs[i])
        elif i < 1+(num_steps+1)+num_steps+num_steps+num_steps:
            cv2.imwrite(f"{d}/Renewal-SampleStep{i-(3*num_steps+1)}.jpg", opencv_visualized_imgs[i])
    return plot_multi_images_grids(args, num_steps, step_options, opencv_visualized_imgs, gallery_mask)

title = "DiffusionDet Demo"
inputs = [
    gr.Slider(minimum=50, maximum=1000, step=50, value=300, label="Number of Dynamic Boxes during Inference(500 during Training)"),
    gr.Slider(minimum=0, maximum=9, step=1, value=3, label="Number of Progressive Refinement Sampling Steps during Inference"),
    gr.CheckboxGroup(choices=['DDIM', 'Box Renewal', 'Ensembling with NMS'], value=['DDIM', 'Box Renewal', 'Ensembling with NMS'], label="Options to Apply during each Progressive Refinement Step"),
    gr.Slider(minimum=0.10, maximum=0.80, step=0.02, value=0.30, label="Box Confidence Filtering Threshold during each Box Renewal Process"),
    gr.Slider(minimum=0.30, maximum=0.70, step=0.05, value=0.50, label="NMS Threshold during Ensembling All Steps Prediction"),
    gr.Image()
]
outputs = [
    gr.Gallery()
]
examples = [
    [300, 3, ['DDIM', 'Box Renewal', 'Ensembling with NMS'], 0.30, 0.50, "./examples/COCO_val2014_000000581831.jpg"],
    [300, 3, ['DDIM', 'Box Renewal', 'Ensembling with NMS'], 0.30, 0.50, "./examples/COCO_val2014_000000306693.jpg"]
]

demo = gr.Interface(
    img2detections, 
    inputs=inputs,
    outputs=outputs,
    title=title,
    examples=examples
)

demo.launch()
