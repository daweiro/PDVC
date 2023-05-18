#!/bin/bash

#    prepare the video features (.npy files) following TSP and convert_tsp_h5_to_npy.py.
#    construct the follow annotations of your dataset.
#    train_caption_file, val_caption_file, visual_feature_folder, gt_file_for_eval, gt_file_for_para_eval, dict_file
#    To further finetune the pre-trained PDVC (TSP), run python train.py --cfg_path=anet_tsp_pdvc.yml --pretrain=full --pretrain_path=path/to/ckpt

python train.py --cfg_path=cfgs/howto100m-tsp_anet_tsp_pdvc.yml --pretrain=full --pretrain_path=save/anet_tsp_pdvc/model-best.pth
