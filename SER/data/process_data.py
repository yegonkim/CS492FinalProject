# Author: hbin0701 @21-12-01
# PRE-DEFINED EMOTION LIST, w.r.t to the TEXT analysis.
import csv
import moviepy.editor
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

  # 3. Preprocess MELD
  MELD_dirs = {"output_repeated_splits_test": "test_sent_emo.csv", "dev_splits_complete": "dev_sent_emo.csv", "train_splits": "train_sent_emo.csv"}
  os.makedirs("./data/MELD/audio", exist_ok=True)
  
  # {'joy', 'neutral', 'surprise', 'disgust', 'anger', 'fear', 'sadness'}
  for subdir in os.listdir("./data/MELD"):
    
    print("subdir", subdir)

    if '.' in subdir or 'audio' in subdir:
      continue

    # Process Label file.
    label_file = f"./data/MELD/{MELD_dirs[subdir]}"
    tmp = [[0 for _ in range(100)] for _ in range(5000)] # make 5000 x 100
    
    f = open(label_file, "r")
    label_reader = csv.reader(f, delimiter=',')
    
    next(f)
    emos = []
    for line in label_reader:
      emos.append(line[3])
      emo, dial_id, utter_id = line[3], int(line[5]), int(line[6])
      tmp[dial_id][utter_id] = emo

    # Process MP4 File.
    with tqdm(list(enumerate(os.listdir(f"./data/MELD/{subdir}")))) as files:
      for idx, file in files:
        if 'mp4' not in file:
          continue
            
        if file[0] != 'd':
          s = file.index('dia')
          file = file[s:]
          os.rename(f"./data/MELD/{subdir}/{file}", f"./data/MELD/{subdir}/{file}")

        dia_num, utt_num = file.split(".")[0].split("_")
        dia_num = int(''.join(a for a in dia_num if a.isdigit()))
        utt_num = int(''.join(b for b in utt_num if b.isdigit()))
        emos = tmp[dia_num][utt_num]

        if emos not in fn_dict:
          continue

        fn_dict[emos].append(mp3)

        mp4, mp3 = f"./data/MELD/{subdir}/{file}", f"./data/MELD/audio/{file.split('.')[0]}.mp3"
        
        if os.path.exists(mp3):
          continue
        
        try:
          videoclip = moviepy.editor.VideoFileClip(mp4, verbose=False)
          audioclip = videoclip.audio
          audioclip.write_audiofile(mp3, logger=None)
          audioclip.close()
          videoclip.close()
        except Exception as e:
          print(e)
          print(f"ERROR on file: {file}")
          continue

  '''

  BERLIN is only used for test-time. Thus, it is commented out.

  # 4. Process Berlin
  ber_dict = {"F": "happiness", "W": "anger", "T": "sadness", "A": "fear", "N": "neutral"}
  
  #{'joy', 'neutral', 'surprise', 'disgust', 'anger', 'fear', 'sadness'}
  for file in os.listdir("./data/BERLIN"):
    emo = ber_dict[file[5]]
    fn_dct[emo].append(f"./data/BERLIN/{file}")
  '''