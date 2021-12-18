import torch
import torch.nn as nn

# Co-atteniton Module:

class MHA(nn.Module):
  def __init__(self):
      super(MHA, self).__init__()
      self.key = nn.Linear(768, 768)
      self.query = nn.Linear(768, 768)
      self.value = nn.Linear(768, 768)
      self.attn_drop = nn.Dropout(0.25)

      # 768 // 8 = 96! Perfect :D
      self.proj = nn.Linear(768, 768)
      self.nhead = 8
      self.d_k = 96

  def forward(self, q, k, v):
      
      q, k, v = self.query(q), self.key(k), self.value(v)
      q = q.reshape((q.shape[0], q.shape[1], self.nhead, self.d_k))
      k = k.reshape((k.shape[0], k.shape[1], self.nhead, self.d_k))
      v = v.reshape((v.shape[0], v.shape[1], self.nhead, self.d_k))

      q = q.transpose(1,2)
      k = k.transpose(1,2)
      v = v.transpose(1,2)
      
      out = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)

      out = torch.softmax(out, dim=-1)
      out = self.attn_drop(out)

      out = torch.matmul(out, v)

      out = out.transpose(1, 2)

      # Concat
      out = out.reshape(out.shape[0], out.shape[1], out.shape[2]*out.shape[3])
      out = self.proj(out)

      return out