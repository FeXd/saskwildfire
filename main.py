import requests
from requests.exceptions import RequestException
import shutil
import filecmp
import os
import tweepy
import time
import datetime
import random
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
from dotenv import load_dotenv

tweet_url = 'https://saskatchewan.ca/fire'

fire_data = [
    {
        'pdf': 'activefires.pdf',
        'path': 'http://environment.gov.sk.ca/firefiles/',
        'title': 'Saskatchewan Daily Wildfire Situation Map',
    },
    {
        'pdf': 'firestodate.pdf',
        'path': 'http://environment.gov.sk.ca/firefiles/',
        'title': 'Fires to Date',
    },
    {
        'pdf': 'MunicipalFireBans.pdf',
        'path': 'http://environment.gov.sk.ca/firefiles/',
        'title': 'Saskatchewan Fire Ban Map',
    },
    {
        'pdf': 'today_fwi.pdf',
        'path': 'http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/',
        'title': "Saskatchewan Spatial Fire Management System: Today's Forecast",
    },
    {
        'pdf': 'tomorrow_fwi.pdf',
        'path': 'http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/',
        'title': "Saskatchewan Spatial Fire Management System: Tomorrow Forecast",
    },
]


def download_file(url, path, file):
    """ Download File from URL to specific path

    Note that the name of source and target file must be same.

    :param string url: web address (without file name)
    :param string path: local file path to save file
    :param string file: file name (bust be the same
    :return boolean: True on success, False on failure
    """
    try:
        response = requests.get(url+file, stream=True, timeout=30)
        write_file = open(path+file, 'wb')
        write_file.write(response.content)
        write_file.close()
        return True
    # All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.
    except RequestException as error: 
        log('RequestException: download_file: ' + url+file, error)
        return False


def move_file(path, file, new_path):
    """ Move a file from one location to another

    :param string path: original path
    :param string file: name of file (include extension)
    :param string new_path: destination path
    """
    if os.path.isfile(path+file):
        shutil.move(path+file, new_path+file)


def generate_images_from_pdf(in_path, pdf, out_path):
    """ Generate PNG images from PDF (single or multi-page)

    File name of PNG is generated from PDF file name.
    A page number and .png is appended to the end of the PDF file name.

    :param string in_path: path for PDF
    :param string pdf: file name of PDF (include extension)
    :param string out_path: path for generated PNGs
    """
    try:
        images = convert_from_path(in_path+pdf)
        for i, image in enumerate(images):
            filename = pdf+str(i)+'.png'
            image.save(out_path+filename, "PNG")
    except PDFPageCountError as error:
        log("Error: generate_images_from_pdf!", error)


def image_history(path, image, new_path):
    # TODO: this function is copying an image file to another location with a time stamp - refactor
    if os.path.isfile(path+image):
        shutil.copy(path+image, new_path + datetime.datetime.now().strftime('%y%m%d-%H%M-') + image)


def tweet(title, image):
    """ Generate a tweet with a specific title and image, then try to tweet it

    :param string title: tweet title, shown at top of tweet
    :param string image: path to image TODO: rename to path or image_path?
    """

    # CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_TOKEN_SECRET are stored in local .env file
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    hashtags = '#sk #wildfire #skwildfire #skfires'
    status = title + '\n\nUpdate Detected: ' + datetime.datetime.now().strftime('%d %b %Y %I:%M %p CST') + '\n\nMore info at: ' + tweet_url + '\n\n' + hashtags

    try:
        api = tweepy.API(auth)
        api.update_with_media(image, status)
        log('Tweet:', status.replace('\n', ''))
    except tweepy.TweepError as error:
        log('Error: update_status: Something went wrong!', error)


def log(text1, text2='', text3=''):
    """ Log convenience function that adds timestamps to print statements

    In the future, it could be good to send these to a file.
    Three text parameters are available for... even more convenience?

    :param * text1: text to log
    :param * text2: more text to log
    :param * text3: even more text to log
    """
    print(f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}: {text1} {text2} {text3}")


if __name__ == '__main__':
    """ Main loop for application
    
    Runs forever with a random sleep between 30 and 60 minutes.
    """
    log('Sask Wildfire Bot is now running...')
    # load the environment variables from .env (required for tweeting)
    load_dotenv()

    # loop forever
    while True:
        # loop through each endpoint we want to check for updates
        for item in fire_data:
            # wait for a few seconds in order to not hammer server and risk banning
            time.sleep(random.randint(60, 120))  # wait 1 or 2 minutes
            # back up previously downloaded pdf
            move_file('./pdf/', item['pdf'], './pdf_old/')
            # back up previously generated image (png)
            move_file('./image/', item['pdf']+'0.png', './image_old/')

            # download and save file from endpoint, and continue to generate content, and possibly tweet
            if download_file(item['path'], './pdf/', item['pdf']):
                # if ...
                if not os.path.isfile('./pdf_old/'+item['pdf']) or not filecmp.cmp('./pdf/' + item['pdf'], './pdf_old/' + item['pdf'], shallow=True):
                    log('PDF is different: ', item['pdf'])
                    # generate image from pdf to prepare for tweet
                    generate_images_from_pdf('./pdf/', item['pdf'], './image/')
                    # copy generated image to history for safe keeping
                    image_history('./image/', item['pdf'] + '0.png', './history/')
                    # if ...
                    if not os.path.isfile('./image_old/'+item['pdf']+'0.png') or not filecmp.cmp('./image/' + item['pdf'] + '0.png', './image_old/' + item['pdf'] + '0.png', shallow=False):
                        tweet(item['title'], './image/'+item['pdf']+'0.png')
                    else:
                        log('No Image Changes: ', item['pdf'])
                else:
                    log('No PDF Changes: ', item['pdf'])
            else:
                log('File Download Issue: ', item['pdf'])

        # wait 30 to 60 minutes - attempt to not hammer server and be banned
        time.sleep(random.randint(1800, 3600))
