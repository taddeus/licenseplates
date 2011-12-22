RM=rm -rf

all: plan.pdf report.pdf

plan.pdf: plan.tex
	pdflatex $^
	pdflatex $^

report.pdf: report.tex
	pdflatex $^
	pdflatex $^

clean:
	$(RM) *.pdf *.aux *.log *.out *.toc
