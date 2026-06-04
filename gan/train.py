import torch
import torch.nn as nn
import torch.optim as optim

from gan.generator import Generator
from gan.discriminator import Discriminator


G = Generator()
D = Discriminator()

loss_fn = nn.BCELoss()

opt_G = optim.Adam(G.parameters(), lr=0.001)
opt_D = optim.Adam(D.parameters(), lr=0.001)


for epoch in range(500):

    real = torch.randn(8, 16)

    noise = torch.randn(8, 16)
    fake = G(noise)

    # train D

    D_real = D(real)
    D_fake = D(fake.detach())

    loss_D = (
        loss_fn(D_real, torch.ones(8,1)) +
        loss_fn(D_fake, torch.zeros(8,1))
    )

    opt_D.zero_grad()
    loss_D.backward()
    opt_D.step()


    # train G

    fake = G(noise)
    out = D(fake)

    loss_G = loss_fn(out, torch.ones(8,1))

    opt_G.zero_grad()
    loss_G.backward()
    opt_G.step()


    if epoch % 100 == 0:
        print(epoch, loss_D.item(), loss_G.item())