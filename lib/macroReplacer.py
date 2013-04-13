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

#Function to create a macroTable for each file
def createMacroTable( fileNames ):
	i=0
	for fileName in fileNames :
		inputFile = open(fileName, 'r')
		code = inputFile.read()
		lines = code.split('\n')
		lastMacro =''
		expCode = []
		flag = 0
		asCode =[]
		for line in lines :
			line = line.split(';')[0].lstrip().rstrip()
			if 'MACRO' in line:
				lastMacro = line.split(' ')[1]
				macroTable[lastMacro] = ' '.join(line.split(' ')[2:])
				flag = 1
			elif 'MEND' in line : 
				macroCode[lastMacro]='\n'.join(expCode)
				flag = 0
				expCode = []
				lastMacro =''
			elif flag == 1 :
				expCode.append(line)
			else :
				if(line!='') :
					asCode.append(line)
		code =  '\n'.join(asCode)
		fileNames[i] = fileNames[i].split('.')[0]+'.pre'
		outputFile = open(fileNames[i], 'w')		
		outputFile.write(code)
		tableFile = open(fileNames[i].split('.')[0]+'.table', 'w')
		mcode = '-------------MACROS-------------\n'
		for macros in macroTable :
			mcode = mcode + macros + "\t" + macroTable[macros]
			mcode = mcode + '\n'+ macroCode[macros]+'\n \n'
		mcode = mcode + '-------------MACROS-------------\n'
		tableFile.write(mcode)
		outputFile.close()
		inputFile.close()
		i=i+1

#Function to expand each occurance of macros in the code via looking into the macroTable
def replaceMacros( fileNames ):
	for fileName in fileNames :
		replacements = True
		while replacements :
			replacements = False
			inputFile = open(fileName, 'r')
			code =  inputFile.read().upper()
			lines = code.split('\n')
			asCode =[]
			for line in lines :
				line = line.lstrip().rstrip()
				tag = macroPresent(line)
				if  tag != '':
					pams =  ''.join(line.split(tag)[1:]).lstrip().rstrip().split(',')
					tag_pam = mapping(tag,pams)
					line = macroCode[tag]
					for pam in tag_pam :
						line = line.replace(pam,tag_pam[pam])
					replacements = True
				if(line!='') :
					asCode.append(line);
			code =  '\n'.join(asCode)
			outputFile = open(fileName, 'w')
			outputFile.write(code)
			outputFile.close()
			inputFile.close()

# Function to map parameters of each of macros with the corrosponding parameters provided in the code
def mapping( tag,pams ):
	tag_pam ={}
	pam_list = macroTable[tag].lstrip().rstrip().split(',')
	i=0
	for pam in pam_list:
		tag_pam[pam] = pams[i]
		i=i+1
	return tag_pam	

# Function to check if the macro is present in the code
def macroPresent( line ):
	tags = line.split(' ')
	for tag in tags :
		if tag in macroTable :
			return tag
	return ''

macroTable = {}
macroCode= {}