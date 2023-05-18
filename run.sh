#!/bin/bash
video_folder=visualization/videos/original
output_folder=visualization/output/original
pdvc_model_path=save/anet_tsp_pdvc/model-best.pth
output_language=en
sh test_and_visualize.sh $video_folder $output_folder $pdvc_model_path $output_language
