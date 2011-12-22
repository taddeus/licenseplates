RM=rm -rf

all: plan.pdf report.pdf presentation_lbp.pdf presentation.pdf

%.pdf: %.tex
	pdflatex $^
	pdflatex $^

clean:
	$(RM) *.pdf *.aux *.log *.out *.toc *.snm *.nav
