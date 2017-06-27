DESTDIR =
SUBDIRS = templates utilities expeyes

all: recursive_all

recursive_all:
	for d in $(SUBDIRS); do make -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do make -C $$d clean; done

.PHONY: all recursive_all clean recursive_clean

install:
	mkdir -p $(DESTDIR)/usr/share/expeyes/eyes17
	cp -R *.* $(DESTDIR)/usr/share/expeyes/eyes17/
	cp -R experiments $(DESTDIR)/usr/share/expeyes/eyes17/experiments
	cp -R utilities $(DESTDIR)/usr/share/expeyes/eyes17/utilities
	cp -R help $(DESTDIR)/usr/share/expeyes/eyes17/help
	cp -R templates $(DESTDIR)/usr/share/expeyes/eyes17/templates
	cp ExpEYES17.desktop $(DESTDIR)/usr/share/applications/
	python setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr

