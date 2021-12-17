from typing import List

import torch
import torchaudio
import torch.nn.functional as F
import numpy as np

wav2mel = torch.jit.load("wav2mel.pt")
dvector = torch.jit.load("dvector.pt").eval()
threshold = 0.27069953083992004

def mel(f):
  wav_tensor, sample_rate = torchaudio.load(f)
  mel_tensor = wav2mel(wav_tensor, sample_rate)
  return mel_tensor

def embed(mel_tensors: list):
  return dvector.embed_utterances(mel_tensors)

def score(enroll_paths, test_path):
  enroll_mel_tensors = [mel(f) for f in enroll_paths]
  test_mel_tensors = [mel(test_path)]

  enroll_embedding = embed(enroll_mel_tensors)
  test_embedding = embed(test_mel_tensors)

  score =  F.cosine_similarity(enroll_embedding.unsqueeze(0), test_embedding.unsqueeze(0))
  score = score.item()
  return score

# check if the score exceeds threshold
def eval(enroll_paths: List[str], test_path: str) -> bool:
  return score(enroll_paths, test_path) > threshold

