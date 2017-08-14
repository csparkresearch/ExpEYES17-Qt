#!/usr/bin/python3
"""
fixing includegraphics macros when the file is an SVG image
"""

import re, sys
from subprocess import call

def run(data):
    """
    fixes included SVG files, by making PDF files from them and
    changing the TEX code
    @param dataIn input data stream
    @return output data stream
    """
    svgRe=re.compile(r"\\includegraphics([^{]*)\{([^}]+)\.svg\}", re.I)
    for f in svgRe.findall(data):
        cmd="rsvg-convert -f pdf {img}.svg -o {img}.pdf".format(img=f[1])
        call(cmd, shell=True)
    data=re.sub(svgRe,r"\\includegraphics\1{\2}",data)
    return data
    
if __name__=="__main__":
    data=run(sys.stdin.read())
    sys.stdout.write(data)
