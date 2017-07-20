QT_VERSION?='PyQt4'
export QT_VERSION

ifeq ($(QT_VERSION), 'PyQt5')
  echo $(QT_VERSION)
  PYUIC = pyuic5
  PYRCC = pyrcc5
else ifeq ($(QT_VERSION), 'PyQt4')
  PYUIC = pyuic4
  PYRCC = pyrcc4
else
  PYUIC = pyuic4
  PYRCC = pyrcc4
endif

DESTDIR =
SUBDIRS = SPARK17

all: recursive_all

recursive_all:
	for d in $(SUBDIRS); do make PYUIC=$(PYUIC) PYRCC=$(PYRCC) -C $$d all; done

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
	python3 setup.py install --install-layout=deb \
	         --root=$(DESTDIR)/ --prefix=/usr

