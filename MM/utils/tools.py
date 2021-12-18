import torch

def collate_fn_pad(batch):
    length = torch.LongTensor([ length for t, label, length in batch ])
    labels = torch.LongTensor([label for t, label, length in batch])
    batch = [ t.squeeze(0) for t, length, label in batch ]
    batch = torch.nn.utils.rnn.pad_sequence(batch)

    return batch, labels, length