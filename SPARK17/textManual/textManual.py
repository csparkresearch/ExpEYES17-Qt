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

def makeMdpp():
    """
    make the file manual.mdpp to use with the command ./md-pp
    which will include multiple .md files to feed later pandoc.
    """
    with open("manual.mdpp","w") as mdppFile :
        mdppFile.write("""\
!TOC

!INCLUDE "index.md", 1

""")
        includeMd("_apps", mdppFile)

def makeTex():
    """
    use pandoc to create TEX file from MD file, and fixes some
    drawbacks of pandoc
    """
    call("pandoc --template=pandoc.latex -t latex -o manual.tex manual.md",
         shell=True)
    # fix width syntax for images, fix hyperlink discrepancies, fix SVG includes
    data=open("manual.tex","r").read()
    for m in (imgWidthFilter, labelFilter, svgFilter):
        data=m.run(data)
    open("manual.tex","w").write(data)

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
    print("making manual.mdpp to feed the Markdown Preprocessor")
    makeMdpp()
    
    print("making manual.md with markdown-pp")
    #call("LANG=en_GB.UTF-8 ./md-pp -o manual.md manual.mdpp",shell=True)
    MarkdownPP(input=open("manual.mdpp","r"),
               output=open("manual.md","w"),
               modules=list(modules))
    
    print("making manual.tex with pandoc")
    makeTex()

    print("making manual.odt with pandoc")
    call("pandoc -o manual.odt manual.md", shell=True)

    print("making manual.pdf with pdfLaTeX")
    if os.path.exists("manual.log"):
        os.unlink("manual.log")
    while PDFnotYetIndexed("manual"):
        call("pdflatex -interaction=nonstopmode manual.tex",
             shell=True)
