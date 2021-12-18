# Automatic Emotion Diary (CS492I) 📖
#### Speech Verifcation 🔒

To train, first preprocess the data with mel spectogram using `python preprocess.py ./data/voxceleb/VoxCeleb1/dev ./data/Libri/LibriSpeech/train-clean-100  -o preprocessed`. This creates a folder `preprocessed` that contains preprocessed data and metadata.
Then, run `python train.py preprocessed model_saved`. The models will be saved under `model_saved/checkpoints`.

To perform speaker verification, import `inference`, and run
```
inference.eval(enroll_paths, test_path)
```
with `enroll_paths` being a list of paths (list of strings) to enrollment .wav files, and `test_path` being the path (string) to .wav file for testing. The function returns `True` if the speakers for enrollment and testing are judged to be the same, and `False` otherwise.

The audio files should have sampling rate of 16kHz.

To 

#### Baseline

- We have referred to this [repo](https://github.com/jymsuper/SpeakerRecognition_tutorial) for implementing d-vector based speaker verification and this [repo](https://github.com/yistLin/dvector) for implementing GE2E loss.

#### Data 🗒️
The directory `./data` contains the script for downloading data. Run with `sh download.sh`. The directory will contain the RAVDESS, LibriSpeech, and VoxCeleb1 dataset, along with our own dataset of emotional speech.

- For more info on each dataset, refer to this following link.
     - [RAVDESS](https://zenodo.org/record/1188976)
     - [LibriSpeech](https://www.openslr.org/12/)
     - [VoxCeleb1](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html)

