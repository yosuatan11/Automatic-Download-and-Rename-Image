import requests
import os
import csv


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print(destination)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    nama = []
    link = []
    path = input('Masukan path dari file yang ingin di simpan = ')

    if not os.path.exists(path):
        os.makedirs(path)

    file = input('Masukan nama dari file csv = ')

    with open(file + '.csv') as data:
        csvReader = csv.reader(data)
        for row in csvReader:
            download_file_from_google_drive(row[1].split('?id=')[1], path+'\\'+row[0]+'.jpg')

    print('Download Complete!')

# USAGE
# python download.py  'SharableLink of google drive file' ' outputFileName'
# python download.py 'https://docs.google.com/uc?export=download&id=1H583z6qDwmrbb9_OYRL05EA2FKVqY8C0' 'world1.tif'