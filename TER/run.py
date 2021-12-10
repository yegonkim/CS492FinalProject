from utils.ter_datasets import TERDataset
from utils.train import train_bert
from models.text_classifier import BertClassifier
from transformers import BertTokenizer
import torch
import torch.nn as nn

def run():

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    # BUILD DATASET
    train_dataset = TERDataset("./TER/data/data_train.csv", tokenizer=tokenizer)
    test_dataset = TERDataset("./TER/data/data_test.csv", tokenizer=tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)

    # DEFAULT
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BertClassifier(num_labels=5).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, eps=1e-8)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, gamma=0.5, step_size=50)

    log_file = "./TER/bert_trained.txt"
    ckpt_path = "./TER/"

    train_bert(train_loader, test_loader, model, criterion, optimizer, scheduler, log_file, ckpt_path)
        
    print("Training Finsihed!")

if '__name__' == '__main__':
    run()