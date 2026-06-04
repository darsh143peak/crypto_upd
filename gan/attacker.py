try:
    import torch
    from gan.discriminator import Discriminator
except ImportError:
    torch = None
    Discriminator = None


class Attacker:

    def __init__(self):

        self.D = Discriminator() if Discriminator is not None else None

        if self.D is not None:
            self.D.eval()


    def try_key(self, key_bytes):

        if torch is None:
            unique_ratio = len(set(key_bytes[:16])) / 16
            return min(1.0, max(0.0, unique_ratio))

        x = torch.tensor(
            list(key_bytes[:16]),
            dtype=torch.float32
        ).unsqueeze(0)

        out = self.D(x)

        score = out.item()

        return score
