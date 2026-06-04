import hashlib


class PondAuth:

    def __init__(self, key, n=5):
        self.n = n
        self.correct = None
        self.key = key

    def _get_image_hash(self):

        with open("data/output.png", "rb") as f:
            data = f.read()

        return hashlib.sha256(data).hexdigest()

    def generate(self):

        img_hash = self._get_image_hash()

        h = hashlib.sha256(self.key + img_hash.encode()).hexdigest()

        num = int(h, 16)

        self.correct = (num % self.n) + 1
        print(self.correct)
        print("\nChoose the correct pond:\n")

        for i in range(1, self.n + 1):
            print(f"[{i}] pond", end=" ")

        print()

    def load(self):
        self.generate()

    def verify(self, choice):
        return choice == self.correct
