You need to install vosk beforehand
```
pip3 install vosk
```

1. Download the speech recognition model from https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
2. Unzip the file and move the folder to the root directory
3. Move the desired audio .wav file to the root directory

To perform ASR and print the text:
1. Check that the path to .wav file and path to model folder is correctly assigned in config.py
2. Run speech_to_text.py

To use the ASR as a library:
1. Import the 'speech_to_text' function inside 'speech_to_text.py'
2. Call the function with path to model, path to .wav file as the argument

