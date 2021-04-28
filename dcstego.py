#!/usr/bin/env python
import sys
from PIL import Image
from dcimage import *
from dcutils import *

import argparse
encode_usage = "Usage: dcstego.py -e <cover image> <secret image>  <key (8 or 16 chars)>"
decode_usage = "Usage: dcstego.py -d <cipher image> <key (8 or 16 chars)>"
parser = argparse.ArgumentParser(description='Image encryption')

#two options encode or decode the image 
options = parser.add_mutually_exclusive_group(required=True)
options.add_argument("-e", "--encode", help=encode_usage, 
        action='store_true')
options.add_argument("-d", "--decode", help=decode_usage, 
        action='store_true')

#source needed for encryption
encryptoptions = argparse.ArgumentParser()
encryptoptions.add_argument("cover", metavar="cover", help="the cover image to hide secret image") 
encryptoptions.add_argument("secret", metavar="secret", help="the secret image to encrypt")
encryptoptions.add_argument("key", metavar="key", help="the key to encrypt the secret image")

#source needed for decryption
decryptoptions = argparse.ArgumentParser()
decryptoptions.add_argument("output", metavar="output_file", help="the cipher image to be decrypted") 
decryptoptions.add_argument("key", metavar="key", help="the key to decrypt the cipher image")

#check the size of the cover image
def checkSize(name):
    im = Image.open(name).convert("RGB")
    return im.width*im.height

#check the size of the cipher
def checkCipherSize(key,name):
    im = Image.open(name).convert("RGB")
    length = len(encodeData(key,toHex(convertSecretToBinary(name))))
    if "/" in name:
        arr = name.split("/")
        name = arr[len(arr)-1]
    header = name + " " + str(im.width) + " " + str(im.height) + " " + str(length) + " "
    length += len(encodeHeader(key,header))
    return length
def main():
    arguments = parser.parse_known_args(sys.argv[1:])
    if arguments[0].encode:
        #check the image format
        arguments = encryptoptions.parse_args(sys.argv[2:])
        cover = arguments.cover
        arr = cover.split(".")
        format_type = ["bmp","png"]
        #check the secret image format
        if(arr[len(arr)-1]) not in format_type:
            print("Error: cover should be a bmp pic")
            sys.exit(2)
        secret_image = arguments.secret
        arr = secret_image.split(".")
        if(arr[len(arr)-1]) not in format_type:
            print("Error: secret image should be a bmp pic")
            sys.exit(2)
        #check the length of the key
        key = arguments.key
        if (len(key)) not in [8,16]:
            print("Error: The length of the key should be 8 or 16 chars")
            sys.exit(2)
        #check if the size of the cover iamge is enough to hide the secret_image
        size_cover = checkSize(cover)
        size_cihper = checkCipherSize(key,secret_image)
        if (int(size_cover / 3)) < size_cihper:
            print("cover image is too small too hide the secret image. Bytes that Cover can cover:" + str(int(size_cover / 3)) + ". Bytes needed for secret image plus header: " + str(size_cihper))
            sys.exit(2) 
        hidePic(key,cover,secret_image)
    else:
        arguments = decryptoptions.parse_args(sys.argv[2:])
        cipher_image = arguments.output
        arr = cipher_image.split(".")
        format_type = ["bmp","png"]
        #check the secret image format
        if(arr[len(arr)-1]) not in format_type:
            print("Error: cipher image should be a bmp pic")
            sys.exit(2)
        #check the length of the key
        key = arguments.key
        if (len(key)) not in [8,16]:
            print("Error: The length of the key should be 8 or 16 chars")
            sys.exit(2)
        showData(key, cipher_image) 
    
if __name__ == "__main__":
    main()