# Automatic Emotion Diary (CS492I)
#### Speech Emotion Recognition

Baseline vs ours.


#### Baseline

- We have referred to this [repo][https://github.com/MeidanGR/SpeechEmotionRecognition_Realtime], based on MFCC + LSTM.
- For this implementation, refer to **baseline.ipynb.**

#### Ours

- We have included more datasets to consider IN-THE-WILD conditions and multi-lingual corpuses.
- We also have further changed the design of the framework, incorporating [wav2vec][https://github.com/pytorch/fairseq/tree/main/examples/wav2vec] for encoding.
- Also, we solve the imbalance caused by data augmentation by adopting various loss functions.


#### Data 🗒️
This is where the data should be stored. The structure of this directory should be:

```
- Data
     - BERLIN
     - MELD
     - RAVDESS
     - TESS
```

#### Baseline
To run baseline, run:

```
python run_baseline.py
```

