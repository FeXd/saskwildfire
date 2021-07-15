import requests
import shutil
import filecmp
import os
from pdf2image import convert_from_path

fire_url = 'http://environment.gov.sk.ca/firefiles/'

fire_pdfs = [
    'activefires.pdf',
    'MunicipalFireBans.pdf',
    'DailyFireDangerMaps/today_fwi.pdf',
    'DailyFireDangerMaps/tomorrow_fwi.pdf',
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
        fname = pdf+str(i)+'.jpg'
        image.save(out_path+fname, "JPEG")


if __name__ == '__main__':
    for pdf in fire_pdfs:
        move_file('./pdf/', pdf, './old/')
        download_file(fire_url, './pdf/', pdf)
        if not filecmp.cmp('./pdf/' + pdf, './old/' + pdf, shallow=True):
            print('Updated File!', pdf)
            generate_images_from_pdf('./pdf/', pdf, './image/')
        else:
            print('No Changes: ', pdf)
