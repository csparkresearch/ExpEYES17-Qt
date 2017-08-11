#!/usr/bin/python3
"""
fixing bad pairs of hyperlink/hypertarget made by pandoc version 1.17.2
This command acts as a filter between stdin and stdout
"""

import re, sys
from difflib import SequenceMatcher

def safeLabel(s):
    return re.sub(r"[^a-zA-Z]",":",s)

if __name__=="__main__":
    labelRe=re.compile(r"\\label\{([^}]+)\}", re.I)
    hyperlinkRe=re.compile(r"\\hyperlink\{([^}]+)\}", re.I)
    data=sys.stdin.read()
    labels=labelRe.findall(data)
    hyperlinks=hyperlinkRe.findall(data)
    for h in hyperlinks:
        ratios=[(l,SequenceMatcher(a=l,b=h).ratio()) for l in labels]
        bestRatio=max(ratios,key=lambda x: x[1])
        label=bestRatio[0]
        # replace hyperlinks
        newlabel=safeLabel(label)
        data=data.replace(r"\hyperlink{%s}" %h, r"\hyperlink{l%s}" %newlabel)
        data=data.replace(r"\label{%s}" %label, r"\label{l%s}\hypertarget{l%s}{}" %(newlabel,newlabel))
    sys.stdout.write(data)
