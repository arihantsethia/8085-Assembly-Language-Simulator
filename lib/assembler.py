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


#PASS1 : Function to create symbol table corresponding to the submitted 8085 assembly code 
def createSymbolTable( fileNames ):
	createLengthTable() 
	i = 0
	for fileName in fileNames :

		inputFile = open(fileName, 'r')
		fileName = fileName.split('.')[0]
		fileLength[fileName] = i		
		i = 0
		symbolTable[fileName] = {}
		variableTable[fileName] = {}		
		variableScopeTable[fileName] = {}
		#variableValue[fileName] = {}
		code = inputFile.read()
		lines = code.split('\n')	
		for line in lines :
			line = line.lstrip().rstrip()
			tag = ''
			if len(line.split(':')) > 1:
				tag = line.split(':')[0].rstrip().lstrip()
				symbolTable[fileName][tag] = i
			if 'DS' in line:
				tag = line.split('DS')[0].rstrip().lstrip()
				tag = tag.split(' ')[-1]
				variableTable[fileName][tag] = i
				variableScopeTable[fileName][tag] = scopeVariable(line)
				i = i + int(line.split('DS')[1].rstrip().lstrip())
			if 'DB' in line:
				tag = line.split('DB')[0].rstrip().lstrip()
				tag = tag.split(' ')[-1]
				variableTable[fileName][tag] = i
				variableScopeTable[fileName][tag] = scopeVariable(line)
				i = i + len (line.split(','))
			tags = line.split(' ')
			for tag in tags :			
				if tag in opcodeLengthTable:
					i = i + int(opcodeLengthTable[tag])
		tableFile = open(fileName+'.table', 'a')
		symbols = '-------------SYMBOL-------------\n'
		for symbol in symbolTable[fileName] :
				symbols = symbols + symbol + "\t" + str(symbolTable[fileName][symbol]) + '\n'
		symbols = symbols + '-------------SYMBOL-------------\n'
		variables = '------------VARIABLE------------\n'
		for variable in variableScopeTable[fileName] :
				variables = variables + variable + "\t" + str(variableTable[fileName][variable]) + '\t' + str(variableTable[fileName][variable])+ "\t" + variableScopeTable[fileName][variable] + '\n'
		variables = variables + '------------VARIABLE------------\n'
		tableFile.write(symbols + variables)
		symbols = ''
		variables = ''
		inputFile.close()
		tableFile.close()

#PASS1 : Function to replace each symbol/labels in the code 
def replaceTable( fileNames ):
	i = 0
	for fileName in fileNames :
		inputFile = open(fileName, 'r')
		fileName = fileName.split('.')[0]
		code =  inputFile.read()
		lines = code.split('\n')
		asCode = []
		for line in lines :
			line = line.lstrip().rstrip()
			if(line!=''):
				if ':' in line :
					line = line.split(':',1)[1]
				if 'DS' in line :
					line = 'DS ' + line.split('DS',1)[1]
				if 'DB' in line :
					line = 'DB ' + line.split('DB',1)[1]
				tags = line.split(' ')
				for tag in tags:
					if tag in symbolTable[fileName]:
						line = line.replace(tag,'$'+str(symbolTable[fileName][tag]))
					elif tag.split('+')[0].strip() in variableTable[fileName]:
						add = tag.split('+')[-1]
						if add.isdigit() :
							add = int(add)
						else :
							add = 0
						line = line.replace(tag,'$'+str(variableTable[fileName][tag.split('+')[0].strip()]+add))
				asCode.append(line.lstrip().rstrip())
		inputFile.close()
		code =  '\n'.join(asCode)
		fileNames[i] = fileNames[i].split('.')[0]+'.s'
		outputFile = open( fileNames[i], 'w')
		outputFile.write(code)
		outputFile.close()
		i = i+1

#Function to cacluate the no. of addresses consumed by each segment of code
def createLengthTable():
	configFile = open('config/opcodeslength.config', 'r')
	opcode = configFile.read()
	lines = opcode.split('\n')	
	for line in lines :
		line = line.lstrip().rstrip()
		if (line!='') :
			tags = line.split(' ')
			opcodeLengthTable[tags[0]]=tags[1]
	configFile.close()

#Function to find if the declared variable has 'GLOBAL' or 'LOCAL' scope
def scopeVariable( line ):
	if 'GLOBAL' in line :
		return 'GLOBAL'			
	else : 
		return 'LOCAL'

symbolTable = {}
variableScopeTable = {}
variableTable = {}
fileLength = {}
opcodeLengthTable = {}
