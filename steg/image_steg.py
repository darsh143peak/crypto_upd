from PIL import Image


class ImageSteg:
    def _text_to_bits(self, text):

        bits = ""

        for ch in text:
            bits += format(ord(ch), "08b")

        bits += "0000000000000000"

        return bits
    def _bits_to_text(self, bits):

        chars = []

        for i in range(0, len(bits), 8):

            byte = bits[i:i+8]

            if byte == "00000000":
                break

            chars.append(chr(int(byte, 2)))

        return "".join(chars)
    def hide(self, input_img, output_img, text):

        img = Image.open(input_img)
        img = img.convert("RGB")

        bits = self._text_to_bits(text)

        pixels = list(img.getdata())

        new_pixels = []

        bit_index = 0

        for pixel in pixels:

            r, g, b = pixel

            if bit_index < len(bits):
                r = (r & ~1) | int(bits[bit_index])
                bit_index += 1

            if bit_index < len(bits):
                g = (g & ~1) | int(bits[bit_index])
                bit_index += 1

            if bit_index < len(bits):
                b = (b & ~1) | int(bits[bit_index])
                bit_index += 1

            new_pixels.append((r, g, b))

        img.putdata(new_pixels)
        img.save(output_img)


    def extract(self, img_path):

        img = Image.open(img_path)
        pixels = list(img.getdata())

        bits = ""

        for pixel in pixels:

            r, g, b = pixel

            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

        return self._bits_to_text(bits)