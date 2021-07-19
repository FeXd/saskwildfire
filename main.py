import requests
import shutil
import filecmp
import os
import tweepy
import time
import datetime
import random
from pdf2image import convert_from_path
from dotenv import load_dotenv

tweet_url = 'https://saskatchewan.ca/fire'

fire_url = 'http://environment.gov.sk.ca/firefiles/'

fire_data = [
    {
        'pdf': 'activefires.pdf',
        'title': 'Saskatchewan Daily Wildfire Situation Map',
    },
    {
        'pdf': 'MunicipalFireBans.pdf',
        'title': 'Saskatchewan Fire Ban Map',
    },
    {
        'pdf': 'DailyFireDangerMaps/today_fwi.pdf',
        'title': "Saskatchewan Spatial Fire Management System: Today's Forecast",
    },
    {
        'pdf': 'DailyFireDangerMaps/tomorrow_fwi.pdf',
        'title': "Saskatchewan Spatial Fire Management System: Tomorrow Forecast",
    },
]


def download_file(url, path, file):
    response = requests.get(url+file, stream=True)
    write_file = open(path+file, 'wb')
    write_file.write(response.content)
    write_file.close()


def move_file(path, file, new_path):
    if os.path.isfile(path+file):
        shutil.move(path+file, new_path+file)


def generate_images_from_pdf(in_path, pdf, out_path):
    images = convert_from_path(in_path+pdf)
    for i, image in enumerate(images):
        filename = pdf+str(i)+'.png'
        image.save(out_path+filename, "PNG")


def image_history(image, path, new_path):
    if os.path.isfile(path+image):
        shutil.copy(path+image, new_path + datetime.datetime.now().strftime('%y%m%d-%H:%M-') + image)


def tweet(title, image):
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    status = title + '\n\nUpdate Detected: ' + datetime.datetime.now().strftime('%d %b %Y %I:%M %p CST') + '\n\n More info at: ' + tweet_url

    try:
        api = tweepy.API(auth)
        api.update_with_media(image, status)
        log('Tweet:', status.replace('\n', ''))
    except tweepy.TweepError as error:
        log('Error: update_status: Something went wrong!', error)


def log(text1, text2='', text3=''):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}: {text1} {text2} {text3}")


if __name__ == '__main__':
    log('Sask Wildfire Bot is now running...')
    load_dotenv()
    while True:
        for item in fire_data:
            time.sleep(random.randint(60, 120))  # wait 1 or 2 minutes
            move_file('./pdf/', item['pdf'], './old/')
            download_file(fire_url, './pdf/', item['pdf'])
            if not os.path.isfile('./old/'+item['pdf']) or not filecmp.cmp('./pdf/' + item['pdf'], './old/' + item['pdf'], shallow=True):
                log('Updated File!', item['pdf'])
                generate_images_from_pdf('./pdf/', item['pdf'], './image/')
                tweet(item['title'], './image/'+item['pdf']+'0.png')
                image_history('./image/', item['pdf']+'0.png', './history/')
            else:
                log('No Changes: ', item['pdf'])
        time.sleep(random.randint(1800, 3600))  # wait 30 to 60 minutes

