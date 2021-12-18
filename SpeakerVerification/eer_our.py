import os
import sys

import torch
import torchaudio
import torch.nn.functional as F
from tqdm.auto import tqdm
from glob import glob
import numpy as np
from sklearn.metrics import roc_curve

from data import Wav2Mel

import config as c

wav_dir = './data/our_dataset'

def get_spk_from_filename(f):
  return os.path.basename(f).split('_')[1]

def main():
	wav2mel = Wav2Mel()

	dvector_path = c.model_path
	dvector = torch.jit.load(dvector_path).eval()

	spk_embedding = {}

	for f in tqdm(glob(os.path.join(wav_dir, '**/*.wav'), recursive=True)):
		spk = get_spk_from_filename(f)
		wav_tensor, sample_rate = torchaudio.load(f)
		mel_tensor = wav2mel(wav_tensor, sample_rate)  # shape: (frames, mel_dim)
		spk_embedding[f] = (spk,  dvector.embed_utterance(mel_tensor))

	feature_enroll = {}
	spk_enroll = {}

	for f in glob(os.path.join(wav_dir, '**/neutral_*_1.wav'), recursive=True):
	  spk = get_spk_from_filename(f)
	  wav_tensor, sample_rate = torchaudio.load(f)
	  feature_enroll[spk] = wav2mel(wav_tensor, sample_rate)  # shape: (frames, mel_dim)

	for spk in feature_enroll:
	  spk_enroll[spk] = dvector.embed_utterance(feature_enroll[spk])

	score_matrix = np.zeros((len(spk_enroll),len(spk_embedding)))
	truth_matrix = np.zeros((len(spk_enroll),len(spk_embedding)))

	for i, spk_i in enumerate(tqdm(spk_enroll)):
	  for j, f_j in enumerate(spk_embedding):
	    score = F.cosine_similarity(spk_enroll[spk_i].unsqueeze(0), spk_embedding[f_j][1].unsqueeze(0))
	    score = score.data.cpu().numpy()
	    score_matrix[i,j] = score
	    if spk_i == spk_embedding[f_j][0]:
	      truth_matrix[i,j] = 1
	    else:
	      truth_matrix[i,j]=0

	y_pred = score_matrix.flatten()
	y = truth_matrix.flatten()

	fpr, tpr, threshold = roc_curve(y, y_pred, pos_label=1)
	fnr = 1 - tpr
	eer_threshold = threshold[np.nanargmin(np.absolute((fnr - fpr)))]
	EER = fpr[np.nanargmin(np.absolute((fnr - fpr)))]
	print(f"EER threshold: {eer_threshold}")
	print(f"EER: {EER}")

if __name__ == '__main__':
	main()



