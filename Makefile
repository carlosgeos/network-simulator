TEXFILE = main

$(TEXFILE).pdf: $(TEXFILE).tex
	latexmk -xelatex -output-directory=tex_files $(TEXFILE)

view: $(TEXFILE).pdf
	evince tex_files/$(TEXFILE).pdf &

clean:
	rm -fv *.aux *.log *.toc *.blg *.bbl *.synctex.gz
	rm -fv *.out *.bcf *blx.bib *.run.xml
	rm -fv *.fdb_latexmk *.fls
	rm -fv $(TEXFILE).pdf
