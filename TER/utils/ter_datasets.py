import pandas as pd
from transformers import BertTokenizer
from torch.utils.data import Dataset, DataLoader

class TERDataset(Dataset):

    def __init__(self, path, tokenizer=None):
                   
        encoding = {
            'joy': 0,
            'sadness': 1,
            'fear': 2,
            'anger': 3,
            'neutral': 4
        }

        data = pd.read_csv(path)
        self.sents, self.labels = data.Text, [encoding[x] for x in data.Emotion]

        self.input_ids = []
        self.attention_masks = []

        for sent in self.sents:
            encoded_dict = tokenizer.encode_plus(
                                sent,                      
                                add_special_tokens = True, 
                                max_length = 140,         
                                pad_to_max_length = True,
                                return_attention_mask = True, 
                                return_tensors = 'pt',
                        )
            
            self.input_ids.append(encoded_dict['input_ids'])
            self.attention_masks.append(encoded_dict['attention_mask'])


    def __getitem__(self, idx: int):
        return self.input_ids[idx], self.labels[idx], self.attention_masks[idx]

    def __len__(self):
        return len(self.sents)