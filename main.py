import requests
import shutil
from pdf2image import convert_from_path

fire_url = 'http://environment.gov.sk.ca/firefiles/'

fire_pdfs = [
    'activefires.pdf',
    'MunicipalFireBans.pdf',
    'DailyFireDangerMaps/today_fwi.pdf',
    'DailyFireDangerMaps/tomorrow_fwi.pdf',
]


def download_files(url, path, files):
    for file in files:
        response = requests.get(url+file, stream=True)
        write_file = open(path+file, 'wb')
        write_file.write(response.content)
        write_file.close()


def move_files(path, files, new_path):
    for file in files:
        shutil.move(path+file, new_path+file)


def generate_images_from_pdfs(in_path, pdfs, out_path):
    for pdf in pdfs:
        images = convert_from_path(in_path+pdf)
        for i, image in enumerate(images):
            fname = pdf+str(i)+'.jpg'
            image.save(out_path+fname, "JPEG")


if __name__ == '__main__':
    move_files('./pdf/', fire_pdfs, './old/')
    download_files(fire_url, './pdf/', fire_pdfs)
    generate_images_from_pdfs('./pdf/', fire_pdfs, './image/')
