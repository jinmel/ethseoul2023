import torch

from models import SimpleModel

ckpt = torch.load('./assets/model.pt')

model = SimpleModel()
model.load_state_dict(ckpt)
model.eval()


with torch.no_grad():
    input_vec = torch.randn(16)
    result = model(input_vec)
    print(result[0].numpy())
