import string

chars = string.ascii_letters + string.digits + "+/="

emojis = [chr(0x1F600 + i) for i in range(len(chars))]

emoji_map = dict(zip(chars, emojis))