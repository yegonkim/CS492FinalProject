from vosk import Model, KaldiRecognizer
import json
import config as c

def speech_to_text(model_path = c.model_path, wav_path = c.wav_path):

  model = Model(model_path)

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

def main():
  print(speech_to_text(c.model_path, c.wav_path))

if __name__ == 'main':
  main()
