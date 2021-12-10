You need to install vosk beforehand
```
pip install vosk
```

Run `download_and_unzip.sh` to download the standard English Vosk model.
Alternatively, you can download a model of your choice from https://alphacephei.com/vosk/models.

1. Import the 'speech_to_text' function inside 'speech_to_text.py'
```
from speech_to_text import speech_to_text
```
2. Create a Vosk model as follows. (You can use a model of your choice by using the path to the model, instead of `c.model_path`)
```
from vosk import Model
import config as c
model = Model(c.model_path)
```
3. Call the function with model and path to .wav file as the argument
```
print(speech_to_text(model, 'audio.wav'))
```

