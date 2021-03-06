import sys
import os
import re
import shutil
import signal
import logging

import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
from tqdm import tqdm


class LorGallery:
    def __init__(self, url='https://www.linux.org.ru', archive='/gallery/archive/', debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

        self.lor = url
        self.archive = archive
        self.re_link = r"\/gallery\/archive\/(\d+)\/(\d+)\/"
        self.user_dir = os.path.expanduser("~") + '/' + __name__ + '/'
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def get_list_archive(self):
        request = requests.get(self.lor + self.archive)

        if request.status_code != 200:
            print('lor servers is not answer')
            sys.exit(0)

        len_archive = len(set(re.findall(self.re_link, request.text))) - 1

        soup_object = self.get_soup_object(request.text)
        archive_container = soup_object.findAll('a', href=True)

        signal.signal(signal.SIGINT, self.signal_handler)
        print('Press Ctrl+C for exit script')

        for link in archive_container:
            href =  str(link['href'])

            if re.search(self.re_link, href) != None:
                numbers = re.findall(self.re_link, href)
                year = numbers[0][0]
                month = numbers[0][1]

                print('Start download at ' + str(year) + ' year and ' + str(month) + ' month:')
                request = requests.get(self.lor + href)

                if request.status_code != 200:
                    print('lor servers is not answer')

                dir = os.path.join(self.user_dir, href.replace('/', '_')[1:-1])

                if not os.path.exists(dir):
                    os.makedirs(dir)

                soup_object_self = self.get_soup_object(request.text)
                for post in tqdm(soup_object_self.findAll('article', {'class':'news'})):
                    # get message box with image and description datas
                    msg = post.find('div', {'class':'msg'})
                    # get post soup object
                    post_obj = self.get_soup_object(str(msg))
                    # author box soup object
                    author_box = post.find('div', {'class':'sign'}).text.split()
                    # author name string
                    author = author_box[0]
                    # create post time string
                    time_create = author_box[1].replace('(', '')
                    # get description string
                    description = post_obj.find('p').text
                    # name for save files (png and txt)
                    name_files = author + '_' + time_create
                    # save txt with description string
                    self.write_description(description, dir, name_files)
                    # get image link from object
                    image_link = post_obj.find('a', {'itemprop':'contentURL'}, href=True)
                    # save image
                    self.download_image(image_link['href'], dir, name_files)

    def download_image(self, url, path, name):
        response = requests.get(url, stream=True)
        with open(os.path.join(self.user_dir, path, '{}.png'.format(name)), 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

    def write_description(self, text, path, name):
        with open(os.path.join(self.user_dir, path, '{}.txt'.format(name)), 'w') as file:
            file.write(self.remove_last_line_from_string(text))
            file.close()

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    """ For remove child paragraph (bug bs4 or bug html lor :) - http://imgur.com/ZTWSh6D, http://imgur.com/nO84DLv) """
    def remove_last_line_from_string(self,s):
        s = s.split('\n')[:5]
        return '\n'.join(s)

    def get_soup_object(self, html):
        return BeautifulSoup(html, 'html.parser')

