
## Installation with anaconda (includes pyqt and scipy dependencies):

https://www.continuum.io/downloads : Download relevant version (~400MB)

open anaconda command prompt: 'Anaconda Prompt' 
```
 - pip install pyqtgraph pyserial
```
test a basic plotting example to see if it works.
```
- python -m pyqtgraph.examples
```

+ Visit  the github page to download the zip file of windows branch of spark17 : https://github.com/csparkresearch/expeyes17-qt/tree/windows
+ Extract the zip file
+ Connect the device and let windows automatically download drivers. takes 2 minutes.

From the anaconda prompt, CD to the relevant location, and run `python -m SPARK17.spark17` 

note that the .py extension is not used.

Alternatively , you can also use `python run.py` which invokes the previous command automatically

## Installation via separate dependencies

Download and install [Python 2.7](https://www.python.org/downloads/) : Checked the 'add to path' option
opened cmd and checked if python was accessible. ctrl-z+enter to exit


DOWNLOAD  and install correct version of PyQt4 from [~Gohlke](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) . Use the 32-bit windows installer.

Install the wheel file using pip : `pip install PyQt4-4.11.4-cp27-cp27m-win32.whl`

-------------------------------------------------

download and install numpy  : http://www.lfd.uci.edu/~gohlke/pythonlibs/wu4bx7or/numpy-1.13.1+mkl-cp27-cp27m-win32.whl

`pip install numpy-1.13.1+mkl-cp27-cp27m-win32.whl`  (took 30 seconds)

-------------------------------------------
Now we are ready to install pyqtgraph and check if everything is running
download and install win32 installer from http://www.pyqtgraph.org/

open cmd

`python -m pyqtgraph.examples`

run one of the examples just to be sure

----------------------------------------------------------
download and install scipy (52MB) http://www.lfd.uci.edu/~gohlke/pythonlibs/wu4bx7or/scipy-0.19.1-cp27-cp27m-win32.whl

`pip install scipy-0.19.1-cp27-cp27m-win32.whl`

---------------------------------------------------------------------

pip install pyserial

--------------------------------------------------------------------


downloaded and extracted  https://github.com/csparkresearch/expeyes17-qt/tree/windows

`cd Expeyes17-qt-windows\`

connect device, and wait for windows to install drivers automatically (took 2 minutes on win10) . If not, you can also download the drivers for MCP2200 via microchip.com

`python -m SPARK17.spark17`
or
`python run.py`

Everything should be working, and the oscilloscope app should be displayed by default.

## Updating

You will only need to download the source for ExpEYES-17 in order to fetch the latest updates.

If you are familiar with `git` , clone the `windows` branch , and do a `git pull` to fetch the latest changes.


## Bundled 32-bit installer
[Download Link](https://drive.google.com/file/d/0B-Zqgt0_c1zDdDIyOXl1WEdXWnc/view?usp=drive_web)

