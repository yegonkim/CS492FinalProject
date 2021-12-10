# Automatic Emotion Diary (CS492I) 📖
#### TEXT Emotion Recognition (TER) Section🔊

1. For training, run `python run.py`
2. For Inference, Use the function in `inference.py`, and pass your `sentence` as the argument.

#### Datasets

- Dataset can be found in `./data` directory.
- We used dataset from baseline [repo](https://github.com/lukasgarbas/nlp-text-emotion).
- where the author mixed `dailydialog`, `emotion-stimulus`, `isear` to create a balanced dataset.

#### Transfer Learning with BERT vs. Baseline
- While the OG author has reached about `0.8320`,
- With careful hyperparameter tuning opitmizer choice, and slight design modification, we reach  over `98%` of accuracy here.

#### Download the pretrained model.
- You can download pretrained model from [here](https://drive.google.com/file/d/14EE8yxx4q9TKL6dDNfsVWlGW-S0-tNnx/view?usp=sharing).
