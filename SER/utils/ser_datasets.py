from torch.utils.data import Dataset
import torchaudio
import torch

class SERDataset(Dataset):

    def __init__(self, path, files, resampled=False, processor=None):
      
        self.files = []
        self.resampled = resampled
        self.processor = processor

        if path is not None:
            self.files = [( f"{path}/{file.split('/')[-1]}", i ) for file, i in files]
        else:
            self.files = files
            
    def __getitem__(self, idx: int):
        path, label = self.files[idx]
        waveform, sample_rate = torchaudio.load(path) 

        if not self.resampled:
          waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
        
        if waveform.shape[0] > 1:
          waveform = waveform.mean(dim=0)

        waveform = waveform.to("cuda")
        if processor is not None:
          wavefrom = torch.FloatTensor(processor(waveform, sampling_rate=16000)["input_values"][0])

        return waveform, label, waveform.shape[-1]

    def __len__(self):
        return len(self.files)