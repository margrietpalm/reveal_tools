#!/usr/bin/env python
"""Clean up images folder for reveal presentation"""

# rom optparse import OptionParser
import argparse
import sys
import os
import glob
import shutil
import future
from itertools import groupby
from operator import itemgetter

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
    parser.add_argument('-q', '--quiet', dest="quiet", action="store_true", help="suppress output")
    parser.add_argument('-o', '--outfile', dest='outfile', default='notes.md')
    parser.add_argument('--to-pdf', action="store_true", help="convert to pdf")
    parser.add_argument('--to-html', action="store_true", help="convert to html")
    parser.add_argument('--number-slides', action="store_true")
    parser.add_argument('mdfile', nargs='?', default='slides.md', help="path to reveal base dir (default: %(default)s)")
    return parser.parse_args()


def get_structure(fn):
    f = open(fn)
    lines = f.readlines()
    blanks = [i for i, l in enumerate(lines) if len(l.strip()) == 0]
    sections = {1: []}
    section = 1
    i0 = 0
    for k, g in groupby(enumerate(blanks), lambda x: x[1] - x[0]):
        elines = list(map(itemgetter(1), g))
        if len(elines) < 2:
            continue
        text = ''.join([lines[i] for i in range(i0, elines[0])])
        sections[section].append(text)
        if len(elines) > 2:
            section += 1
            sections[section] = []
        i0 = elines[-1] + 1
    return sections


def extract_notes(sections, number_slides=False):
    notes = ''
    parts = list(sections.keys())
    parts.sort()
    for p in parts:
        notes += '# Part {}\n\n'.format(p)
        for i, slide in enumerate(sections[p], 1):
            lines = slide.split('\n')
            notes += '##'
            if number_slides:
                notes += '## {}.{} '.format(p, i)
            notes += lines[0] + '\n'
            inotes = len(lines)
            for j, l in enumerate(lines):
                if l.startswith('Note:'):
                    inotes = j
                    break
            for j in range(inotes + 1, len(lines)):
                notes += lines[j] + '\n'
            notes += '\n'
    return notes


def main():
    opt = parse_args()
    sections = get_structure(opt.mdfile)
    notes = extract_notes(sections, opt.number_slides)
    f = open(opt.outfile, 'w')
    f.write(notes)
    f.close()

    if opt.to_pdf:
        template = '/' + '/'.join(os.path.realpath(__file__).split('/')[1:-1]) + '/templates/eisvogel.tex'
        os.system('pandoc {} -o {} --from gfm --template {} '
                  '--listings'.format(opt.outfile, opt.outfile.replace('.md', '.pdf'), template))
    if opt.to_html:
        os.system('pandoc {} -o {} --from gf'.format(opt.outfile, opt.outfile.replace('.md', '.html')))


if __name__ == "__main__":
    main()
