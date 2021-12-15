import torch
import torch.nn as nn
from MHA import MHA
from attention import MM_attention

class MultiModalClassifier(nn.Module):
  def __init__(self, bc, wc, opt=2):
    super(MultiModalClassifier, self).__init__()

    # FOR YOUR REFERENCE
    options = [
               "MHA_before_pooling", 
               "MHA_after_pooling", 
               "Channel-wise attention", 
               "CONCAT", 
               "WEIGHTED", 
               "SPEECH ONLY", 
               "TEXT ONLY"
               ]
    
    self.opt = opt
    self.bc = bc
    self.wc = wc

    if self.opt < 0 :
        self.mha = MHA()
        self.classifier = nn.Sequential(
              nn.Linear(768*2, 512),
              nn.Tanh(),
              nn.Dropout(0.25),
              nn.Linear(512, 4)
          )
        
    if self.opt == 0:
      self.mm_attention = MM_attention()
      self.classifier = nn.Sequential(
          nn.ReLU(),
          nn.Dropout(0.25),  
          nn.Linear(768, 4)
      )

    if self.opt == 1:  
      self.classifier = nn.Sequential(
              nn.Linear(768*2, 512),
              nn.Tanh(),
              nn.Dropout(0.25),
              nn.Linear(512, 4)
          )
      
    elif opt == 2:
      self.alpha = nn.Parameter(torch.randn(5))
    
  def forward(self, speech, length, text, attention_mask):
    
    if self.opt == -2:
      # USING MHA before pooling, to exploit attention from channelwise richness.
      speech_result, _ = self.wc.wav2vec2(speech, length)
      text_result = self.bc.bert.bert(text, attention_mask)['last_hidden_state']

      out1 = self.mha(speech_result, text_result, text_result).squeeze(1)
      out2 = self.mha(text_result, speech_result, speech_result).squeeze(1)
      
      out1 = torch.mean(out1, dim=1)
      out2 = torch.mean(out2, dim=1)

      # concat
      out = torch.cat([out1, out2], dim=-1)
      out = self.classifier(out)
      return out

    if self.opt == -1:
      # Co-attention in (MHA):
      # https://arxiv.org/pdf/2008.06682.pdf
      speech_result, _ = self.wc.wav2vec2(speech, length)
      speech_result = speech_result.mean(dim=1).unsqueeze(1)

      text_result = self.bc.bert(text, attention_mask)['logits'].unsqueeze(1)
      
      out1 = self.mha(speech_result, text_result, text_result).squeeze(1)
      out2 = self.mha(text_result, speech_result, speech_result).squeeze(1)
      
      # concat
      out = torch.cat([out1, out2], dim=-1)
      out = self.classifier(out)
      return out

    if self.opt == 0:
      # Channel-wise ATTENTION Module Inpisred by CBAM:
      speech_result, _ = self.wc.wav2vec2(speech, length)
      # Note this bert does not contain pooling layer now.
      text_result = self.bc.bert.bert(text, attention_mask)['last_hidden_state']
      result = self.mm_attention(speech_result, text_result)
      result = self.classifier(result)
      return result

    elif self.opt == 1:
      # CONCAT. BASED ATTENTION:
      speech_result, _ = self.wc.wav2vec2(speech, length)
      speech_result = speech_result.mean(dim=1)
      text_result = self.bc.bert(text, attention_mask)['logits']
      out = torch.cat([text_result, speech_result], dim=-1)
      out = self.classifier(out)
      return out

    # WEIGHTED BASED LATE FUSION.    
    elif self.opt == 2:
      speech_result = self.wc(speech, length)
      text_result = self.bc(text, attention_mask)   
      return self.alpha * speech_result + (1- self.alpha) * text_result

    # SPEECH ONLY
    elif self.opt == 3:
      out = self.wc(speech ,length)
      return out
    
    # TEXT ONLY
    elif self.opt == 4:
      out = self.bc(text, attention_mask)
      return out
