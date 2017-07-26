DESTDIR =
SUBDIRS = templates utilities expeyes
PYLUPDATE = pylupdate5
PRO_FILE = spark17.pro
TS_FILES = $(shell ls lang/*.ts)
QM_FILES = $(patsubst %.ts, %.qm, $(TS_FILES))
TS_SOURCES = $(shell find . -name "*.py")

all: recursive_all lang

lang: $(TS_FILES) $(QM_FILES)

$(QM_FILES): $(TS_FILES)
	lrelease $(PRO_FILE)

$(TS_FILES): $(TS_SOURCES)
	echo -n "# GENERATED FILE, DO NOT EDIT\nSOURCES = " > $(PRO_FILE)
	find . -name "*.py" | xargs echo >> $(PRO_FILE)
	echo -n "TRANSLATIONS = " >> $(PRO_FILE)
	find lang -name "*.ts" | xargs echo >> $(PRO_FILE)
	$(PYLUPDATE) $(PRO_FILE)
	
recursive_all:
	for d in $(SUBDIRS); do make PYUIC=$(PYUIC) PYRCC=$(PYRCC) -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do make -C $$d clean; done

.PHONY: all recursive_all clean recursive_clean lang

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

