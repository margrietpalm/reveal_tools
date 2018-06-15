#!/usr/bin/env python
"""Clean up images folder for reveal presentation"""

#rom optparse import OptionParser
import argparse
import sys
import os
import glob
import shutil
import future

__author__ = "Margriet Palm"
__copyright__ = "Copyright 2018"
__credits__ = "Margriet Palm"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Margriet Palm"

def parse_args():
    # read arguments
    # create parser
    parser = argparse.ArgumentParser(description='Clean images folders')
    parser.add_argument('-q','--quiet',dest="quiet",action="store_true",help="suppress output")
    parser.add_argument('--imfolder',type=str,default="images/",help="path to images in reveal base dir (default: %(default)s)")
    parser.add_argument('--mdfolder',type=str,default="markdown/",help="path to markdown in reveal base dir (default: %(default)s)")
    parser.add_argument('--index',type=str,default="index.html",help="html index (default: %(default)s)")
    parser.add_argument('--delete',dest="delete",action="store_true",default=False,help="delete unused images (default: %(default)s)")
    parser.add_argument('path', nargs='?', default='./',help="path to reveal base dir (default: %(default)s)")
    return parser.parse_args()

def find_im_in_tag(text):
    i0 = text.find("src=\"")
    i1 = text.find("\"",i0+5)
    return(text[i0+5:i1].split('/')[-1])

def get_images_in_md_file(fn):
    text = open(fn,'r').read()
    i0 = text.find("<img")
    images = []
    while i0 > 0:
        images.append(find_im_in_tag(text[i0:text.find(">",i0)]))
        i0 = text.find("<img",i0+1)
    return images

def get_images_in_index_file(fn):
    text = open(fn,'r').read()
    i0 = text.find("data-background-image=\"")
    images = get_images_in_md_file(fn)
    while i0 > 0:
        i1 = text.find("\"",i0+23)
        images.append(text[i0+23:i1].split('/')[-1])
        i0 = text.find("data-background-image=\"",i1)
    return images

def get_all_images(path,mdfolder,index_file):
    images = []
    for fn in glob.glob('{}/{}/*.md'.format(path,mdfolder)):
        images = images+get_images_in_md_file(fn)
    return set(images + get_images_in_index_file(path+'/'+index_file))

def get_permission(nfiles):
    ntries = 0
    valid = False
    while (ntries < 5) and not valid:
        answer = input("Do you want to delete {} files? (y/n): ".format(nfiles)).lower()
        if answer in ['y','n','yes','no']:
            valid = True
            if answer in ['y','yes']:
                return True
            else:
                return False
        else:
            ntries += 1
    return False


def clean_im_dir(imdir,images,delete=False,quiet=True):
    unused = [im.split('/')[-1] for im in glob.glob(imdir+'/*.*') if im.split('/')[-1] not in images]
    if not delete and not os.path.isdir('{}/bak/'.format(imdir)):
        os.mkdir('{}/bak/'.format(imdir))
    elif delete:
        get_permission(len(unused))
    for fn in unused:
        if delete:
            if not quiet:
                print('delete {}'.format(fn))
            os.remove(imdir+fn)
        else:
            if not quiet:
                print('move {} to {}/bak/'.format(fn,imdir))
            shutil.move(imdir+fn,'{}/bak/'.format(imdir))


def main():
    # get command-line arguments
    opt = parse_args()
    images = get_all_images(opt.path,opt.mdfolder,opt.index)
    clean_im_dir(opt.path+'/'+opt.imfolder,images,opt.delete,opt.quiet)

if __name__ == "__main__":
    main()
