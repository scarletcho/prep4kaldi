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
- Before running prep4kaldi.sh, please check out the input section and modify to fit your needs.

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
		-> textgrids (.TextGrid)  
- Then, specify as:

	`$ datadir='/Users/cho/mycorpus/'`

(2) **datatype**
- Type of data from which information should be extracted.
- Please choose between 'textgrid' or 'wavtxt'.
- For instance:

	`$ datatype='textgrid'`

(3) **tiername**  
- Name of TextGrid tier to extract labels from.
- For example, if the transcriptions need to be extracted from 'utterance' tier, specify as:

	`$ tiername='utterance'`

## Usage
After specifying 'datadir', 'datatype', and 'tiername' in *prep4kaldi.sh*, type the following command:

	$ sh prep4kaldi.sh

