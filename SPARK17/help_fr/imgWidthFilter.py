#!/usr/bin/python3

import re, sys

if __name__=="__main__":
    imgWidthRe=re.compile(r"(\\includegraphics{(\S+)}\\{:[ \n]*width=``(.*)''\\})", re.I)
    data=sys.stdin.read()
    sys.stdout.write(re.sub(imgWidthRe,r"\\includegraphics[width=\3]{\2}",data))
    
