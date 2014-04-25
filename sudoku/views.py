# This Python file uses the following encoding: utf-8

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context
from django.utils.safestring import SafeString
from django.shortcuts import render_to_response, render, get_object_or_404
from django.conf import settings
from django import forms
from sudoku.forms import *
from sudoku.models import *
from datetime import datetime
from django.db.models import Q
import os
import copy
import csv
import unicodedata
import numpy

def start(request):
	DebugOut('In start Sudoku')
	errMsg = []
 	initStart2 = [
		["","","","","","8","","",""],
		["4","","","","2","","","7",""],
		["8","","","","4","1","3","",""],
		["2","","","","","","7","4",""],
		["5","","","","","","","","9"],
		["","8","3","","","","","","5"],
		["","","6","5","1","","","","8"],
		["","9","","","7","","","","1"],
		["","","","8","","","","",""],
		]
	DebugOut('In start Sudoku2')
		
	initStart = [
		["","","9","","","8","","1",""],
		["","","","","1","","","","8"],
		["7","","1","","","3","","",""],
		["","","","","","5","9","","4"],
		["","5","","","3","","","7",""],
		["3","","6","8","","","","",""],
		["","","","4","","","3","","5"],
		["2","","","","8","","","","1"],
		["","7","","6","","","4","",""],
		]
	# Define the 9x9 matrix "initStart". This is a default "start matrix"
	initStart = initStart2

	# Flatten the 9x9 matrix "initStart" into a one dimensional list "theInputList"
	if 'SudokuMatrix' in request.session:
		theInputList = list(request.session['SudokuMatrix'])
	else:
		theInputList = flatten(initStart)
 		request.session['SudokuMatrix'] = list(theInputList)
	DebugOut('after input list calculation')
	# Reshape the one dimensional list "theInputList" into a 3x3x3x3 "displayForInput"
	DebugOut('before ListTo3333')
	displayForInput = ListTo3333(theInputList)
	DebugOut('after ListTo3333')
	DebugOut('request.method: %s' %request.method)
	
	if request.method == 'POST':
		DebugOut('request.POST: %s' %request.POST)
		if 'submitButton' in request.POST:
			DebugOut('in submitButton')
			if request.POST['submitButton'] == 'Calculate using your entries' or request.POST['submitButton'] == 'Save Puzzle':
				DebugOut('in calc or save')
				# tag to search for is defined with "displayForInput" so copy code from Template
				# update "theInputList" then update "displayForInput"
				for aItem in displayForInput:
					for bItem in aItem:
						for cItem in bItem:
							for theValue, listLocation, array33Location in cItem:
								searchTag = "Elem_"+str(listLocation) +"_"+str(array33Location)
								if searchTag in request.POST:
									# update "theInputList"
									tagVal = request.POST[searchTag]
									tagIndex = int(listLocation) # one level list index
									theInputList[tagIndex] = tagVal
								else:
									DebugOut("searchTag %s not found *********" %searchTag)
				request.session['SudokuMatrix'] = list(theInputList)
				displayForInput = ListTo3333(theInputList) # update displayForInput
			if request.POST['submitButton'] == 'Save Puzzle':
				DebugOut('in save puzzle')
				request.session['SudokuStartMatrix'] = list(theInputList)
				errMsg.append("Puzzle saved")
			if request.POST['submitButton'] == 'Start over, purge all':
				DebugOut('in flush')
				request.session.flush() # =========== flush Session data ========================
				theInputList = flatten(initStart)
				displayForInput = ListTo3333(theInputList)
		 		request.session['SudokuMatrix'] = list(theInputList)
			if request.POST['submitButton'] == 'Restore Puzzle':
				DebugOut('in restore puzzle')
				if 'SudokuStartMatrix' in request.session:
					theInputList = list(request.session['SudokuStartMatrix'])
					request.session['SudokuMatrix'] = list(theInputList)
					displayForInput = ListTo3333(theInputList)
					errMsg.append('Puzzle restored')
					DebugOut('Puzzle restored')
				else:
					errMsg.append('No puzzle restored')
					DebugOut('No puzzle restored')
		
				
	# create possibilities for each entry. Display output is "displayForOutput"
	[possList, success, errMsg] = determinePossible(theInputList)
	if errMsg == []:
		errMsg = '' # send as flag:  "no errors"
	else:
		# if error, then "theInputList" is returned
		possList = theInputList
#	trimmedList = elim22pairs(possList) # not ready for prime time
	displayForOutput = SimpleListTo3333(possList)
		
	nLargeRows = range(9)
	nLargeCols = range(9)
	nRows = range(3)
	nCols = range(3)
	testv = [['1','2','3'],['1','2','3'],['1','2','3']]
	introContext = {'current_date' : timezone.now(),
		'initStart' : initStart,
		'displayForInput' : displayForInput,
		'displayForOutput' : displayForOutput,
		'testv' : testv,
		'nRows' : nRows,
		'nCols' : nCols,
		'nLargeRows' : nLargeRows,
		'nLargeCols' : nLargeCols,
		'urlprefix' : settings.WSGI_URL_PREFIX,
		'debug' : settings.DEBUG,
		'errMsg' : errMsg,
		}

	return render(request, 'sudokustart.html', introContext)

def flatten(xx):
	"""Flatten all levels in a list of lists to one level."""
	result = []
	for el in xx:
		if type(el) == list:
			result.extend(flatten(el))
		else:
			result.append(el)
	return result

def elim22pairs(yy):
	"""Investigate pairs of values, eliminating values outside
	of mutually shared pairs of possibilities. Will not disentangle 
	multiple overlapping pairs."""
	# nested for loop comparing xx to xx
	xx = list(yy) # make an internal copy
	for ii, val1 in enumerate(xx):
		remainingList = xx[ii+1:]
		if len(remainingList) >= 1:
			for jj, val2 in enumerate(remainingList):
				el1 = set(val1)
				el2 = set(val2)
				# determine common elements
				elCommon = el1 & el2
				if len(elCommon) == 2:
					# bingo. Other elements in val1 & val2 outside intersection
					# are not possible.
					xx[ii] = list(elCommon) # val1 at ii
					xx[jj+ii+1] = list(elCommon) # val2 at jj
				# else, no changes
	return xx

def make99(xx):
	"""Convert list to 9x9 2d list"""
	tarr = numpy.array(xx).reshape(9,9)
	tout = tarr.tolist()
	return tout


def ListTo3333(xx):
	"""Reformats list to 3x3x3x3 for display. Adds index value as well."""
	jj = 0
	abMat = []
	iRow = 0 # identify 3x3 matrix location
	for aItem in range(3):
		iCol = 0
		bMat = []
		for bItem in range(3):
			ijMat=[]
			for iItem in range(3):
				jMat = []
				for jItem in range(3):
					listLocation = jItem + 3*bItem + 9*iItem + 27*aItem
					arrayLoc = [iRow,iCol] # location of the 3x3 matrix
					jMat.append([xx[listLocation],listLocation,arrayLoc])
					jj+=1
				ijMat.append(jMat)
			bMat.append(ijMat)
			iCol+=1
		abMat.append(bMat)
		iRow+=1
	return abMat
	
def SimpleListTo3333(xx):
	"""Reformats list to 3x3x3x3 for display."""
	jj = 0
	abMat = []
	iRow = 0 # identify 3x3 matrix location
	for aItem in range(3):
		iCol = 0
		bMat = []
		for bItem in range(3):
			ijMat=[]
			for iItem in range(3):
				jMat = []
				for jItem in range(3):
					listLocation = jItem + 3*bItem + 9*iItem + 27*aItem
					jMat.append(xx[listLocation])
					jj+=1
				ijMat.append(jMat)
			bMat.append(ijMat)
			iCol+=1
		abMat.append(bMat)
		iRow+=1
	return abMat

def	StripNonIntegers(xx):

	return

def IsDups( xx):
	"""Determine if there are duplicates in a single-level list"""
	return len(xx) != len(list(set(xx)))

def DebugOut( debugMessage):
	#now = timezone.now()
	# open a debug file
	try:
		if settings.DEBUG_1:
			fpage = open('debugInfo.txt','a')
			#fpage.write('mQuest:  Time: %s \n' % now)
			fpage.write( debugMessage + '\n')
			fpage.close()
	except:
		pass
	return True

def determinePossible(xx):
	'''Determine possible values for each cell.
	Assume an input list. Output is a one dimensional list of possibilities for each cell,
	with original values not in a list.'''
	success = True # optimism
	errMsg = []
	legalVals = set(map(lambda x: str(x+1),range(9)))
	# strip any extra blanks.
	xx = [xb.strip() for xb in xx]
	map9to3 = lambda x: x/3 # determines indices for which small 3x3 matrix the i,j element belongs
	# create 3x3 arrays
	the33Arrays = SimpleListTo3333(xx)
	# create list of a list (matrix)
	mat99 = make99(xx)
	# create row lists
	theRows = mat99
	# create col lists
	theCols = [ [ yRow[ii] for yRow in mat99] for ii in range(9)]
	# traverse all cells
	listPoss = [] # list of list of possible elements
	for irow in range(9):
		for icol in range(9):
			cellVal = mat99[irow][icol]
			cellLoc = str(irow + 1)+" "+str(icol + 1) # start with 1 for humans
			# check for a single blank
			# flatten the appropriate 3x3 matrix
			irow33 = map9to3(irow)
			icol33 = map9to3(icol)
			f33 = flatten(the33Arrays[irow33][icol33])
			# collect all numbers in intersecting matrices
			# Check for uniqueness in each row, column and 3x3 matrix
			nonullRow = stripNulls(theRows[irow])
			if IsDups(nonullRow):
				success = False
				errMsg.append("Duplicates in col  " + str(irow+1))
			nonullCol = stripNulls(theCols[icol])
			if IsDups(nonullCol):
				success = False
				errMsg.append("Duplicates in row  " + str(icol+1))
			nonullf33 = stripNulls(f33)
			if IsDups(nonullf33):
				success = False
				errMsg.append("Duplicates in 3x3 matrix (%s,%s) " %(irow33+1,icol33+1))
			aNums = flatten([nonullRow,nonullCol,nonullf33])
			# make unique
			aNumsUnique = set(aNums)
			# find number "left over"
			numsRemaining = list(legalVals - aNumsUnique)
			numsRemaining.sort()
			if len(cellVal) == 0: # empty cell, so fill with choices
				numsInts = map(int,numsRemaining)
				listPoss.append(numsInts) # convert to integers for better display
				if len(numsInts) == 0:
					success = False
					errMsg.append("No legal choices in location " + cellLoc)
			elif len(cellVal) == 1: # this is one of the one digit input values
				listPoss.append(cellVal)
				if cellVal not in legalVals:
					success = False
					errMsg.append("Not a legal value in location " + cellLoc)
			else: # too many characters
				listPoss.append(cellVal)
				success = False
				errMsg.append("Too many characters in cell location " + cellLoc)
	# Eliminate duplicate messages
	errMsg = list(set(errMsg))
	return [listPoss, success, errMsg]

def stripNulls(xx):
	yy = []
	for nnuls in xx:
		if nnuls:
			yy.append(nnuls) # append if non null
	return yy
	
def partitonToList(xx):
	'''Partition the 9x9 array into a multi level list'''
	outList=[]
	jj=0
	for ii in range(3):
		outList.extend(xx[jj])
		
	yy = xx.copy()
	return yy
