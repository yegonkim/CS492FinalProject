import torch.nn as nn
import torch

class wav2Vec2Classifier(nn.Module):
  def __init__(self, wav2vec2, num_labels):
    super(wav2Vec2Classifier, self).__init__()
    self.wav2vec2 = wav2vec2
    self.wav2vec2.aux = nn.Identity()

    self.classifier = nn.Sequential(
         nn.Linear(768, 768),
         nn.Tanh(),
         nn.Dropout(0.25),
         nn.Linear(768, num_labels)
    )

    for idx, child in enumerate(self.wav2vec2.children()):
      if idx == 0:
        for param in child.parameters():
          param.requires_grad = False
   
  def forward(self, x, lengths=None):
    features, _ = self.wav2vec2(waveforms=x, lengths=lengths)
    features = torch.mean(features, dim=1)
    return self.classifier(features)