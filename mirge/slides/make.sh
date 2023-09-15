#! /bin/bash

set -e

export TEXINPUTS="$TEXINPUTS:media:figures:ceesd-style"

unset PYTHONWARNINGS

DOWATCH="0"

if [[ "$1" = "watch" ]]; then
  DOWATCH="1"
  shift
fi

if [[ "$1" = "" ]]; then
  FILES=(talk.tex )
else
  FILES=("$@")
fi

#LATEXRUN="python -m pudb $(which latexrun) --latex-cmd lualatex --bibtex-cmd $BIBER --verbose-cmds -O out"
LATEXRUN="latexrun --latex-cmd pdflatex --verbose-cmds -O out"

if [[ "$DOWATCH" = "1" ]]; then
  git ls-files | entr $LATEXRUN "${FILES[0]}"
else
  for f in "${FILES[@]}"; do
    $LATEXRUN "$f"
  done
fi

cp talk.pdf ~/nc/shared/misc/2023-09-ncsa-west.pdf
