
# Afin de generer la bibliographie :
# 1. modifier le fichier latexensg.bib, par exempel avec JabRef
# 2. compliler le document Latex en lançant le script : > sh CompilationAvecBiblio.sh

pdflatex latexppmd.tex
biber latexppmd
pdflatex latexppmd.tex
pdflatex latexppmd.tex

rm *.aux
rm *.log
rm *.bcf
#rm *.bbl
rm *.run.xml
rm *.blg
rm *.out
