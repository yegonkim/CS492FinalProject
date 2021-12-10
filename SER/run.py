import json
from SER.utils.ser_datasets import SERDataset
from SER.utils.train import train_wav2vec
from utils.ser_datasets import SERDataset
from utils.tools import collate_fn_pad
from transformers import Wav2Vec2Processor
from models.speech_classifier import wav2Vec2Classifier
import torch.nn as nn
import torch

def train():

    # Open List of Files for traning and testing.
    f = open("./CS492FinalProject/SER/data/files.json", "r")
    data = json.load(f)

    # 80% training, 20% testing.
    train = []
    test = []

    for i, emo in enumerate(data):
        split = int(len(data[emo]) * 0.8)
        train.extend([(file.split("/")[-1], i) for file in data[emo][:split]])
        test.extend([(file.split("/")[-1], i) for file in data[emo][split:]])


    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h", )
    
    # CHANGE THIS LINE , according to your situation.
    resampled = True

    if resampled:
        path = "./data/rs_audio"
    else:
        path = None

    # Build Dataset and DataLoader
    train_dset = SERDataset(train, path, resampled=True, processor=processor)
    test_dset = SERDataset(test, path, resampled=True, processor=processor)
    train_loader = DataLoader(train_dset, batch_size=16, shuffle=True, collate_fn=collate_fn_pad)
    test_loader = DataLoader(test_dset, batch_size=16, shuffle=True, collate_fn=collate_fn_pad)

    # Load Pretrained Wav2Vec.
    original = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    model = import_huggingface_model(original)
    torch.save(model.state_dict(), "wav2vec2-base-960h.pt")
    model = wav2vec2_base(aux_num_out=32).to("cuda")
    model.load_state_dict(torch.load("wav2vec2-base-960h.pt")) 
    wav_model = wav2Vec2Classifier(model, 5).to("cuda")

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(wav_model.parameters(), lr=5e-5, eps=1e-8)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, gamma=0.5, step_size=50)

    log_file = "./SER/wav_trained.txt"
    ckpt_path = "./TER/"
    train_wav2vec(train_loader, test_loader, wav_model, optimizer, criterion, scheduler, log_file, ckpt_path)

    print("Training Finished!")