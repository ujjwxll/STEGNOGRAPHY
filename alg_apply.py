import string
from forms import encodeForm, decodeForm
import cv2
import numpy as np
from PIL import Image
import os
import re


def original_text():
    form = encodeForm()
    txt = bin(int.from_bytes(form.text.data.encode(), 'big')).replace('b', '')
    return txt


def enc_alg(image: Image):
    a = []
    img = cv2.imread(image)
    new_name = image.split('\\')[-1].replace('org', 'enc')
    row, col, ch = img.shape
    flat_img = img.flatten()
    text = original_text()
    try:
        for i in text:
            c = [int(i)]
            c.append(0)
            a.append(c)
        flat_txt = np.array(a).flatten()
        zeros = np.zeros((len(flat_img)-len(flat_txt),), dtype=int)
        encoded_txt = np.append(flat_txt, zeros)
        encoded_img_flat = np.subtract(flat_img, encoded_txt)
        encoded_img = np.reshape(encoded_img_flat, (row, col, ch))
        enc_path = new_name

        cv2.imwrite(enc_path, encoded_img)
        return len(flat_txt), new_name
    except:
        pass


def dec_alg(original_pic: string, encode_pic: string):
    decodedTxt = []
    form = decodeForm()
    length = int(form.pwd_d.data)
    print(original_pic, '--------------------',
          encode_pic, '--------------------', length)
    org_img = cv2.imread(original_pic)
    flat_org_img = org_img.flatten()
    enc_img = cv2.imread(encode_pic)
    flat_enc_img = enc_img.flatten()

    try:
        sub = np.subtract(flat_org_img[:length], flat_enc_img[:length])
        for i in range(length):
            if i % 2 == 0:
                decodedTxt.append(str(sub[i]))

        txt = ''.join(decodedTxt)
        rev = txt[:1]+'b'+txt[1:]
        n = int(rev, 2)
        # TODO: Include why reason value is 7
        # TODO: Fix image transparent issue
        message = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return message
    except:
        return 'error'
