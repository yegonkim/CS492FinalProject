from models.speech_classifier import wav2Vec2Classifier
from utils.ser_datasets import SERDataset
from utils.tools import collate_fn_pad
from transformers import Wav2Vec2Processor
from models.speech_classifier import wav2Vec2Classifier
import torch.nn as nn
import torch
import torchaudio

def infer(audio_file_path):

    ## RECOMMENDED TO EXPLICITLY SET IT AS AN ABSOLUTE PATH.
    pt_path = "/content/CS492FinalProject/SER/wav2vec2-best.pth"

    emos = ['joy', 'sadness', 'fear', 'anger', 'neutral']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Preprocess waveform.
    waveform, sample_rate = torchaudio.load(audio_file_path) 
    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
    
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0)

    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h", ).to(device)
    waveform = waveform.to(device)
    waveform = torch.FloatTensor(processor(waveform, sampling_rate=16000)["input_values"][0])
    waveform = torch.nn.utils.rnn.pad_sequence(waveform)
    length = waveform.shape[-1]

    model = wav2Vec2Classifier(num_labels=5).to(device)
    model.load_state_dict(torch.load(pt_path)["model"])

    output = model(waveform, length)
    pred = torch.max(output, dim=1)[1]

    return {"emotion": emos[pred]}