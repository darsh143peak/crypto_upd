import random
import time


class OTP:

    def __init__(self):
        self.current = None
        self.expire = 0


    def generate(self):

        self.current = str(random.randint(100000, 999999))

        self.expire = time.time() + 30

        return self.current


    def verify(self, code):

        if time.time() > self.expire:
            return False

        return code == self.current