TEXFILE = main

$(TEXFILE).pdf: $(TEXFILE).tex
	latexmk -xelatex -output-directory=tex_files $(TEXFILE)

view: $(TEXFILE).pdf
	evince tex_files/$(TEXFILE).pdf &

test:
	python3 network-simulator/tkinter/GUI.py

clean:
	rm -rfv tex_files
