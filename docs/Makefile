RM=rm -rf

all: plan.pdf report.pdf

plan.pdf: plan.tex
	pdflatex $^

report.pdf: report.tex
	pdflatex $^

clean:
	$(RM) *.pdf *.aux *.log *.out *.toc
