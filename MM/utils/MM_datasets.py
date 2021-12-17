import torchaudio
import torch.nn as nn
from torch.utils.data import Dataset

# Text, audio Multimodal Dataset for IEMOCAP.
class IEMOCAP_Dataset(Dataset):
  def __init__(self, data, tokenizer):
      self.files = [a for a, _, _ in data]
      self.texts = [b for _, b, _ in data]
      self.labels = [c for _, _, c in data]

      self.input_ids = []
      self.attention_masks = []

      for sent in self.texts:
        encoded_dict = tokenizer.encode_plus(
                          sent,                      
                          add_special_tokens = True, 
                          max_length = 80,         
                          pad_to_max_length = True,
                          return_attention_mask = True, 
                          return_tensors = 'pt',
                    )
        self.input_ids.append(encoded_dict['input_ids'])
        self.attention_masks.append(encoded_dict['attention_mask'])

  def __getitem__(self, idx: int):
      # AUDIO
      fname = self.files[idx]
      waveform, sample_rate = torchaudio.load(fname) 

      if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
      
      if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0)
      
      # CUT
      if waveform.shape[1] > 250000:
        waveform = waveform[:, :250000]

      # Audio, Audio_length, TEXT TOKENIZED, TEXT_ATT, Label
      return waveform, waveform.shape[-1], self.input_ids[idx], self.attention_masks[idx], self.labels[idx]
  
  def __len__(self):
    return len(self.input_ids)

  ### Our Dataset

import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


# For dataset_B: 15 files
# For dataset_A: 60 files.

class Our_Dataset(Dataset):
  def __init__(self, dset_path, tokenizer):

      self.texts = []
      self.files = []
      self.labels = []

      text_path = os.path.join(dset_path, "text.txt")
      
      emotions = ['anger', 'joy', 'neutral', 'sadness']
      f = open(text_path, "r")
      
      for line in f:
        # Not an empty line
        if line.strip():
          idx = line.index(",")
          f_name = line[:idx]
          text = line[idx+2:]
          
          # Skip fear
          if "fear" in f_name:
            continue
          
          emo = emotions.index(f_name.split("_")[0])
          self.labels.append(emo)
          
          # Add label
          self.files.append(os.path.join(dset_path, f_name.strip()))
          self.texts.append(text.strip())
      
      self.input_ids = []
      self.attention_masks = []

      for sent in self.texts:
        encoded_dict = tokenizer.encode_plus(
                          sent,                      
                          add_special_tokens = True, 
                          max_length = 80,         
                          pad_to_max_length = True,
                          return_attention_mask = True, 
                          return_tensors = 'pt',
                    )
        self.input_ids.append(encoded_dict['input_ids'])
        self.attention_masks.append(encoded_dict['attention_mask'])

  def __getitem__(self, idx: int):
      # AUDIO
      fname = self.files[idx]
      waveform, sample_rate = torchaudio.load(fname) 

      if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
      
      if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0).unsqueeze(0)
      
      # CUT
      if waveform.shape[1] > 250000:
        waveform = waveform[:, :250000]

      # Audio, Audio_length, TEXT TOKENIZED, TEXT_ATT, Label
      return waveform, waveform.shape[-1], self.input_ids[idx], self.attention_masks[idx], self.labels[idx]
  
  def __len__(self):
    return len(self.input_ids)