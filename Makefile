ADDON = animated-graphs.ankiaddon
PY_FILES = $(wildcard *.py)

$(ADDON): $(PY_FILES)
	zip $(ADDON) $(PY_FILES)