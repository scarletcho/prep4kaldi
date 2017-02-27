# -*- coding: utf-8 -*-

'''
wavtxt2info.py
~~~~~~~~~~

This script extracts a tab delimited utterance information (uttinfo.txt)
from .wav and .txt files in a specific directory.

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

Input:  Full path of the corpora

Usage:  $ python wavtxt2text.py '/Users/Scarlet_Mac/mycorpus/'

Yejin Cho (scarletcho@gmail.com)

Created: 2017-02-21
Last updated: 2017-02-27
'''

import sys
import os
import glob
import re
import math
import wave
import contextlib
from kolm.utils import readfileUTF8
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


def getWavDuration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    return duration


def getInfo_wavtxt(datadir):
    # Add slash('/') if datadir is specified without final slash
    if datadir[-1] != '/':
        datadir = datadir + '/'

    os.chdir(datadir)
    dirs = glob.glob('*/')
    stack = []

    for subdir in dirs:
        print('Working on ' + subdir)
        os.chdir(datadir + subdir)
        txtlist = glob.glob('*.txt')

        # For each text and wav
        for file_id in range(0, len(txtlist)):
            fname_txt_ext = txtlist[file_id]
            fname = re.sub('\..+', '', fname_txt_ext)
            fname_wav_ext = fname + '.wav'

            txt = readfileUTF8(fname_txt_ext)
            dur = getWavDuration(fname_wav_ext)

            # Get time range
            t_init_sec = 0.0
            t_end_sec = math.floor(float(dur)*100)/100

            # Codify seconds into 6 digit numbers
            t_init_code = u'000000'
            t_end_code = codify6digits(int(t_end_sec * 100))

            # info (7 columns total)
            record_id = fname
            utt_id = fname + '-' + t_init_code + '-' + t_end_code
            spk_id = re.sub('/', '', subdir)
            textlabel = ''.join(txt)
            seg_beg = str(t_init_sec)
            seg_end = str(t_end_sec)
            extended_fname = datadir + spk_id + '/' + fname + '.wav'

            # if not re.match(exclude_pattern, textlabel):
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
# ----------------------------------------------------- #

# Get information from wavs and txts
getInfo_wavtxt(datadir)

