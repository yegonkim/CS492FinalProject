# Automatic Emotion Diary (CS492I) 📖
------------------------------------
- We aim to replace `second-level authentication` with `voice-verficiation` along which an user is asked to write an `emotional diary`.
- With `voice-verification`, we also detect `multi-modal emotion detection` from `speech` and `text` (extracted with `speech recognition module`, `vosk`), possibly providing different UIs/suggestions in the future along with the detected emotion.
- With this end, we also aim to help user to record their status everyday, and `provide mental clinical provision`, if negative emotions are consistently observed. 

Below are the brief description of each directory, and please refer to `README.md` of each directory for more information.

#### APP 📱
----
This directory contains backend/frontend service.

#### Speech Recognition 👂
---
For `Speech Recognition`, we used pretrained `VOSK` in order to convert speech to text.

#### Speaker Verifcation 🔒
---
For `Speaker Verification`, we used `GE2E Loss` based framework to verify the input audio file against the enrolled audio files.

#### TER (Text Emotion Recognition) ✍️
---
For `TER`, we aimed to use TEXT-only module to classify the emotion.

#### SER (Speech Emotion Recognition) 🗣️
---
For `SER`, we aimed to use SPEECH-only module to classify the emotion.

#### MM (Multimodal Emotional Recognition) 📠
----
For `MM`, we implement the multimodal (audio + text) emotion classifier which generalizes best with our testing datasets.
