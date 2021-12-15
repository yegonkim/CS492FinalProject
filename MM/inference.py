import torch.nn as nn
import torch
from torch.utils.data import DataLoader
from torchaudio.models.wav2vec2.model import wav2vec2_base
from transformers import BertTokenizer
from data.preprocess import get_IEMOCAP_files
from utils.MM_datasets import IEMOCAP_Dataset
from utils.tools import collate_fn_pad
from utils.train import train_MM
from models.mm_classifier import MultiModalClassifier

# IMPORT MODELS
import sys
sys.path.insert(1, '/content/CS492FinalProject')

from models.mm_classifier import MultiModalClassifier
from SpeechRecognition.speech_to_text import speech_to_text
from vosk import Model

def inference(audio_path, text=None):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # From Vosk. get text file, if text is not Provided.
    if not text:   
        vosk_path = "./vosk-model-en-us-0.22"
        model = Model(vosk_path)
        text = speech_to_text(model, audio_path)
    

    # Bert Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    # CONCAT-BASED Fusion yields best result.
    mm_model = MultiModalClassifier(bc=bc, wc=wc, opt=1).to(device)
    pretrained_path = "./MM_opt1-best.pth"
    mm_model.load_state_dict(torch.load(pretrained_path)["model"])

    # Process input audio_file
    waveform, sample_rate = torchaudio.load(path) 

    if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
    
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0)

    waveform = waveform.to(device)

    # Process text.
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    
    encoded_dict = tokenizer.encode_plus(
                    text,                      
                    add_special_tokens = True, 
                    max_length = 80,         
                    pad_to_max_length = True,
                    return_attention_mask = True, 
                    return_tensors = 'pt',
                )

    input_id = encoded_dict['input_ids'].to(device)
    attention_mask = encoded_dict['attention_mask'].to(device)
    
    output = mm_model(waveform.unsqueeze(0), waveform.shape[-1], input_id, attention_mask)
    pred = torch.max(output, dim=1)[1]

    emos = ['anger', 'joy', 'neutral', 'sadness']
    
    return {"emotion": emos[pred]}


