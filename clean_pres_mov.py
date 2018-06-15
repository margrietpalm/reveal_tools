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
    parser.add_argument('--movfolder',type=str,default="movies/",help="path to movies in reveal base dir (default: %(default)s)")
    parser.add_argument('--mdfolder',type=str,default="markdown/",help="path to markdown in reveal base dir (default: %(default)s)")
    parser.add_argument('--index',type=str,default="index.html",help="html index (default: %(default)s)")
    parser.add_argument('--delete',dest="delete",action="store_true",default=False,help="delete unused images (default: %(default)s)")
    parser.add_argument('path', nargs='?', default='./',help="path to reveal base dir (default: %(default)s)")
    return parser.parse_args()

def find_vid_in_tag(text):
    i0 = text.find("src=\"")
    i1 = text.find("\"",i0+5)
    return(text[i0+5:i1].split('/')[-1])

def get_videos_in_md_file(fn):
    text = open(fn,'r').read()
    i0 = text.find("<video")
    movies = []
    while i0 > 0:
        movies.append(find_vid_in_tag(text[i0:text.find("</video>",i0)]))
        i0 = text.find("<video",i0+1)
    return movies


def get_all_movies(path,mdfolder):
    movies = []
    for fn in glob.glob('{}/{}/*.md'.format(path,mdfolder)):
        movies = movies+get_videos_in_md_file(fn)
    return set(movies)

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


def clean_movies_dir(movdir,movies,delete=False,quiet=True):
    unused = [mov.split('/')[-1] for mov in glob.glob(movdir+'/*.*') if mov.split('/')[-1] not in movies]
    if not delete and not os.path.isdir('{}/bak/'.format(movdir)):
        os.mkdir('{}/bak/'.format(movdir))
    elif delete:
        get_permission(len(unused))
    for fn in unused:
        if delete:
            if not quiet:
                print('delete {}'.format(fn))
            os.remove(movdir+fn)
        else:
            if not quiet:
                print('move {} to {}/bak/'.format(fn,movdir))
            shutil.move(movdir+fn,'{}/bak/'.format(movdir))


def main():
    # get command-line arguments
    opt = parse_args()
    movies = get_all_movies(opt.path,opt.mdfolder)
    print(movies)
    clean_movies_dir(opt.path+'/'+opt.movfolder,movies,opt.delete,opt.quiet)

if __name__ == "__main__":
    main()
