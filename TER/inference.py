from utils.ter_datasets import TERDataset
from utils.train import train_bert
from models.text_classifier import BertClassifier
from transformers import BertTokenizer
import torch
import torch.nn as nn

def infer(sentence):

    ## PUT HERE YOUR PRETRAINED MODEL.
    pt_path = "./bert-best.pt"

    emos = ['joy', 'sadness', 'fear', 'anger', 'neutral']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    
    encoded_dict = tokenizer.encode_plus(
                    sentence,                      
                    add_special_tokens = True, 
                    max_length = 140,         
                    pad_to_max_length = True,
                    return_attention_mask = True, 
                    return_tensors = 'pt',
                )

    input_id = encoded_dict['input_ids'].to(device)
    attention_mask = encoded_dict['attention_mask'].to(device)

    model = BertClassifier(num_labels=5).to(device)

    model.load_state_dict(torch.load(pt_path))
    output = model(input_id, attention_mask)

    pred = torch.max(output, dim=1)[1]

    return {"text": sentence, "emotion": emos[pred]}