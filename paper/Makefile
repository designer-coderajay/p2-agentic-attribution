# P2 manuscript. `make` builds main.pdf, `make clean` removes every artifact.
# latexmk runs pdflatex and bibtex as many times as needed to resolve
# references, so a one-pass build never ships with unresolved citations.

.PHONY: all anon clean check audit figures

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

# The double-blind variant, from the same source. IASEAI'26 required anonymised
# submission under double-blind review. Building it from a forked file would
# guarantee the two drift; building it from a flag guarantees they cannot.
anon: main.tex refs.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=anon \
	  -pdflatex='pdflatex %O "\def\anon{}\input{%S}"' main.tex
	cd .. && python3 scripts/check_anonymous.py paper/anon.pdf

# Every artifact-backed number in the manuscript, against its artifact.
audit:
	cd .. && python3 scripts/audit_paper_numbers.py

# Regenerate the two figures. Needs requirements-paper.txt, which pins
# matplotlib because these PDFs are committed artifacts. The bytes will differ
# from the committed ones because matplotlib stamps a creation date; what must
# match is the rendered content and the font program. Check the latter with
# `pdffonts figures/fig1_two_total_effects.pdf`: it must say CID TrueType, not
# Type 3. Type 3 fonts do not embed hinting and render badly in some viewers,
# and matplotlib emits them by default.
figures:
	python3 make_figures.py
	@pdffonts figures/fig1_two_total_effects.pdf | sed -n '3p'
	@pdffonts figures/fig2_coupling_gap.pdf | sed -n '3p'
	@for f in figures/*.pdf; do \
	  if pdffonts "$$f" | grep -q "Type 3"; then \
	    echo "TYPE 3 FONTS ARE BACK in $$f; see the rcParams in make_figures.py"; \
	    exit 1; \
	  fi; \
	done; echo "both figures embed Type 42 (CID TrueType), as the manuscript needs"

clean:
	latexmk -C
	rm -f main.bbl main.blg anon.pdf anon.aux anon.log anon.out anon.fls anon.fdb_latexmk
