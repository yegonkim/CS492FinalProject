# Automatic Emotion Diary (CS492I) 📖
#### Speech Verifcation 🔒

To train, first preprocess the data with MFCC filter using  `python  `python train.py 

#### Baseline

- We have referred to this [repo](https://github.com/jymsuper/SpeakerRecognition_tutorial) for implementing d-vector based speaker verification and this [repo](https://github.com/yistLin/dvector) for implementing GE2E loss.

#### Data 🗒️
The directory `./data` contains the script for downloading data. Run with `sh download.sh`. The directory will contain the RAVDESS, LibriSpeech, and VoxCeleb1 dataset, along with our own dataset of emotional speech.

- For more info, refer to this following link.
     - [RAVDESS](https://zenodo.org/record/1188976)
     - [TESS](https://tspace.library.utoronto.ca/handle/1807/24487)



To perform speaker verification, import `inference`, and run
```
eval(enroll_paths, test_path)
```
with `enroll_paths` being a list of paths (string format) to enrollment .wav files, and `test_path` being the path (str) to .wav file for testing.

The `.wav` files should have sampling rate of 16kHz.
