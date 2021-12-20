import json
import urllib
from idlelib.multicall import r

import requests
import urllib.request
import tempfile, os, zipfile
import requests
import local_settings


def get_all_sportsground():

    url = local_settings.SOURCE_URL

    response = requests.get(url)
    zfile = tempfile.TemporaryFile()
    zfile.write(response.content)
    with zipfile.ZipFile(zfile, 'r') as zip:
        for name in zip.namelist():
            with zip.open(name) as f:
                content = f.read()
                fullpath = os.path.join(os.getcwd(), name)
                with open(fullpath, 'wb') as f:
                    f.write(content)



if __name__ == "__main__":    
    get_all_sportsground()


