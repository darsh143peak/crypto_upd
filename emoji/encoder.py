from emoji.map import emoji_map
class EmojiEncoder:

    def encode(self, text):

        out = ""

        for c in text:
            out += emoji_map.get(c, c)

        return out