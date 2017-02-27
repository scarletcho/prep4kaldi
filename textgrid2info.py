# -*- coding: utf-8 -*-

'''
textgrid2info.py
~~~~~~~~~~

This script extracts a tab delimited utterance information (uttinfo.txt)
from .TextGrid files in a specific directory.

The extracted information includes 7 fields in total:

=================================================================
[ Information structure of uttinfo.txt (tsv) ]
  field 1. <extended-filename>
  field 2. <recording-id>
  field 3. <utterance-id>
  field 4. <speaker-id>
  field 5. <transcription>
  field 6. <segment-begin (in sec)>
  field 7. <segment-end (in sec)>
  -> < Each row > includes a set of information about
     < a single utterance >, which is delimited by newlines(\n).
=================================================================

Input:  (1) Full path of the corpora, and
        (2) the name of tier to be extracted should be specified.

Usage:  $ python textgrid2text.py '/Users/Scarlet_Mac/mycorpus/' 'utt.ortho'

Yejin Cho (scarletcho@gmail.com)

Created: 2017-02-21
Last updated: 2017-02-27
'''

import sys
import os
import glob
import re
import math
from konlpy.utils import pprint
from kolm.utils import convertEncoding
from kolm.utils import writefile

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass


def readTextGridUTF8(fname, tiername):
    f = open(fname, 'r')
    corpus = []
    lines = f.readlines()
    begin = lines.index('"'+ tiername + '"\n')
    end_indices = [i for i, x in enumerate(lines) if re.search('"IntervalTier"\n', x)]

    # Find the next higher IntervalTier index after 'begin' index
    for n in end_indices:
        if n > begin:
            end = n
            break

    try:
        end
    except NameError:
        end = len(lines) - 1

    for m in range(begin + 1, end):
        line = lines[m]
        # if line[0] == "\"":
        line = line.encode('utf-8')
        line = re.sub(u'\n', u'', line)
        line = re.sub(u'\"', u'', line)
        corpus.append(line)

    # Delete the first 3 items which include:
    #   - (item #1) beginning time info of the audio file
    #   - (item #2) end time info of the audio file
    #   - (item #3) total number of intervals
    corpus[0:3] = []

    f.close()
    return corpus


def codify6digits(floats):
    if sys.version_info[0] == 2:
        numstr = unicode(str(floats))
    else:
        numstr = str(floats)
    while len(numstr) < 6:
        numstr = u'0' + numstr

    return numstr


def getInfo(datadir, tiername, exclude_pattern):
    # Add slash('/'') if datadir is specified without final slash
    if datadir[-1] != '/':
        datadir = datadir + '/'

    os.chdir(datadir)
    dirs = glob.glob('*/')
    stack = []

    for subdir in dirs:
        print('Working on ' + subdir)
        os.chdir(datadir + subdir)
        gridlist = glob.glob('*.TextGrid')

        # (1) For each TextGrid
        for file_id in range(0, len(gridlist)):
            fname_ext = gridlist[file_id]
            fname = re.sub('\..+', '', fname_ext)
            txt = readTextGridUTF8(fname_ext, tiername)

            # (2) For each labels
            for x in range(0, len(txt)-2, 3):
                # Get time range
                t_init_sec = math.floor(float(txt[x])*100)/100
                t_end_sec = math.floor(float(txt[x+1])*100)/100

                # Codify seconds into 6 digit numbers
                t_init_code = codify6digits(int(t_init_sec * 100))
                t_end_code = codify6digits(int(t_end_sec * 100))

                # info (7 columns total)
                record_id = fname
                utt_id = fname + '-' + t_init_code + '-' + t_end_code
                spk_id = re.sub('/', '', subdir)
                textlabel = txt[x+2]
                seg_beg = str(t_init_sec)
                seg_end = str(t_end_sec)
                extended_fname = datadir + spk_id + '/' + fname + '.wav'

                if not re.match(exclude_pattern, textlabel):
                    stack.append(extended_fname + u'\t'
                                 + record_id + u'\t'
                                 + utt_id + u'\t'
                                 + spk_id + u'\t'
                                 + textlabel + u'\t'
                                 + seg_beg + u'\t' + seg_end)

    os.chdir(datadir)
    writefile(stack, 'uttinfo.txt')


# ----------------------------------------------------- #
# Input arguments:
datadir = sys.argv[1]
tiername = sys.argv[2]
exclude_pattern = u'(<[^>]+> ?)+'
# ----------------------------------------------------- #

# Get information from TextGrids
getInfo(datadir, tiername, exclude_pattern)

