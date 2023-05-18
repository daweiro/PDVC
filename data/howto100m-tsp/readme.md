# Howto100m TSP ver

# Clone TSP

# Create env
python -m venv venv
pip install --upgrade pip
pip install -r requirements.txt

requirements.txt
```
pandas
h5py
av
joblib
tqdm
-f https://download.pytorch.org/whl/torch_stable.html
torch==1.9.1+cu111
torchvision==0.10.1+cu111
torchaudio==0.9.1
```

# Get videos

```
for v in $(cat $HOME/git/daweiro/PDVC/data/howto100m/captiondata/formatted_captions_val.json| jq "keys|.[]"|tr -d '"'|
tr '\n' ' '); do ~/yt-dlp -o '%(id)s' --remux-video=mp4 $v; done
```

# Standardize videos
```
 bash $HOME/git/daweiro/TSP/data/standardize_videos_to_constant_30fps_mp4.sh $HOME/git/daweiro/howto-videos/output/train/ $HOME/git/daweiro/howto-videos/stand_out/train/
```

# Generate metadata csv
```
python $HOME/git/daweiro/TSP/data/generate_metadata_csv.py  --video-folder=$HOME/git/daweiro/howto-videos/stand_out/train/ --output-csv=$HOME/git/daweiro/howto-videos/stand_out/train.csv
```

# Launch release extract
```
source train_env
bash extract_features_from_a_released_checkpoint.sh
```

Train env
```
export DATA_PATH=$HOME/git/daweiro/howto-videos/stand_out/train
export METADATA_CSV_FILENAME=$HOME/git/daweiro/howto-videos/stand_out/train.csv
export RELEASED_CHECKPOINT=r2plus1d_34-tsp_on_activitynet
export STRIDE=16
```

# Launch post process
```
python merge_pkl_files_into_one_h5_feature_file.py --features-folder=$HOME/git/daweiro/TSP/extract_features/output/r2plus1d_34-tsp_on_activitynet_features/stride_16/test --output-h5=$HOME/git/daweiro/howto-videos/featuresr2plus1d_34-tsp_on_activitynet-howto-test_features.h5
```

# Convert
```
python convert_tsp_h5_to_npy.py
```



