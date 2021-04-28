#!/usr/bin/env python
import sys
from PIL import Image
from des import DesKey

#get the last bit of the binary string
def getLastBit(n):
    iTb=list("{0:b}".format(n))
    lastInd = len(iTb) - 1
    return iTb[lastInd]

#convert the decimal integer to the binary string 
def intToBinaryString(n):
    strlst = list("{0:b}".format(n))
    if(len(strlst) < 8):
        num = 8 - len(strlst)
        for i in range(num):
            strlst.insert(0,'0')
    string = ''.join([str(elem) for elem in strlst])
    return string

#convert the decimal integer to a list of binary
def intToBinaryList(n):
    strlst = list("{0:b}".format(n))
    if(len(strlst) < 8):
        num = 8 - len(strlst)
        for i in range(num):
            strlst.insert(0,'0')
    return strlst

#convert the secret image to binary string
def convertSecretToBinary(name):
    im=Image.open(name)
    im=im.convert("RGB")
    binaryString=""
    #get the pixels of secret image
    for i in range(im.width):
        for j in range(im.height):
            lst = list(im.getpixel((i,j)))
            binaryString+=intToBinaryString(lst[0])
            binaryString+=intToBinaryString(lst[1])
            binaryString+=intToBinaryString(lst[2])
    return binaryString

#decode the binary string to hex
def toHex(bl):
    nbyte = len(bl) / 8
    index = 0
    edata = ""
    for i in range(int(nbyte)):
        bstr = bl[index:index+8]
        index += 8
        if len('{:x}'.format(int(bstr,2))) == 1:
            ascode = "0"+'{:x}'.format(int(bstr,2)) + " "
        else:    
            ascode = '{:x}'.format(int(bstr,2)) + " "
        edata += ascode
    return edata

#encrypt the Header
def encodeHeader(key,header):
    key0 = DesKey(bytes((key),"utf-8"))
    enData = key0.encrypt(bytes(header,"utf-8"),padding=True)
    lst = []
    for i in enData:
        lst.append(i)
    return lst

#encrypted the Data
def encodeData(key,data):
    key0 = DesKey(bytes((key),"utf-8"))
    enData = key0.encrypt(bytes.fromhex(data),padding=True)
    lst = []
    for i in enData:
        lst.append(i)
    return lst

#decode the header data
def decodeHeaderData(key,encrypt_Data):
    key0 = DesKey(bytes((key),"utf-8"))
    try:
        data = key0.decrypt(encrypt_Data,padding=True)
    except:
        print("Key is not valid")
        sys.exit(2)
    return data.decode("utf-8")

#decode the content data
def decodeContentData(key,encrypt_Data):
    key0 = DesKey(bytes((key),"utf-8"))
    data = key0.decrypt(encrypt_Data,padding=True)
    return list(data)


