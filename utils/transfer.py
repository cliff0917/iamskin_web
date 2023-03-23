import PIL.Image, io, base64

def decode(code=None):
    code = str.encode(code)
    code = base64.b64decode(code)
    code = io.BytesIO(code)
    image = PIL.Image.open(code)
    return image


def base2picture(resbase64):
    res = resbase64.split(',')[1]
    img_b64decode = base64.b64decode(res)
    image = io.BytesIO(img_b64decode)
    img = PIL.Image.open(image)
    # img.save("test.jpg")
    return image