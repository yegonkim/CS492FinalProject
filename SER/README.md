# Automatic Emotion Diary (CS492I)
#### Speech Emotion Recognition

Baseline vs ours.


#### Baseline

- We have referred to this [repo](https://github.com/MeidanGR/SpeechEmotionRecognition_Realtime), based on MFCC + LSTM.
- For this implementation, refer to **baseline.ipynb.**, accuracy is about 80%.

#### Ours

- We have changed the design of the framework, incorporating [wav2vec](https://github.com/pytorch/fairseq/tree/main/examples/wav2vec) and NN for classifier. The code was slightly modified from the notebook file in [repo](https://github.com/m3hrdadfi/soxan)
- We achieve > 98% accuracy.

#### Future work
- We have included more datasets to consider IN-THE-WILD conditions and multi-lingual corpuses.
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
