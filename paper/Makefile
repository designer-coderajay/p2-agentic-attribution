# P2 manuscript. `make` builds main.pdf, `make clean` removes every artifact.
# latexmk runs pdflatex and bibtex as many times as needed to resolve
# references, so a one-pass build never ships with unresolved citations.

.PHONY: all clean check

all: main.pdf

main.pdf: main.tex refs.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

# Fails if anything is unresolved. Run this before sending a draft anywhere:
# an undefined citation renders as [?] and is easy to miss in a 20-page PDF.
check: main.pdf
	@if grep -qE 'Citation .* undefined|Reference .* undefined' main.log; then \
	  echo "UNRESOLVED references or citations:"; \
	  grep -E 'Citation .* undefined|Reference .* undefined' main.log; \
	  exit 1; \
	else echo "all references and citations resolved"; fi

clean:
	latexmk -C
	rm -f main.bbl main.blg
