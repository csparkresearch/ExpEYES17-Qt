#!/usr/bin/python3

import os, os.path
import sys
sys.path=[os.path.dirname(__file__)]+sys.path
from subprocess import call, Popen, PIPE, STDOUT
from tm import imgWidthFilter, labelFilter, svgFilter
from MarkdownPP import MarkdownPP
from MarkdownPP.Modules import modules

def includeMd(path, outFile):
    """
    Includes files from a subdirectory, eventually taking in account
    groups and some sorting. The early version makes no grouping.
    @param path the subdirectory where .md files are searched
    @param outFile the .mdpp file to write into
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".md"):
                outFile.write("!INCLUDE \"%s\", 1\n" %os.path.join(root,f))

def makeMdpp(outdir="."):
    """
    make the file manual.mdpp to use with the preprocessor
    which will include multiple .md files to feed later pandoc.
    @param outdir output directory
    """
    with open(os.path.join(outdir,"manual.mdpp"),"w") as mdppFile :
        mdppFile.write("""\
!TOC

!INCLUDE "index.md", 1

""")
        includeMd("_apps", mdppFile)

def makeTex(outdir="."):
    """
    use pandoc to create TEX file from MD file, and fixes some
    drawbacks of pandoc
    @param outdir output directory
    """
    mdFile=os.path.join(outdir,"manual.md")
    texFile=os.path.join(outdir,"manual.tex")
    call("pandoc --template=pandoc.latex -t latex -o %s %s" %(texFile, mdFile),
         shell=True)
    # fix width syntax for images, fix hyperlink discrepancies, fix SVG includes
    data=open(texFile,"r").read()
    for m in (imgWidthFilter, labelFilter, svgFilter):
        data=m.run(data)
    open(texFile,"w").write(data)

def PDFnotYetIndexed(fname):
    """
    @param fname a file name, without any suffix
    @return True if pdflatex did not index correctly the PDF output
    """
    f=fname+".log"
    return not os.path.exists(f) or\
        call("grep -iq 'Rerun to get cross-references ' "+f,
             shell=True)==0 or\
        call("grep -iq 'Rerun to get outlines ' "+f,
             shell=True)==0
    
if __name__=="__main__":
    
    outdir="manual"
    if len(sys.argv) >1:
        outdir=sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    
    print("making %s/manual.mdpp to feed the Markdown Preprocessor" %outdir)
    makeMdpp(outdir=outdir)
    
    print("making %s/manual.md with markdown-pp" %outdir)
    MarkdownPP(input=open("%s/manual.mdpp" %outdir,"r"),
               output=open("%s/manual.md" %outdir,"w"),
               modules=list(modules))
    
    print("making %s/manual.tex with pandoc" %outdir)
    makeTex(outdir=outdir)

    print("making %s/manual.odt with pandoc" %outdir)
    call("pandoc -o %s/manual.odt %s/manual.md" %(outdir,outdir), shell=True)

    print("making %s/manual.pdf with pdfLaTeX" %outdir)
    if os.path.exists("%s/manual.log" %outdir):
        os.unlink("%s/manual.log" %outdir)
    while PDFnotYetIndexed("%s/manual" %outdir):
        call("cd %s; pdflatex -interaction=nonstopmode manual.tex" %outdir,
             shell=True)
