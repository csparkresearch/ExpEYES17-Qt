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

echo "fixing paths to application images"
sed -e 's%images/%_apps/images/%g' manual.md > manual.md.tmp &&
    mv manual.md.tmp manual.md

echo "making manual.tex with pandoc"
pandoc -t latex -o manual.tex manual.md

echo "making manual.odt with pandoc"
pandoc -o manual.odt manual.md

echo "making manual.pdf with unoconv"
unoconv -f pdf manual.odt

