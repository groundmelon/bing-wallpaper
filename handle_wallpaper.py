# -*- coding: utf-8 -*-
MAX_IMAGE_NUMBER = 7
BING_GALLERY_URL = r"http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=20&mkt=zh-cn"

import requests
import datetime
import time
import glob
import os
import sys
import argparse
import random
import logging
import logging.handlers
from PIL import Image
from StringIO import StringIO


FILEPATH = os.path.join(os.path.expanduser("~"), 'Pictures/bing-wallpaper')
os.chdir(FILEPATH)


formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")


def download_pictures():
    logger = logging.getLogger("download_pictures")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        "{}.log".format("download_pictures"), mode='w', encoding=None, delay=0)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        f = requests.get(BING_GALLERY_URL)
        logger.debug(u'json url opened\n')
        d = f.json()
        req_idx = 0
        while True:
            files = glob.glob(r'*.jpg')
            files.sort()

            imageurl = r'http://www.bing.com' + d[u'images'][req_idx][u'url']
            logger.debug(u'image url <%s>\n' % imageurl)
            logger.info(u'copyright: {}\n'.format(
                d[u'images'][req_idx][u'copyright']).encode('utf8'))

            fname = d[u'images'][req_idx][u'startdate'] + '.jpg'
            if fname not in files:
                r = requests.get(imageurl)
                img = Image.open(StringIO(r.content))
                img.save(fname)
                logger.debug(u'file %s saved\n' % fname)
            else:
                logger.debug(u'file %s exist\n' % fname)

            files = glob.glob(r'*.jpg')
            files.sort()
            if len(files) > MAX_IMAGE_NUMBER:
                try:
                    os.remove(files[0])
                    logger.debug('Delete %s\n' % files[0])
                except Exception, e:
                    logger.debug('Del %s error.[%s] Break.\n' % (files[0], str(e)))
                    break
            elif len(files) < MAX_IMAGE_NUMBER:
                logger.debug('There is %d files.\n' % len(files))
                req_idx += 1
            else:
                break
    except Exception, e:
        logger.error(u'{}'.format(str(e)))
        sys.exit(str(e))
    else:
        sys.exit(0)


def change_wallpaper():
    logger = logging.getLogger("change_wallpaper")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        u"{}.log".format("change_wallpaper"), mode='a', maxBytes=1024 * 10, backupCount=1)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    CURRENT_PIC_FILE_NAME = u"current_pic.txt"
    fname = None
    try:
        idfile = open(CURRENT_PIC_FILE_NAME, 'r')
        fname = idfile.read()
        idfile.close()
    except IOError as e:
        pass

    files = glob.glob(r'*.jpg')

    if len(files) == 0:
        return

    if fname in files:
        files.remove(fname)
        logger.debug("random pick exclude {}".format(fname))

    if len(files) == 0:
        fname = fname
    else:
        idx = random.randint(0, len(files) - 1)
        fname = files[idx]

    try:
        logger.debug("random picked {}".format(fname))
        idfile = open(CURRENT_PIC_FILE_NAME, 'w')
        idfile.write(fname)
        idfile.close()
    except IOError as e:
        pass

    # http://askubuntu.com/questions/140305/cron-not-able-to-succesfully-change-background
    os.system(
        ''' export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/`pgrep gnome-session`/environ|cut -d= -f2-); 
            gsettings set org.gnome.desktop.background picture-uri file://{pic_path}'''.format(
            pic_path=os.path.join(FILEPATH, fname)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--change", action="store_true", help="change desktop background")
    group.add_argument("-d", "--download", action="store_true", help="download bing wallpapers")
    args = parser.parse_args()

    if args.change:
        change_wallpaper()

    if args.download:
        download_pictures()
