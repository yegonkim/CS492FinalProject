from transformers import BertForSequenceClassification
import torch.nn as nn

class BertClassifier(nn.Module):
  def __init__(self, num_labels):
    super(BertClassifier, self).__init__()
    self.bert = BertForSequenceClassification.from_pretrained(
                    "bert-base-uncased", 
                    num_labels = 5,
                    output_attentions = False, 
                    output_hidden_states = False, 
                )

    for param in self.bert.bert.embeddings.parameters():
      param.requires_grad = False

    self.bert.classifier = nn.Identity()
    self.classifier = nn.Sequential(
         nn.Linear(768, 768),
         nn.Tanh(),
         nn.Dropout(0.25),
         nn.Linear(768, num_labels)
    )

  def forward(self, x, attention_mask):
    output = self.bert(x, attention_mask=attention_mask)['logits']
    output = self.classifier(output)
    return output