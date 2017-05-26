## Configuration details for Jekyll based help files for ExpEYES-17

+ Generated HTML files are stored in MD_HTML
+ helpfiles for general purpose utilities are located in _utilities
+ application specific files are located in _apps/


### testing the build locally

Jekyll can be used to host a temporary web server via the command `jekyll serve`.

Navigate to `localhost:4000` in the web browser to access the generated html 

the static html files are located in MD_HTML , and are automatically loaded by spark17.py


### What the end result looks like

![help_window](https://cloud.githubusercontent.com/assets/19327143/26511180/7396c32e-427e-11e7-88bb-92617c1c5f58.png)

Static site generator Jekyll is used along with with bootstrap css.

experiment help files are stored in _apps/ in markdown format
e.g. diode-iv.md

```markdown
---
layout: e17page
title: Diode IV
date: 2017-05-21
description: Current-Voltage characteristics of PN junctions
imagebase: diode-iv
---
```
will automatically create the following page. but the following image files must also be present : photographs/diode-iv.jpg , screenshots/diode-iv.png, schematics/diode-iv.svg
![diode-iv](https://cloud.githubusercontent.com/assets/19327143/26511293/07696d90-427f-11e7-9729-f29d6ab2ca4d.png)


