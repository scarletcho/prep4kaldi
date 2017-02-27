# prep4kaldi
Data preparation code for building Kaldi ASR system.
</br>

## What it does
These codes help data preparation for building an ASR system in Kaldi by creating 'text', 'utt2spk', 'segments', and 'wav.scp' under 'required' folder.

## Inputs to be specified   
(1) **datadir**  
- Directory path of where subfolders named by speaker ids are located.  

	e.g. Given /Users/cho/mycorpus/,  
  				├─ s01/			  
  				├─ s02/		NB. each subfolder includes its corresponding speaker's  
  				├─ s03/			-> recordings (.wav)  
  				├─ ...			-> textgrids (.TextGrid)
				├─ s19/			  
				└─ s20/  

		Specify as:
			$ datadir='/Users/cho/mycorpus/'

(2) **tiername**  
- Name of TextGrid tier to extract labels from.

	e.g. 'utterance', 'sent', ...

## Usage
After specifying 'datadir' and 'tiername' in *prep4kaldi.sh*, type the following command:

	$ sh prep4kaldi.sh

