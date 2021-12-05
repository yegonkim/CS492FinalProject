import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2Processor
import numpy as np
import pandas as pd

from preprocess import build_dataloader
import argparse
from transformers import AutoConfig, Wav2Vec2Processor
from models.classifier import Wav2Vec2ForSpeechClassification

parser = argparse.ArgumentParser(description="Running inference...")
parser.add_argument('-p', '--path', help='audio file to predict. Supports mp3 or wav.')

def infer_SER():

    args = parser.parse_args()
    mp = "./wav2vec2SER/checkpoint-2100"
    basic_path = 'facebook/wav2vec2-base-960h'
    device = torch.device("cuda")
    config = AutoConfig.from_pretrained(basic_path)
    processor = Wav2Vec2Processor.from_pretrained(basic_path)
    model = Wav2Vec2ForSpeechClassification.from_pretrained(mp).to(device)
    sampling_rate = processor.feature_extractor.sampling_rate
    label_list = ['joy', 'sadness', 'anger', 'neutral', 'fear']

    def speech_file_to_array_fn(path, sampling_rate):
        speech_array, _sampling_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(_sampling_rate, sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
    
        return speech
    
    def predict(path, sampling_rate):
        speech = speech_file_to_array_fn(path, sampling_rate)
        features = processor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
        
        input_values = features.input_values.to(device)

        if len(input_values.shape) == 3:
            input_values = input_values.mean(dim=1)

        with torch.no_grad():
            logits = model(input_values).logits

        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        outputs = [{"Emotion": label_list[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
        
        return outputs

    def prediction(path):
        
        setup = {
            'border': 2,
            'show_dimensions': True,
            'justify': 'center',
            'classes': 'xxx',
            'escape': False,
        }
        
        outputs = predict(path, sampling_rate)
        return pd.DataFramee(outputs)
    
    result = prediction(str(args.path))
    return result
    
if __name__ == '__main__':
    result = infer_SER()
    print(result)