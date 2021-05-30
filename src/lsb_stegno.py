import numpy as np
from PIL import Image

# Convert encoding msg into 8-bit binary
# form using ASCII value of characters
def charToBinList(msg):

        # list of binary codes
        # of given msg
        l = []

        for i in msg:
            l.append(format(ord(i), '08b'))
        return l

# Pixels are modified according to the
# 8-bit binary msg and finally returned
def modPix(pix, msg):

    datalist = charToBinList(msg)
    lendata = len(datalist)
    img_data = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in img_data.__next__()[:3] +
                                  img_data.__next__()[:3] +
                                  img_data.__next__()[:3]]
        print(pix)
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Ninth pixel of every set tells
        # whether to stop or to read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        # pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
        
def encode_enc(new_img, msg):
    w = new_img.size[0]
    (x, y) = (0, 0)
    # print(list(new_img.getdata()))
    print(list(new_img.getdata())[:15])
    for pixel in modPix(new_img.getdata(), msg):

        # Putting modified pixels in the new image
        new_img.putpixel((x, y), tuple(pixel))
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    # print(list(new_img.getdata())[:15])

# Encode msg into image
def lsb_encode(msg):
    try:
        image = Image.open('images/img.jpg', 'r')
    except:
        image = Image.open('images/img.png', 'r')

    new_img = image.copy()
    encode_enc(new_img, msg)

    return new_img

# Decode the msg in the image
def lsb_decode(file_name):
    image = Image.open(file_name, 'r')

    msg = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        # string of binary msg
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        msg += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return msg

