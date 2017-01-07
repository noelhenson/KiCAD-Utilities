#!/usr/bin/python
# KiCAD PCBnew utility to center and orient reference designators to
# quickly create assebmbly documentation.
# Author: Noel Henson - nowlwhenson@gmail.com
#
# MIT License
# 
# Copyright (c) 2017 Noel Henson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# imports
import sys
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('command',help='center, (center is only command at this time)')
parser.add_argument('infile', help='input file', type=argparse.FileType('r'))
parser.add_argument('outfile', help='output file (must not be input file)', type=argparse.FileType('w'))
parser.add_argument('--fab', help ='force references to fab layer', action='store_true')
parser.add_argument('-v, --version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

#globals
fin = args.infile
fout = args.outfile
command = args.command
orientation = ''

# center and orient reference designators
def centerRefDes(line):
    global orientation
    if 'fp_text reference' in line:
        start = line.find('(at ')
        end = line[start:].find(')') + start
        out = line[:start] + '(at 0 0 ' + orientation + line[end:]
        # optionally move the refdes from the silkscreen to the fab layer
        if args.fab:
            out = out.replace('F.SilkS','F.Fab')
            out = out.replace('B.SilkS','B.Fab')
        return out
    elif '   (at ' in line:
        splitline = line.split(' ')
        if len(splitline) == 7:
            orientation = ''
        elif len(splitline) == 8:
            orientation = splitline[7][:-2]
        return line
    else:
        return line

# rifle through each line of the file
def centerAllRefDes(fin,fout):
    line = fin.readline()
    while(line != ''):
        line = centerRefDes(line)
        fout.write(line)
        line = fin.readline()
    fin.close()
    fout.close()

# Main
if command == 'center':
    centerAllRefDes(fin,fout)
else: # unknown command
    print parser.prog
    print "    unknown command:",args.command
