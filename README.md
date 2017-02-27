# prep4kaldi
Data preparation code for building Kaldi ASR system.
</br>

## What it does
These codes help data preparation for building an ASR system in Kaldi by creating the following text files within 'required' folder:
- Files created:  
	- text  
	- utt2spk  
	- segments  
	- wav.scp  

## Inputs to be specified   
- Before running prep4kaldi.sh, please check out the **input section** and modify to fit your needs.

(1) **datadir**  
- Directory path of where subfolders named by speaker ids are located.
- For example, given a corpus in the following directory:  
>	/Users/cho/mycorpus/,  
	&nbsp;&nbsp;&nbsp;&nbsp;├─ s01/  
	&nbsp;&nbsp;&nbsp;&nbsp;├─ s02/  
	&nbsp;&nbsp;&nbsp;&nbsp;├─ s03/  
	&nbsp;&nbsp;&nbsp;&nbsp;├─ ...  
	&nbsp;&nbsp;&nbsp;&nbsp;├─ s19/  
	&nbsp;&nbsp;&nbsp;&nbsp;└─ s20/  
	
		NB. each subfolder includes its corresponding speaker's  
		-> recordings (.wav)  
		-> transcriptions (.txt) or textgrids (.TextGrid)  
		
- Then, your datadir should be specified as '/Users/cho/mycorpus/'.

(2) **datatype**
- Type of data from which information should be extracted.
- Please choose between 'textgrid' or 'wavtxt'.

(3) **tiername**  
- Name of TextGrid tier to extract labels from.


## Usage
After specifying 'datadir', 'datatype', and 'tiername' in *prep4kaldi.sh*, type the following command:

	$ sh prep4kaldi.sh <datadir> <datatype> <tiername>

	# EXAMPLES
	# CASE 1: Gather info from a tier in textgrids named 'utt.ortho'
	$ sh prep4kaldi.sh /Users/cho/mycorpus/ textgrid utt.ortho
	
	# CASE 2: Gather info from a set of wav & txt files (thus no need to specify <tiername>)
	$ sh prep4kaldi.sh /Users/cho/mycorpus/ wavtxt

