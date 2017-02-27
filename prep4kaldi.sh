#!/usr/bin/env bash
# ~~~~~~~~~
# prep4kaldi.sh
# ~~~~~~~~~

# This script helps data preparation for building an ASR system in Kaldi
# by creating 'text', 'utt2spk', 'segments', and 'wav.scp' under 'required' folder.

# Inputs to be specified: 
# (1) datadir
#	- Directory path of where subfolders named by speaker ids are located.
#	e.g. Given /Users/cho/mycorpus/,
#				├─ s01/			
#				├─ s02/		NB. each subfolder includes
#				├─ s03/			its corresponding speaker's
#				├─ ...			-> recordings (.wav)
#				├─ s19/			-> textgrids (.TextGrid)
#				└─ s20/
#
#		Specify as:
#			$ datadir='/Users/cho/mycorpus/'
#
# (2) datatype
#   - Type of data from which information should be extracted.
#   - Please choose between 'textgrid' or 'wavtxt'.
#
# (2) tiername
#	- Name of TextGrid tier to extract labels from (if datatype is specified as 'textgrid').
#	e.g. 'utterance', 'sent', ...
#
# Usage: $ sh prep4kaldi.sh

# Created: 2017-02-27
# Last updated: 2017-02-27

# Yejin Cho (scarletcho@gmail.com)
# ─────────────────────────────────────────────────────────────────────────
# Input section
datadir='/Users/Scarlet_Mac/krss/wavtxt/read/'
datatype='wavtxt'
tiername='utt.ortho'

# ─────────────────────────────────────────────────────────────────────────
# STEP1
echo '[STEP1] Extract uttinfo.txt from .TextGrids in $datadir'
case $datatype in
    textgrid)
        # When extracting info from TextGrids:
        python textgrid2info.py "$datadir" "$tiername"
        ;;
    wavtxt)
        # When extracting info from wavs and txts:
        python wavtxt2info.py "$datadir"
        ;;
    *)
        echo -n "Please specify your datatype as 'textgrid' of 'wavtxt'."
        ;;
esac

cd $datadir
mkdir required

# NB. Information structure of uttinfo.txt (tsv):
	# field 1. <extended-filename>
	# field 2. <recording-id>
	# field 3. <utterance-id>
	# field 4. <speaker-id>
	# field 5. <transcription>
	# field 6. <segment-begin (in sec)>
	# field 7. <segment-end (in sec)>

# ─────────────────────────────────────────────────────────────────────────
# STEP2
echo '[STEP2] Organize collected info to create: 'text', 'utt2spk', 'segments', and 'wav.scp''

# (1) 'text': <utt-id> <transcription>
cut -f 3,5 uttinfo.txt | tr '\t' ' ' > ./required/text

# (2) 'utt2spk': <utt-id> <spk-id>
cut -f 3,4 uttinfo.txt | tr '\t' ' ' > ./required/utt2spk

# (3) 'segments': <utt-id> <rec-id> <seg-beg> <seg-end>
cut -f 3,2,6,7 uttinfo.txt | tr '\t' ' ' > ./required/segments

# (4) 'wav.scp': <rec-id> <extended-fname>
cut -f 2,1 uttinfo.txt | tr '\t' ' ' > ./required/wav.scp

# ─────────────────────────────────────────────────────────────────────────
echo 'Kaldi data preparation has successfully COMPLETED!'
