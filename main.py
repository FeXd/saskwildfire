from pdf2image import convert_from_path

fire_pdfs = [
    'http://environment.gov.sk.ca/firefiles/activefires.pdf',
    'http://environment.gov.sk.ca/firefiles/MunicipalFireBans.pdf',
    'http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/today_fwi.pdf',
    'http://environment.gov.sk.ca/firefiles/DailyFireDangerMaps/tomorrow_fwi.pdf',
]

local_pdfs = [
    './pdf/activefires.pdf',
    './pdf/MunicipalFireBans.pdf',
    './pdf/today_fwi.pdf',
    './pdf/tomorrow_fwi.pdf',
]

if __name__ == '__main__':
    for pdf_file in local_pdfs:
        images = convert_from_path(pdf_file)
        for i, image in enumerate(images):
            fname = pdf_file+str(i)+'.jpg'
            image.save(fname, "JPEG")
