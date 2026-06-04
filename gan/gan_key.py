import os

try:
    import torch
    from gan.generator import Generator
except ImportError:
    torch = None
    Generator = None


class GANKey:

    def __init__(self):

        self.G = Generator() if Generator is not None else None

        if self.G is not None:
            self.G.eval()


    def generate_noise(self):

        if torch is None:
            key = os.urandom(16)

            with open("data/gan_noise.bin", "wb") as f:
                f.write(key)

            return key

        noise = torch.randn(1, 16)

        out = self.G(noise)

        key = out.detach().numpy().tobytes()

        with open("data/gan_noise.bin", "wb") as f:
            f.write(key)

        return key


    def load_noise(self):

        with open("data/gan_noise.bin", "rb") as f:
            return f.read()
