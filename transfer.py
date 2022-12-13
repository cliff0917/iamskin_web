import io
import base64
import PIL.Image

# convert string to img
def encode(code=None):
    code = str.encode(code)
    code = base64.b64decode(code)
    code = io.BytesIO(code)
    img = PIL.Image.open(code)
    return img

# convert string to img
def decode(b64_string):
    res = b64_string.split(',')[1]
    img_b64decode = base64.b64decode(res)
    image = io.BytesIO(img_b64decode)
    img = PIL.Image.open(image)
    img.save("test.jpg")
    return image