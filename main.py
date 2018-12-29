import string
import random
from bs4 import BeautifulSoup
import shutil
import os
import requests
import time

from multiprocessing.dummy import Pool as ThreadPool

noneWorking = [0, 11809]

userhome = os.path.expanduser('~')
desktop = userhome + '/Desktop/Pictures_From_PRNSTCRN/'

if not os.path.exists(desktop):
    os.makedirs(desktop)


def get_html(code):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        response = requests.get('https://prnt.sc/' + code, headers=headers, timeout=5)
        return response.text
    except:
        time.sleep(10)
        print("ReadTimeout - Sleep for 10 sec")
        get_code(code_old)


def RandomNumber(col, size=6, chars=string.ascii_lowercase + string.digits):
    code = ''
    for a in range(col):
        code = ''.join(random.choice(chars) for _ in range(size))
    return code


def main(col):
    while True:
        code = RandomNumber(1)
        html = get_html(code)
        soup = BeautifulSoup(html, 'lxml')

        try:
            line = soup.find('img', class_='screenshot-image')['src']

            # Get name file
            txt = line.replace('https://i.imgur.com/', '')
            txt = txt.replace('https://i.imgur.com/', '')
            txt = txt.replace('https://image.prntscr.com/image/', '')

            # Check for remove image
            if '0_173a7b_211be8ff.png' in txt:
                pass
            else:
                response = requests.get(line, stream=True)

                # Save image
                with open(desktop + txt, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                size = os.path.getsize(desktop + txt)

                # Check for remove image
                if size in noneWorking:
                    print("[-] Invalid: " + str(code))
                    os.remove(desktop + txt)
                else:
                    print("[+] Valid: " + str(code))
        except TypeError:
            print("ERROR - TypeError - " + str(code))


if __name__ == '__main__':
    pool = ThreadPool(5)
    # Use [1,2,3,4,5] only for multiprocessing
    pool.map(main, [1,2,3,4,5])
