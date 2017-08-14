#!/usr/bin/python3

import os, os.path
import sys
sys.path=[os.path.dirname(__file__)]+sys.path
from subprocess import call, Popen, PIPE, STDOUT
from tm import imgWidthFilter, labelFilter, svgFilter
from MarkdownPP import MarkdownPP
from MarkdownPP.Modules import modules

# just for translations
from PyQt5 import QtCore, QtWidgets
_translate = QtCore.QCoreApplication.translate

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
# {toc}
!TOC

# {intro}
!INCLUDE "index.md", 1

# {apps}
        """.format(
            toc=_translate("textmanual","Table of contents"),
            intro=_translate("textmanual","Introduction"),
            apps=_translate("textmanual","Applications"),
        ))
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
    
def translators(langDir, lang=None):
    """
    create a list of translators
    @param langDir a path containing .qm translation
    @param lang the preferred locale, like en_IN.UTF-8, fr_FR.UTF-8, etc.
    @result a list of QtCore.QTranslator instances
    """
    if lang==None:
            lang=QtCore.QLocale.system().name()
    result=[]
    qtTranslator=QtCore.QTranslator()
    qtTranslator.load("qt_" + lang,
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    result.append(qtTranslator)

    # path to the translation files (.qm files)
    sparkTranslator=QtCore.QTranslator()
    sparkTranslator.load(lang, langDir);
    result.append(sparkTranslator)
    return result

def firstExistingPath(l):
    """
    Returns the first existing path taken from a list of
    possible paths.
    @param l a list of paths
    @return the first path which exists in the filesystem, or None
    """
    for p in l:
        if os.path.exists(p):
            return p
    return None

def common_paths():
    """
    Finds common paths
    @result a dictionary of common paths
    """
    path={}
    curPath = os.path.dirname(os.path.realpath(__file__))
    path["current"] = curPath
    sharedPath = "/usr/share/expeyes17"
    path["translation"] = firstExistingPath(
            [os.path.join(p, "lang") for p in
             (curPath, "..",)])
    return path

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    path = common_paths()
    for t in translators(path["translation"]):
        print("GRRR",t)
        app.installTranslator(t)
    
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
