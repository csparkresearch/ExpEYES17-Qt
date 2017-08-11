#!/usr/bin/python3
"""
fixing includegraphics macros when the file is an SVG image
"""

import re, sys
from subprocess import call

if __name__=="__main__":
    svgRe=re.compile(r"\\includegraphics([^{]*)\{([^}]+)\.svg\}", re.I)
    data=sys.stdin.read()
    for f in svgRe.findall(data):
        cmd="rsvg-convert -f pdf {img}.svg -o {img}.pdf".format(img=f[1])
        call(cmd, shell=True)
    data=re.sub(svgRe,r"\\includegraphics\1{\2}",data)
    sys.stdout.write(data)
