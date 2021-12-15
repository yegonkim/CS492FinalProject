import torch
import torch.nn as nn

class MM_attention(nn.Module):
  def __init__(self):
    super(MM_attention, self).__init__()
    self.mlp = nn.Sequential(
                  nn.Linear(768, 256),
                  nn.ReLU(),
                  nn.Dropout(0.25),
                  nn.Linear(256, 768)
                )
    
    self.maxpool = nn.AdaptiveMaxPool1d(1)
    self.avgpool = nn.AdaptiveAvgPool1d(1)
    self.sigmoid = nn.Sigmoid()

  def forward(self, x, y):
    # x shape is (c1, 768)
    # y shape is (c2, 768)
    x = x.permute(0, 2, 1)
    x_max = self.maxpool(x).permute(0, 2, 1).squeeze(1)
    x_avg = self.avgpool(x).permute(0, 2, 1).squeeze(1)

    y = y.permute(0, 2, 1)
    y_max = self.maxpool(y).permute(0, 2, 1).squeeze(1)
    y_avg = self.avgpool(y).permute(0, 2, 1).squeeze(1)

    x_max = self.mlp(x_max)
    x_avg = self.mlp(x_avg)
    y_max = self.mlp(y_max)
    y_avg = self.mlp(y_avg)

    result = x_max + x_avg + y_avg + y_max
    result = self.sigmoid(result)

    return result