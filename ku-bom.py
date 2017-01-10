#!/usr/bin/python
# KiCAD BOM processor
# Author: Noel Henson - nowlwhenson@gmail.com
# Copyright (c) 2017
# Use at your own risk

from os import linesep
import argparse
import csv

# Arguments
parser = argparse.ArgumentParser()
#parser.add_argument('command',help='center, (center is only command at this time)')
parser.add_argument('infile', help='input file', type=argparse.FileType('r'))
parser.add_argument('outfile', help='output file (must not be input file)', type=argparse.FileType('w'))
parser.add_argument('-p', '--prune', help ='prune unused fields', action='store_true')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

# globals
additionalFields = ['Part Number','Manufacturer']
fin = args.infile               # input file
fout = args.outfile             # output file
bomin = csv.reader(fin)         # cvs reader object
components = []                 # list of components, one for each reference designator
devices = []                    # list of unique devices, one field with list of reference designators
numfields = 0                   # max number of fields
rawfields = []                  # raw field names, may contain preceding space
fields = []                     # list of parameter field names

# Normalize field count
def addMissingFields(line,cnt):
    while len(line) < cnt:
        line.append('')

# Read the CSV file
def cvsRead():
    global rawfields, numfields
    rawfields = bomin.next()        # read the field names from the first line all but the first will have a leading space
    numfields = len(rawfields) + len(additionalFields)

# Make the list of field names
def getFieldNames():            # without leading or trailing spaces
    for field in rawfields:
        fields.append(field.strip())
    for field in additionalFields:
        fields.append(field)

# Read the raw CSV from EESchema
def readComponents():
    global components
    for component in bomin:
        addMissingFields(component,numfields)
        components.append(component)

# Convert component list to device list
def createDeviceList():
    global components, devices
    cvsRead()
    getFieldNames()
    readComponents()
    components = sorted(components, key=lambda comp: comp[1:])
    prevcomp = fields  # prime the compare-to so it has the appropriate number of fields
    refdes = []
    refdes.append(prevcomp[0]) # weird, but it removes a special case for line 0
    for comp in components:
        if prevcomp[1:] != comp[1:]:
            prevcomp[0] = ','.join(sorted(refdes))
            if prevcomp[0] == 'Reference': # ugly and inefficient but effective
                qty = 'Qty'
            else:
                qty = len(refdes)
            prevcomp.insert(1,str(qty))
            devices.append(prevcomp)
            refdes = []
        refdes.append(comp[0])
        prevcomp = comp

# Prune unused fields (but keep the additional fields)
def pruneFields():
    global devices
    usage = []
    flen = len(fields) - len(additionalFields)
    for i in range(flen):
        usage.append(-1)    # pre-decrement counts to account for line 0
    for device in devices:  # check the usage of each field over the list of devices
        for i in range(flen):
            if device[i] != "":
                usage[i] += 1
    pruned = []
    for device in devices:  # prune fields with no entries
        for i in range(flen-1,-1,-1):   # prune from right to left so pruned fields won't mess up others
            if not usage[i]:    # if count == 0, prune the field
                device.pop(i)
        pruned.append(device)
    devices = pruned

# Main

def main():
    global components, devices
    # data preparation
    createDeviceList()

    if args.prune:
        pruneFields()

    # output the csv
    for device in devices:
        line = ';'.join(device) + linesep
        fout.write(line)

main()
