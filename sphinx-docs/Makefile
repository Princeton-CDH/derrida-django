# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Derrida
SOURCEDIR     = .
BUILDDIR      = .

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# build production documentation for publishing on github pages
# run the html build, then move to /docs/ folder and add to git
docs:
	rm -rf ../docs/*
	@make html
	mv html/* ../docs/
	touch ../docs/.nojekyll
	cd ../docs && git add --all && git commit -m "Publishing updated documentation on gh-pages" && cd ..


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
