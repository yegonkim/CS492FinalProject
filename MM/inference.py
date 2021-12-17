import torch.nn as nn
import torch
from torchaudio.models.wav2vec2.model import wav2vec2_base
from models.mm_classifier import MultiModalClassifier

# IMPORT MODELS
import sys
sys.path.insert(1, '/content/CS492FinalProject')

from TER.models.text_classifier import BertClassifier
from SER.models.speech_classifier import wav2Vec2Classifier
from models.mm_classifier import MultiModalClassifier
from SpeechRecognition.speech_to_text import speech_to_text
from transformers import BertTokenizer
from vosk import Model
import torchaudio

def inference(audio_path, text=None):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = Model("vosk-model-en-us-0.22")

    # From Vosk. get text file, if text is not Provided.
    if text is None:   
        text = speech_to_text(model, audio_path)

    print(f"Detected Text: [{text}]")    

    # Bert Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    bc = BertClassifier(num_labels=4)
    model_ = wav2vec2_base(aux_num_out=32)
    wc = wav2Vec2Classifier(num_labels=4, wav2vec2=model_)

    # Channelwise Attention Yields Best Result.
    # Use the early-stopped version for better generalizaiton.
    mm_model = MultiModalClassifier(bc=bc, wc=wc, opt=1).to(device)
    pretrained_path = "./opt0-14.pth"
    mm_model.load_state_dict(torch.load(pretrained_path)["model"])

    # First check, if the audio_file is 16 kHz.
    # Process input audio_file
    waveform, sample_rate = torchaudio.load(audio_path) 

    if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
        torchaudio.save(f"{audio_path}_resample.wav", waveform, sample_rate=16000)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0).unsqueeze(0)

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

    output = mm_model(waveform, None, input_id, attention_mask)
    pred = torch.max(output, dim=1)[1]

    emos = ['anger', 'joy', 'neutral', 'sadness']

    return {"emotion": emos[pred]}