import torch
import torchaudio
import torch.nn.functional as F
import numpy as np

wav2mel = torch.jit.load("wav2mel.pt")
dvector = torch.jit.load("dvector.pt").eval()
threshold = 0.27069953083992004

def embed(f):
	wav_tensor, sample_rate = torchaudio.load(f)
	mel_tensor = wav2mel(wav_tensor, sample_rate)
	emb_tensor = dvector.embed_utterance(mel_tensor)

	return emb_tensor


def score(enroll_path, test_path):
	enroll_embedding = embed(enroll_path)
	test_embedding = embed(test_path)
	score =  F.cosine_similarity(enroll_embedding.unsqueeze(0), test_embedding.unsqueeze(0))
	score = score.item()
	return score

# check if the score exceeds threshold
def eval(enroll_path, test_path):
	return score(enroll_path, test_path) > threshold
