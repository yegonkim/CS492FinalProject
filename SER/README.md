# Automatic Emotion Diary (CS492I) 📖
#### Speech Emotion Recognition (SER) Section🔊


Run following scripts after downloading the datasets, according to your purpose:

```
# For training
python train.py -td [PyArrow Train Data Path] -vd [PyArrow Val Data Path]

# For Evaluation
python eval.py -vd [PyArrow Val Data Path]

# For Inference
python inference.py -p [Audio File Path]
```

> For training and evaluation, you don't have to provide the arguments, but without providing the PyArrow Train Data Path, it will take time preprocessing the data ~ 1 hour. The PyArrow Dataset files are provided through download.sh.

#### Baseline

- We have referred to this [repo](https://github.com/MeidanGR/SpeechEmotionRecognition_Realtime), based on MFCC + LSTM.
- For this implementation, refer to **baseline.ipynb.**, accuracy is about **80%.**

#### Ours

- For this task, We adopt [wav2vec](https://github.com/pytorch/fairseq/tree/main/examples/wav2vec), which exploits powerful representations from speech audio alone without labels, and shows powerful results when applied to downstream tasks.
- The code was slightly modified and organized from the notebook file in [repo](https://github.com/m3hrdadfi/soxan).
- We achieve **> 98%** accuracy.

#### Future work
- We have included more datasets to consider IN-THE-WILD conditions and multi-lingual corpuses.
- Also, we solve the imbalance caused by data augmentation by adopting various loss functions.


#### Data 🗒️
This is where the data should be stored. The structure of this directory should be:
First download the data (audio files), PyArrow processed dataset file, and pretrained model, by running:
```
sh ./data/download.sh
```


Below describes the data files, with its according source link.
- Data
     - [BERLIN](http://emodb.bilderbar.info/start.html)
     - [MELD](https://github.com/declare-lab/MELD)
     - [RAVDESS](https://zenodo.org/record/1188976)
     - [TESS](https://tspace.library.utoronto.ca/handle/1807/24487)


