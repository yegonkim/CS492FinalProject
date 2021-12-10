# Author: hbin0701 @21-12-01
# PRE-DEFINED EMOTION LIST, w.r.t to the TEXT analysis.

# This file is to process the data in the first place right after downloading and unzipping.
import csv
from tqdm import tqdm
import os

emos = ['joy', 'sadness', 'fear', 'anger', 'neutral']

fn_dict = {}
for emo in emos:
  fn_dict[emo] = []


def data_process():
  '''
  The directory format should be:
  - data
      - BERLIN
      - RAVDESS
      - TESS
      - MELD
  
  train/val: TESS/RAVDESS/MELD (90%)
  test1: MELD (10%)
  test2: BERLIN (cross-dataset TEST, cross-language EVAL)
   
  AFTER, the directory must be in the following format:

  - final_data
    - test
      - anger
        anger01.wav
        anger02.wav
        ...
      - joy
        joy01.wav
        joy02.wva 
        ...
      etc.
   '''

  os.makedirs("./final_data", exist_ok=True)

  # 1. Preprocess RAVDESS 
  # RAVDESS: (192, 192, 192, 192, 288)

  # "02" is calm, but we consider it here as calm.
  rav = {"03": "joy", 
         "01": "neutral", 
         "02": "neutral", 
         "04": "sadness", 
         "05": "anger",
         "06": "fear"
        }

  for actors in os.listdir("./data/RAVDESS"):
    for file in os.listdir(f"./data/RAVDESS/{actors}"):
      file_emo = file.split("-")[2]

      # Process only those 5 predefined emotions.
      if file_emo in rav:
        fn_dict[rav[file_emo]].append(f"./data/RAVDESS/{actors}/{file}")
      else:
        continue

  # 2. Preprocess TESS (400, 400, 400, 400, 400)

  tess = {
      "angry": "anger",
      "happy": "joy",
      "neutral": "neutral",
      "sad": "sadness",
      "fear": "fear"
  }
  for file in os.listdir("./data/TESS"):
    file_emo = file.split(".")[0].split("_")[-1]
    if file_emo in tess:
      fn_dict[tess[file_emo]].append(f"./data/TESS/{file}")