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

from TER.models.text_classifier import BertClassifier
from SER.models.speech_classifier import wav2Vec2Classifier

def train():

    # GET IEMOCAP files.
    data_dict = get_IEMOCAP_files()

    # 80% training, 20% testing.
    train = []
    test = []

    for i, emo in enumerate(data_dict):
        split = int(len(data_dict[emo]) * 0.8)
        train.extend((fname, text, i) for fname, text in data_dict[emo][:split])
        test.extend((fname, text, i) for fname, text  in data_dict[emo][split:])

    # Bert Tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    train_dset = IEMOCAP_Dataset(data=train, tokenizer=tokenizer)
    test_dset = IEMOCAP_Dataset(data=test, tokenizer=tokenizer)
    train_loader = DataLoader(train_dset, batch_size=4, shuffle=True, collate_fn=collate_fn_pad)
    test_loader = DataLoader(test_dset, batch_size=4, shuffle=True, collate_fn=collate_fn_pad)

    bc = BertClassifier(num_labels=5)
    model = wav2vec2_base(aux_num_out=32)
    wc = wav2Vec2Classifier(num_labels=5, wav2vec2=model)

    # Load pretrinaed models.

    bc.load_state_dict(torch.load("bert-best.pth")["model"])
    bc.classifier =  nn.Sequential(
            nn.Linear(768, 768),
            nn.Tanh(),
            nn.Dropout(0.25),
            nn.Linear(768, 4))

    wc.load_state_dict(torch.load("wav2vec2-best.pth")["model"])
    wc.classifier = nn.Sequential(
            nn.Linear(768, 768),
            nn.Tanh(),
            nn.Dropout(0.25),
            nn.Linear(768, 4))


    # CONCAT-BASED Fusion yields best result.
    mm_model = MultiModalClassifier(bc=bc, wc=wc, opt=1).to("cuda")
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(mm_model.parameters(), lr=1e-5, eps=1e-8)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, gamma=0.5, step_size=50)

    
    # SET PATH FOR LOG and MODEL .PT FILES.
    log_file = "./"
    ckpt_path = "./"

    train(train_loader, test_loader, mm_model, optimizer, criterion, scheduler, log_file, ckpt_path)

    print("Training Finished!")