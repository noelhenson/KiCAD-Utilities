# KiCAD-Utilities
KiCAD Utilities

These are utilities I find useful in near constant use of KiCAD in professional design projects.

* ku-refdes.py - Convert a PCBnew file into an assembly file with reference designators centered and oriented on their components with the option to push them to their associated fab layers.
This program is very simple and does little in the way of error checking.
But it is very fast.

* ku-bom.py - Convert an EESchema BOM CSV file into something more usable. 
There is optional pruning of unused fields and 'Part Number' and 
'Manufacturer' fields are added.

# Requirements 

* Python 2
* argparse module
* csv module

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
ku-refdes.py --fab center design.kicad_pcb assembly.kicad_pcb
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
## ku-bom.py

Conver an EESchema BOM CSV from one line per component instance to a 
shorter format with one unique component per line. This depends on using 
field values. Appropriate field name might be "Tolerance", "Voltage", 
"Power" or others. Unused fields can be optionally pruned from the output. 
Version 0.2 will support a configuration file for adding and custom 
ordering (column-wise) of the fields.
```
ku-bom --prune design.csv bom.csv
```
Will take this:
```
Reference;Qty;Value;Footprint;Datasheet;Field5;Field6;Field7;Field8;Field4;Tolerance;Power;Voltage
R7;1;0;Resistors_SMD:R_0603;;;;;;;;;
C30;1;0.0015uF;Capacitors_SMD:C_0603;;;;;;;;;;;
C68;2;0.01uF;Capacitors_SMD:C_0603;;;;;;;;;;;
C31;2;0.01uF;Capacitors_SMD:C_0603;;;;;;;;;;;
```
And turn it into this:
```
Reference;Qty;Value;Footprint;Datasheet;Tolerance;Power;Voltage;Part Number;Manufacturer
R7;1;0;Resistors_SMD:R_0603;;;;;;
C30;1;0.0015uF;Capacitors_SMD:C_0603;;;;;;
C31,C68;2;0.01uF;Capacitors_SMD:C_0603;;;;;;
```
To get help:
```
ku-bom.py -h
usage: ku-bom.py [-h] [-p] [-v] infile outfile

positional arguments:
  infile         input file
  outfile        output file (must not be input file)

optional arguments:
  -h, --help     show this help message and exit
  -p, --prune    prune unused fields
  -v, --version  show program's version number and exit
```
