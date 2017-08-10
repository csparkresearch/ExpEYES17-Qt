#!/usr/bin/python3

import re, sys

if __name__=="__main__":
    imgWidthRe=re.compile(r"(\\includegraphics{(\S+)}\\{:[ \n]*width=``(.*)''\\})", re.I)
    widthRe=re.compile(r"^(.*)\\includegraphics\[width=(\d*)(.+)\]{([^}]+)}(.*)$")
    data=sys.stdin.read()
    lines=re.sub(imgWidthRe,r"\\includegraphics[width=\3]{\2}",data).split("\n")
    for i in range(len(lines)):
        m=widthRe.match(lines[i])
        if m:
            w = 1 # the width in \textwidth unity,defaults to 1
            if "%" in m.group(3): # width given as a percentage
                w=int(m.group(2))/100
            elif "px" in m.group(3): # width given as pixels
                w=int(m.group(2))/800 # assuming that the navigator's width would be 800 px.
            lines[i]=r"%s\includegraphics[width=%s\textwidth]{%s}%s" \
              %(m.group(1),w,m.group(4),m.group(5))
    data2="\n".join(lines)
    sys.stdout.write(data2)
    
