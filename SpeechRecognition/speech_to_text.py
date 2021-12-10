from vosk import KaldiRecognizer
import json
import config as c

def speech_to_text(model, wav_path=c.wav_path):
  rec = KaldiRecognizer(model, 16000)

  wf = open(wav_path, "rb")
  wf.read(44) # skip header

  result = []

  while True:
      data = wf.read(4000)
      if len(data) == 0:
          break
      if rec.AcceptWaveform(data):
          res = json.loads(rec.Result())
          result.append(res['text'])

  res = json.loads(rec.FinalResult())
  result.append(res['text'])
  
  result_text = ' '.join(result)
  
  return result_text
