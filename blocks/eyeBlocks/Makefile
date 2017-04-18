SUBDIRS = templates

all: recursive_all

recursive_all:
	for d in $(SUBDIRS); do make -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do make -C $$d clean; done

.PHONY: all recursive_all clean recursive_clean
