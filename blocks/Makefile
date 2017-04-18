# Main Makefile for Expeyes-Blocks

SUBDIRS = eyePlot doc

all: recursive_all lang

lang:
	pylupdate4 Expeyes-Blocks.pro
	cd eyeBlocks/lang; for f in *.ts; do lrelease $$f; done

recursive_all:
	for d in $(SUBDIRS); do make -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do make -C $$d clean; done

doc:
	make -f Makefile.sphinx html

.PHONY: all recursive_all clean recursive_clean doc lang
