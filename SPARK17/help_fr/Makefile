DESTDIR =
LANG = fr
JEKYLL = jekyll
STATIC_OUTPUTDIR = MD_HTML

all:
	# symlink missing files from ../help
	# when a file must be localized, one must replace
	# the symlink by a plain file, manually.
	for f in $$(find ../help| grep -v $(STATIC_OUTPUTDIR)); do \
	  g=$$(echo $$f | sed 's%../help%.%'); \
	  if [ ! -e "$$g" ]; then \
	     if [ -d "$$f" ]; then \
	      echo "create missing directory $$g"; \
		  mkdir -p "$$g"; \
		fi; \
	    if [ -f "$$f" ]; then \
	      echo "symlinking $$g ==> $$f"; \
	      ln -sr "$$f" "$$g"; \
	     fi; \
	  fi; \
	done
	# jekkyl will make plain copies so the symlinks are no
	# longer in the generated web pages.
	mkdir -p $(STATIC_OUTPUTDIR)
	$(JEKYLL) build

clean:
	rm -rf $(STATIC_OUTPUTDIR)

install:
	install -d $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)
	cp -a $(STATIC_OUTPUTDIR)/* $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)

.PHONY: all clean install
