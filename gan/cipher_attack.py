try:
    import torch
    from gan.discriminator import Discriminator
except ImportError:
    torch = None
    Discriminator = None


class CipherAttack:

    def __init__(self):

        self.D = Discriminator() if Discriminator is not None else None

        if self.D is not None:
            self.D.eval()


    def check_cipher(self, text):

        data = text.encode()

        if torch is None:
            unique_ratio = len(set(data[:16])) / max(1, min(len(data), 16))
            return min(1.0, max(0.0, unique_ratio))

        nums = list(data[:16])

        if len(nums) < 16:
            nums += [0] * (16 - len(nums))

        x = torch.tensor(nums, dtype=torch.float32).unsqueeze(0)

        out = self.D(x)

        score = out.item()

        return score
