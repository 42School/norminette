# List the pdf's to build. foo.tex will produce foo.pdf
TARGETS = en.norm.pdf fr.norme.pdf ko.norm.pdf

# List the files included in the slides
# DEPS = somePicture.png someSound.flac someOtherPicture.png
DEPS = 

# Relative path to the LaTeX documentclass setup files
# Adapt as needed
RELPATH = $(shell git rev-parse --show-toplevel)/resources/latex

# You should not touch this either
include $(RELPATH)/Makefile.LaTeX
