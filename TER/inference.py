from models.text_classifier import BertClassifier
from transformers import BertTokenizer
import torch
import torch.nn as nn

def infer(sentence):

    ## RECOMMENDED TO EXPLICITLY SET IT AS AN ABSOLUTE PATH.
    pt_path = "/home/kyuholee/proj_v2/CS492FinalProject/TER/bert-best.pth"

    emos = ['joy', 'sadness', 'fear', 'anger', 'neutral']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True).to(device)
    
    print("activated 1")

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
    print("activated 1")
    del tokenizer
    model = BertClassifier(num_labels=5).to(device)
    print("activated 1")
    print("activated 1")
    model.load_state_dict(torch.load(pt_path)["model"])
    print("activated 2")
    output = model(input_id, attention_mask)

    pred = torch.max(output, dim=1)[1]

    return {"text": sentence, "emotion": emos[pred]}