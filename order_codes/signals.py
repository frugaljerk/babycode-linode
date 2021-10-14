from django.db.models.signals import pre_save
from django.dispatch import receiver
# import boto3
from .models import MyBabyCodes
from game_logs.models import GameCharacter
from django.db.models.fields.files import ImageField
from django.core.files import File
from django.core.files.base import ContentFile
import re
import zipfile
import os
import uuid
from babycode import settings
# imports for cartoonization:
import cv2
import concurrent.futures
import itertools
from rembg.bg import remove
import numpy as np
import io
from PIL import Image

# # AWS S3 bucket name
# BUCKET = 'babycode'

# create edge mask
def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(
        gray_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        line_size,
        blur_value,
    )
    return edges

#to get countours
def Countours(image):
    contoured_image = image
    gray = cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 100)

    canny = cv2.dilate(canny, None)
    canny = cv2.erode(canny, None)

    contours, hierarchy = cv2.findContours(
        canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )[-2:]
    cv2.drawContours(contoured_image, contours, contourIdx=-1, color=5, thickness=1)
    return contoured_image

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

# resize image according to character width and height passed in.
def resize_image(img, width=300, height=200):
    return cv2.resize(img, (width, height))


def cartoonize(filename, width, height):

    img = cv2.imdecode(np.frombuffer(filename, np.uint8), cv2.IMREAD_ANYCOLOR)
    # for some reason need to convert RGB2BGR for bilaterfilter to work...
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    edges = edge_mask(img, line_size=9, blur_value=5)

    # colour quantization
    # k value determines the number of colours in the image
    total_color = 9
    k = total_color
    data = np.float32(img).reshape((-1, 3))
    # Determine criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    # Implementing K-Means
    ret, label, center = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)


    # Blurr
    blurred = cv2.bilateralFilter(result, d=9, sigmaColor=300, sigmaSpace=300)

    # final image processing>cartoonize>resize>brighten>encode
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    contoured = Countours(cartoon)
    resized = resize_image(contoured, width, height)
    brightened = increase_brightness(resized, value=60)
    brightened = cv2.cvtColor(brightened, cv2.COLOR_BGR2RGB)
    # return encoded imgfile for further process
    img_encoded = cv2.imencode('.jpg', brightened)[1].tobytes()
    return img_encoded



def process_img(img, imgFile, chars, instance):


    # get the last digit of "image1" and use it to search for character
    imgIndex = img.name[-1]
    # get the character's width and height for the image resizing
    character = chars.get(orderimage_index=imgIndex)

    #convert imgFile to bytearry to be loaded by openCv
    inputpath = bytearray(imgFile.read())

    # cartoonize function return encoded img file
    cartoonfile = cartoonize(inputpath, character.width, character.height)


    # pass the encoded img file to remove function to remove background
    # Credit: https://github.com/danielgatis/rembg
    result = remove(cartoonfile)

    # convert new image file from bytes to ImgFile using PIL and sign a filename
    # imgFileNew = Image.open(io.BytesIO(result)).convert("RGBA")
    # create filename to be saved in AWS
    regex = "\.(?i)(jpe?g|png|gif|bmp)$"
    imgFileNewname = (
            f"order_pics/order_{str(instance.order_id)}/"
            + "background_removed_"
            + img.name
            + re.search(regex, imgFile.name).group()
    )
    # set imgfile to django filefield instance
    imgFileNew = ContentFile(result, imgFileNewname)

    setattr(instance, img.name, imgFileNew)
    # set arcname for zipfile file transfer later
    arcname = os.path.join(
        "data", "img", os.path.basename(imgFileNew.name)
    )  # image subfolder path in the zip


    return arcname, result






@receiver(pre_save, sender=MyBabyCodes)
def create_order(sender, instance, **kwargs):
    #create an random order_id for this instance
    if instance:
        if not instance.order_id:
            global i
            i = str(uuid.uuid4())[:8]
            instance.order_id = i

        order = instance
        # list of instance fields as imagefield
        imgList = [
            x
            for x in instance._meta.fields
            if type(x) == ImageField and getattr(instance, x.name)
        ]
        # list of imgFile from the imagefields
        imgFileList = [getattr(instance, x.name) for x in imgList]


        # key to access AWS S3 bucket for template gamefile and destination folder for download
        key_to_template_gamefile = os.path.join(
                    settings.MEDIA_ROOT,
                    r"game_logs",
                    rf"game_{order.game_id.id}",
                    rf"{str(order.game_id)}.zip"
                )
        key_to_dest_filename = os.path.join(
                    'order_pics',
                    f'order_{str(order.order_id)}',
                    f"{str(order.game_id)}.zip"
                ).replace("\\","/")


        # open AWS S3 bucket and object
        # s3 = boto3.resource('s3')
        # bucket = s3.Bucket(BUCKET)
        # obj = bucket.Object(key_to_template_gamefile)


        # list of characters in the game order
        chars = GameCharacter.objects.filter(game=order.game_id.id)


        # multithread processing for function process_img
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = executor.map(
                process_img,
                imgList,
                imgFileList,
                itertools.repeat(chars),
                itertools.repeat(instance),
            )

            # create a tempt binary file to hold zipfile

            tf = open(key_to_template_gamefile, 'rb')
            tf = io.BytesIO(tf.read())
            # rewind the file
            tf.seek(0)

            for arcname, result in future_results:
            # Read the file as a zipfile and process the members
                with zipfile.ZipFile(tf, mode='a') as zipf:
                    zipf.writestr(arcname, result)



            instance.gamefile = File(tf, key_to_dest_filename)
            print('created instance.game', instance.gamefile)

