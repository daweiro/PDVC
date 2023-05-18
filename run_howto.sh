#!/bin/bash
video_folder=visualization/videos/howtovalidation
output_folder=visualization/output/howtovalidation
pdvc_model_path=save/howto100m-tsp_anet_tsp_pdvc_v_2023-05-18-18-10-37/model-best.pth
output_language=en
sh test_and_visualize.sh $video_folder $output_folder $pdvc_model_path $output_language
