# EE

This repo is for the extended essay.

```
.
├── citations.bib					# biblatex citation
├── figures							# Figures for latex
├── implementation					# Code
│   ├── experiment					# More figures for latex
│   ├── arrays						# Saved array data 
│   ├── chroma generate images.py	# Script to generate color space figures
│   ├── chroma subsampling.py		# JFIF 1
│   ├── dct.py						# JFIF 2
│   ├── Photos						# Sample photos, pixels must be in factors of 32
│   │   ├── *.bmp					# resized
│   │   ├── *.CR2					# RAW
│   └── quantization table			# Quantization Tables for DCT, higher the number, the less compression
│       ├── ps00c.csv				# Photoshop save as, 00 quality, chroma
│       ├── ps00l.csv				# Photoshop save as, 00 quality, luma
│       ├── ps010c.csv				# Photoshop save to web, 010 quality, chroma
│       ├── ps010l.csv				# Photoshop save to web, 010 quality, luma
├── main.pdf
├── main.tex						# Main tex file
└── README.md
```
