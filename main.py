import requests
import shutil
import filecmp
import os
from pdf2image import convert_from_path

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
        'title': "Saskatchewan Spatial Fire Management System: Tomorrow Early Forecast",
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
        filename = pdf+str(i)+'.jpg'
        image.save(out_path+filename, "JPEG")


if __name__ == '__main__':
    for item in fire_data:
        move_file('./pdf/', item['pdf'], './old/')
        download_file(fire_url, './pdf/', item['pdf'])
        if not filecmp.cmp('./pdf/' + item['pdf'], './old/' + item['pdf'], shallow=True):
            print('Updated File!', item['pdf'])
            generate_images_from_pdf('./pdf/', item['pdf'], './image/')
        else:
            print('No Changes: ', item['pdf'])
