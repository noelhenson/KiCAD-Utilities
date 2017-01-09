# KiCAD-Utilities
KiCAD Utilities

These are utilities I find useful in near constant use of KiCAD in professional design projects.

* ku-refdes.py - convert a PCBnew file into an assembly file with reference designators centered and oriented on their components with the option to push them to their associated fab layers.
This program is very simple and does little in the way of error checking.
But it is very fast.

# Requirements 

* Python 2
* argparse module
* csv module

# Installation
Just copy these utilities to some place in your path. I use $HOME/bin. You may have to set the exec flag with 'chmod +x'. You may also have to change the path to python. It is currently set to '/usr/bin'.
