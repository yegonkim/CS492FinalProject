from glob import glob
from pathlib import Path
import pandas as pd


for f in glob('./data/BERLIN/wav/*.wav'):
  speaker = os.path.basename(f)[:2]
  Path(os.path.join('./data/BERLIN/wav' , speaker)).mkdir(parents=True, exist_ok=True)
  os.rename(f, os.path.join('./data/BERLIN/wav', speaker, os.path.basename(f)))

for f in glob('./data/CREMA/CREMA-D/AudioWAV/*.wav'):
  speaker = os.path.basename(f).split('_')[0]
  Path(os.path.join('./data/CREMA/CREMA-D/AudioWAV' , speaker)).mkdir(parents=True, exist_ok=True)
  os.rename(f, os.path.join('./data/CREMA/CREMA-D/AudioWAV', speaker, os.path.basename(f)))