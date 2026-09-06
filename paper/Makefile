# P2 manuscript. `make` builds main.pdf, `make clean` removes every artifact.
# latexmk runs pdflatex and bibtex as many times as needed to resolve
# references, so a one-pass build never ships with unresolved citations.

.PHONY: all anon clean check audit figures arxiv

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

# The arXiv submission package, as a tarball rather than a directory, because a
# directory in a working tree accumulates whatever a previous build left in it
# and arXiv takes one upload anyway. Built in a scratch directory so no LaTeX
# droppings are ever created inside the repository, and test-compiled the way
# arXiv compiles it: three pdflatex passes, no bibtex, nothing else present.
# arXiv does not run bibtex, so main.bbl ships with the source. The recipe
# asserts the shipped main.tex is byte-identical to this one, because a second
# copy of a manuscript is a drift waiting to happen. The tarball is derived and
# gitignored.
ARXIV_TARBALL = p2-arxiv-submission.tar.gz

arxiv: main.pdf
	@B=$$(mktemp -d) && mkdir -p $$B/pkg/figures && \
	 cp main.tex main.bbl $$B/pkg/ && \
	 cp figures/fig1_two_total_effects.pdf figures/fig2_coupling_gap.pdf $$B/pkg/figures/ && \
	 cmp main.tex $$B/pkg/main.tex && \
	 cp -r $$B/pkg $$B/build && \
	 ( cd $$B/build && for i in 1 2 3; do \
	     pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null; done ) && \
	 if grep -qE 'Citation .* undefined|Reference .* undefined' $$B/build/main.log; then \
	   echo "the arXiv package does not resolve its own references"; rm -rf $$B; exit 1; fi && \
	 [ -s $$B/build/main.pdf ] || { echo "no PDF came out of the standalone build"; rm -rf $$B; exit 1; } && \
	 echo "compiles standalone with pdflatex only, no bibtex$$(command -v pdfinfo >/dev/null 2>&1 && echo ": $$(pdfinfo $$B/build/main.pdf | awk '/Pages/{print $$2}') pages")" && \
	 ( cd $$B/pkg && tar czf $$B/out.tgz . ) && \
	 cp $$B/out.tgz $(ARXIV_TARBALL) && rm -rf $$B && \
	 echo "paper/$(ARXIV_TARBALL) contains exactly:" && tar tzf $(ARXIV_TARBALL) | sed 's/^/  /'

clean:
	rm -f $(ARXIV_TARBALL)
	latexmk -C
	rm -f main.bbl main.blg anon.pdf anon.aux anon.log anon.out anon.fls anon.fdb_latexmk
