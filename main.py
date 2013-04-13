#!/usr/bin/python

# This file is a part of software 8085 Simulator 
#Copyright (C) 2013  Arihant Sethia
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib import pre_processor,assembler,linker,loader

fileNames = []
inFile = raw_input('Enter the file name : ');
i=0;
while (inFile!='') :
	fileNames.append(inFile)
	inFile = raw_input('Enter the file name : ');
	i=i+1

pre_processor.replace_macros ( fileNames )
pre_processor.replace_opcodes ( fileNames )
raw_input('Pre-Processing Done ......\nPress Enter to Coninue..... ')
assembler.createSymbolTable( fileNames )
raw_input('Pass 1 Assembling Done ......\nPress Enter to Coninue..... ')
assembler.replaceTable( fileNames )
raw_input('Pass 2 Assembling Done ......\nPress Enter to Coninue..... ')
linker.link(fileNames)
raw_input('Linking Done ......\nPress Enter to Coninue..... ')
loader.load(fileNames)
raw_input('Loading Done ......\nPress Enter to Coninue..... ')