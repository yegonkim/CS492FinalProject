# Automatic Emotion Diary (CS492I) 📖
#### Speech Emotion Recognition (SER) Section🔊


Run following scripts after downloading the datasets, according to your purpose:

```
1. For training, run `python run.py`
2. For Inference, Use the function in `inference.py`, and pass your `audio_file_path` as the argument.
```

> For training and evaluation, you don't have to use the resampled ones. But resampling original files will take time preprocessing the data ~ 1 hour. So it is recommended to use the resmapled version from the beginning, which is the default.
(Refer to `line 30` of `run.py`)

#### Baseline

- We have referred to this [repo](https://github.com/MeidanGR/SpeechEmotionRecognition_Realtime), based on MFCC + LSTM.
- For this implementation, refer to **baseline.ipynb.**, accuracy is about **80%.**

#### Ours

- For this task, We adopt [wav2vec](https://github.com/pytorch/fairseq/tree/main/examples/wav2vec), which exploits powerful representations from speech audio alone without labels, and shows powerful results when applied to downstream tasks.
- We achieve **> 98%** accuracy.


#### Data 🗒️
This is where the data should be stored. The directory contains RAVDESS, TESS, and their resampled versions.
First download the data (audio files) using `sh download.sh.`

##### RAVDESS

- RAVDESS consists 24 professional actors (12 female, 12 male) speaking different lines, for 1~3 seconds, which contains in total of 1440 files.
- TESS consists of two female actors speaking `Say the Word ____"`, with a set of 200 target words, and is spoken in variety of emotions.
- Our data contains in total of ~ 3,000 files, as we careful select only 5 emotions that may be applicable for our scneario. (Joy, Sadness, Anger, Fear, Sadness)

- For more info, refer to this following link.
     - [RAVDESS](https://zenodo.org/record/1188976)
     - [TESS](https://tspace.library.utoronto.ca/handle/1807/24487)


