#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
'''
    Copyright (C) 2018 Yuusha
'''
################################################################################
'''
License
    This file is part of Yuusha contribution to OpenFOAM.

    This contribution is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This contribution is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this contribution.  If not, see <http://www.gnu.org/licenses/>.
'''
################################################################################

from re import sub

class thermophysicalTable() :
    """Base class for manipulate thermophysical table
    needed by OpenFOAM tabulated thermophysical properties model."""

    def __init__(self) :
        self.table = []

    def read(self, fileName='') :
        """ Read a tabulated thermophysical file and store it into table"""

        with open(fileName, 'r') as f :
            for line in f :
                tmpList = sub('\(+|\)+', ' ', line).strip().split()
                try :
                    tupleList=[]
                    for i in range(1,len(tmpList)-1,2):
                        tupleList.append((tmpList[i], tmpList[i+1]))
                    self.table.append([tmpList[0], tupleList])
                except IndexError :
                    continue

    def write(self, fileName='', precision=6) :
        """ Write a thermopysical file """

        with open(fileName, 'w') as f :
            f.write('(\n')
            for element in self.table :
                stringOut=""
                for elem in element[1][:] :
                    stringOut += '({:<.{precision}e} {:<.{precision}e}) '.format(float(elem[0]), float(elem[1]), precision=precision)
                f.write('( {:<.{precision}e} ({}))\n'.format(float(element[0]), stringOut, precision=precision))
            f.write(')')

    def importation(self, fileName, fixValue, sep=',', columns=(0,1)) :
        """ Import thermophysical data from a file.
        Only CSV or equivalent is implemented yet """

        with open(fileName, 'r') as f :
            for line in f :
                # Special command when separator is space
                if sep is ' ' :
                    tmpList = line.strip().split()
                else :
                    tmpList = line.strip().split(sep)

                tup=[(fixValue, tmpList[columns[1]])]
                self.table.append([tmpList[columns[0]], tup])

    def transpose(self) :
        """ Invert lines and columns in a tabulated thermophysical list """

        tableTmp = list(self.table)
        self.table = []
        for element in tableTmp :
            for elem in element[1] :
                find = False
                for pres in self.table :
                    if elem[0] == pres[0] :
                        pres[1].append((element[0], elem[1]))
                        find = True
                        break
                if not find :
                    self.table.append([elem[0], [(element[0], elem[1])]])


thermo = thermophysicalTable()
#thermo.read('hTable_orig')
thermo.importation(fileName='test.txt',sep=' ', columns=(0,3), fixValue=1.e5)
#thermo.transpose()
thermo.write('cpTable')
