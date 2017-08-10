#!/bin/sh

echo "making manual.mdpp to feed the Markdown Preprocessor"
cat << EOF > manual.mdpp
!TOC

!INCLUDE "index.md"

# Applications

EOF

for f in $(find _apps -name "*.md"); do
  echo "!INCLUDE \"$f\"" >> manual.mdpp
done

echo "making manual.md with markdown-pp"

./md-pp -o manual.md manual.mdpp

echo "making manual.tex with pandoc"
pandoc --template=pandoc.latex -t latex -o manual.tex manual.md

echo "making manual.odt with pandoc"
pandoc -o manual.odt manual.md

echo "making manual.pdf with pdfLaTeX"
pdflatex -interaction=nonstopmode manual.tex
pdflatex -interaction=nonstopmode manual.tex


