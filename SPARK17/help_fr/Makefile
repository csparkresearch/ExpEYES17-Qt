DESTDIR =
LANG = fr
JEKYLL = jekyll
STATIC_OUTPUTDIR = MD_HTML

all:
	for f in $$(find ../help| grep -v $(STATIC_OUTPUTDIR)); do \
	  g=$$(echo $$f | sed 's%../help%.%'); \
	  if [ ! -e "$$g" ]; then \
	    if [ -f "$$f" ]; then \
	      echo "symlinking $$g ==> $$f"; \
	      ln -sr "$$f" "$$g"; \
	     fi; \
	  fi; \
	done
	mkdir -p $(STATIC_OUTPUTDIR)
	$(JEKYLL) build

clean:
	rm -rf $(STATIC_OUTPUTDIR)

install:
	install -d $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)
	cp -a $(STATIC_OUTPUTDIR)/* $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)

.PHONY: all clean install
