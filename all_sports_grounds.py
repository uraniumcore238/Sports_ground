import urllib
import requests
import urllib.request
import tempfile, os, zipfile
import requests
import local_settings


def get_all_sportsground():

    print('Beginning file download with requests')

    url = local_settings.SOURCE_URL

    # r = requests.get(url)
    # with open('D:/Programming/Sports_ground/first.json', 'wb') as f:
    #     f.write(r.content)

    response = requests.get(url)

    file = tempfile.TemporaryFile()
    file.write(response.content)
    fzip = zipfile.ZipFile(file)
    fzip.extractall('./')
    file.close()
    fzip.close()


if __name__ == "__main__":    
    get_all_sportsground()


