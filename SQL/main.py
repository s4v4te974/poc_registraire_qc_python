import const as ct
import cloudscraper
import zipfile


def download_files():
    scraper = cloudscraper.create_scraper()
    response = scraper.get(ct.URL_REGISTRE, headers=ct.HEADERS)
    if response.status_code == 200:
        print(ct.CONNEXION_SUCCESS, response.status_code)
        content = response.content
        with open(ct.DOWNLOAD_FILE_PATH, 'wb') as file:
            file.write(content)
        print(ct.DOWNLOAD_SUCCESS)
    else:
        print(ct.FAILED_TO_DOWNLOAD, response.status_code)

def unzip_files():
    with zipfile.ZipFile(ct.DOWNLOAD_FILE_PATH, 'r') as jdzip:
        jdzip.extractall(ct.)



def download_and_unzip_files():
    download_files()
    unzip_files()

