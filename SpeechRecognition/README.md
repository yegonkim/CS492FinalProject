You need to install vosk beforehand
```
pip install vosk
```

Run `download_and_unzip.sh` to download the Vosk model.

1. Import the 'speech_to_text' function inside 'speech_to_text.py' (`from speech_to_text import speech_to_text`)
2. Create a Vosk model as follows.
```
from vosk import Model
import config as c
model = Model(c.model_path)
```
4. Call the function with model and path to .wav file as the argument
```
print(speech_to_text(model, 'audio.wav'))
```

