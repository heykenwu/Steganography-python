#!/usr/bin/env python
import sys
from PIL import Image
from dcutils import *


#get the Byte from the 3 pixels from the cover image 
def getByte(lst):
    val = []
    val.append(getLastBit(lst[0][0]))
    val.append(getLastBit(lst[1][0]))
    val.append(getLastBit(lst[2][0]))
    val.append(getLastBit(lst[0][1]))
    val.append(getLastBit(lst[1][1]))
    val.append(getLastBit(lst[2][1]))
    val.append(getLastBit(lst[0][2]))
    val.append(getLastBit(lst[1][2]))
    bs=''.join(val)
    return int(bs,2)

#change the last bit of the pixel and get the number in decimal
def hideInPixel(integ, digitToHide):
    intStr = "{0:b}".format(integ)
    strlst = list(intStr)
    if(len(strlst) < 8):
        num = 8 - len(strlst)
        for i in range(num):
            strlst.insert(0,'0')
    strlst[7] = digitToHide
    string = ''.join([str(elem) for elem in strlst])
    return int(string,2)

#hide the secret image inside the cover image
def hidePic(key,cover_name,name):
    
    #open cover image
    im = Image.open(cover_name).convert("RGB")
    
    #open secret image
    sc = Image.open(name)
    #convert the secret 
    encryptData = encodeData(key,toHex(convertSecretToBinary(name)))
    #encrypt header
    if "/" in name:
        arr = name.split("/")
        name = arr[len(arr)-1]
    header = name + " " + str(sc.width) + " " + str(sc.height) + " " + str(len(encryptData)) + " "
    encryptHeader = encodeHeader(key,header)

    #position of current pixel
    height=0
    width=0

    #number of bytes of the secret header
    numOfbyte = len(encryptHeader)
    
    for byte in range(int(numOfbyte)):
        bList = intToBinaryList(encryptHeader[byte])
        pList=[]
    #save current postion
        x = width
        y = height
    #Get 3 pixels at a time (3 pixels = 1 char)
        for i in range(3):
            pList.append(list(im.getpixel((width,height))))
            width += 1
            if width == im.width:
                width = 0
                height += 1
    #Hide char in the every 3 pixels 
        pList[0][0] = hideInPixel(pList[0][0], bList[0])
        pList[1][0] = hideInPixel(pList[1][0], bList[1])
        pList[2][0] = hideInPixel(pList[2][0], bList[2])
        pList[0][1] = hideInPixel(pList[0][1], bList[3])
        pList[1][1] = hideInPixel(pList[1][1], bList[4])
        pList[2][1] = hideInPixel(pList[2][1], bList[5])
        pList[0][2] = hideInPixel(pList[0][2], bList[6])
        pList[1][2] = hideInPixel(pList[1][2], bList[7])
    #put a byte to three pixels
        for i in range(3):
            im.putpixel((x,y),(pList[i][0],pList[i][1],pList[i][2]))
            x += 1
            if x == im.width:
                x = 0
                y += 1
        pList=[]

    #number of bytes of the secret data
    numOfbyte = len(encryptData)
    
    for byte in range(int(numOfbyte)):
        bList = intToBinaryList(encryptData[byte])
        pList=[]
    #save current postion
        x = width
        y = height
    #Get 3 pixels at a time (3 pixels = 1 char)
        for i in range(3):
            pList.append(list(im.getpixel((width,height))))
            width += 1
            if width == im.width:
                width = 0
                height += 1
    #Hide char in the every 3 pixels 
        pList[0][0] = hideInPixel(pList[0][0], bList[0])
        pList[1][0] = hideInPixel(pList[1][0], bList[1])
        pList[2][0] = hideInPixel(pList[2][0], bList[2])
        pList[0][1] = hideInPixel(pList[0][1], bList[3])
        pList[1][1] = hideInPixel(pList[1][1], bList[4])
        pList[2][1] = hideInPixel(pList[2][1], bList[5])
        pList[0][2] = hideInPixel(pList[0][2], bList[6])
        pList[1][2] = hideInPixel(pList[1][2], bList[7])
    #put a byte to three pixels
        for i in range(3):
            im.putpixel((x,y),(pList[i][0],pList[i][1],pList[i][2]))
            x += 1
            if x == im.width:
                x = 0
                y += 1
        pList=[]
    outputName=str(len(encryptHeader))+".bmp"
    im.save(outputName)

#get data
def showData(key,output_name):
    #open the cpiher pic
    im = Image.open(output_name).convert("RGB")
    #position of current pixel for the cipher pic
    height=0
    width=0
    #secret image name
    name=output_name
    splitarr=[]
    if "/" in output_name:
        splitarr = output_name.split("/")
        name = splitarr[len(splitarr) - 1]
    name_arr = name.split(".")
    #Total encryption data len
    enHeaderLen=int(name_arr[0])
    enHeaderData=[]

    for by in range(enHeaderLen):
        pList=[]
        for i in range(3):
            pList.append(list(im.getpixel((width,height))))
            width += 1
            if width == im.width:
                width = 0
                height += 1
        enHeaderData.append(getByte(pList[0:3]))
        pList=[]
    try:
        data = decodeHeaderData(key,bytes(enHeaderData))
    except:
        print("Key is not valid")
        sys.exit(2)
    #get the name width height and data of the secret image
    data_arr = data.split(" ")
    sc_name=data_arr[0]
    try:
        sc_width = data_arr[1]
    except:
        print("Key is not valid")
        sys.exit(2)
    sc_height = data_arr[2]
    data_size = data_arr[3]  
    encryptcontent = []
    for by in range(int(data_size)):
        pList=[]
        for i in range(3):
            pList.append(list(im.getpixel((width,height))))
            width += 1
            if width == im.width:
                width = 0
                height += 1
        encryptcontent.append(getByte(pList[0:3]))
        pList=[]
    content = decodeContentData(key,bytes(encryptcontent))
    #secret image width
    secret_width = int(sc_width)
    secret_currentW = 0
    #secret image height
    secret_height = int(sc_height)
    secret_currentH = 0
    #create new image
    secret_img = Image.new( 'RGB', (secret_width,secret_height))
    numOfpixels = len(content)/3
    index = 0
    for pixel in range(int(numOfpixels)):
        r=content[index]
        index += 1
        g=content[index]
        index += 1
        b=content[index]
        index += 1
        try:
            secret_img.putpixel((secret_currentW,secret_currentH),(r,g,b))
        except:
            print(secret_currentH,secret_currentW)
            sys.exit(2)
        secret_currentH += 1
        if  secret_currentH== secret_height:
            secret_currentH = 0
            secret_currentW += 1
    secret_img.save(sc_name)
