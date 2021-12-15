# Automatic Emotion Diary (CS492I) 📖
#### Multimodal (MM) Emotinon Recognition Section 👨‍💻
------------
Run following scripts after downloading the datasets, according to your purpose:

1. For training, run `python run.py`
2. For Inference, Use the function in `inference.py`, and pass your `audio_file_path` as the argument. Now, if you already know the **text** of the audio_file, you can pass it as the second argument. Otherwise, **Vosk** will take care of it.


#### Baseline

- There are many multimodal speech emotion recongition tasks involving `IEMOCAP`,
- However, since we only choose 4 emotions (refer to `/data/preprocess.py`) it is hard to compare to other baselines. 
- Therefore, we have set our own baselines as speech-only and text-only modules.

#### Ours

- For this task, We adopt several multimodal fusion design choices, based on [wav2vec](https://github.com/pytorch/fairseq/tree/main/examples/wav2vec),and [bert](https://arxiv.org/abs/1810.04805). For each module, please refer to `SER` and `TER` directories.
- You can download the pretrained model for our multimodal task, [here](https://drive.google.com/file/d/1RgLIUvf_rZA8BK9RmlBqJQovsIziQrdn/view?usp=sharing). 
- This pretrained module is based on the multimodal design choice with `opt.1: Intermediate fusion: concatenation of encoder features.` To explore model design choices, refer to `./models`, where we provide 6 total options, with the corresponding argument `opt.`

#### Data️
This is where the data should be stored. The directory contains IEMOCAP, where we only filtered out, `neu`, `exc`, `hap`, `sad`, `anger`, while considering `exc` and `hap` belonging to the same emotion of `joy`. For more information refer to `/data/preprocess.py.` But, first download the data, using `sh download.sh.`

#### RESULT

| Fusion Method                     | IEMOCAP Accuracy |
|-----------------------------------|------------------|
| Multi-Headed Attention + Pooling  | 0.7202           |
| Pooling + Multi-Headed Attention  | 0.7374           |
| Channel-wise Attention            | 0.7419           |
| Feature Concatenation             | 0.7410           |
| Weighted Parameter Shallow Fusion | 0.6977           |
| Speech-only                       | 0.7310           |
| Text-only                         | 0.5514           |

