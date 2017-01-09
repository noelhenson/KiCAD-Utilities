# KiCAD-Utilities
KiCAD Utilities

These are utilities I find useful in near constant use of KiCAD in professional design projects.

* ku-refdes.py - convert a PCBnew file into an assembly file with reference designators centered and oriented on their components with the option to push them to their associated fab layers.
This program is very simple and does little in the way of error checking.
But it is very fast.

# Requirements 

* Python 2
* argparse module
* csv module (for the forthcoming ku-bom.py utility)

# Installation
Just copy these utilities to some place in your path. I use $HOME/bin. You may have to set the exec flag with 'chmod +x'. You may also have to change the path to python. It is currently set to '/usr/bin'.

# Examples

## ku-refdes.py

Create a version of a layout for assembly purposes. This will center the 
reference designators on top of their components and rotate them to match 
the orientation of the its footprint. The '--fab' option will move the 
reference designators from the front or back silkscreen to the front or 
back fab layer, respectively.
```
ku-refdes.py center --fab design.kicad_pcb assembly.kicad_pcb
```
To get help:
```
ku-refdes.py -h
usage: ku-refdes.py [-h] [--fab] [-v, --version] command infile outfile

positional arguments:
  command        center, (center is only command at this time)
  infile         input file (PCBnew file)
  outfile        output file (must not be input file)

optional arguments:
  -h, --help     show this help message and exit
  --fab          move references to fab layer
  -v, --version  show program's version number and exit
```
