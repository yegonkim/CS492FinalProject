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