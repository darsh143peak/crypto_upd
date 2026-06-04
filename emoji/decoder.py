from emoji.map import emoji_map

reverse_map = {v: k for k, v in emoji_map.items()}
class EmojiDecoder:

    def decode(self, text):

        out = ""

        for c in text:
            out += reverse_map.get(c, c)

        return out