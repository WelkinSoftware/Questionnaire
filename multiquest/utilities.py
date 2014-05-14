from django.utils import timezone
from django.utils.timezone import *
from datetime import datetime
from django.conf import settings
from dateutil.relativedelta import relativedelta
from os import listdir
import os
from os.path import isfile, join
import glob

# ==================================<h3>General Utilities and tools</h3>
# ==================================
# ==================================

def convertCSVMultiLineTo2DList(ptlLinesRaw):
	"""Reformats a transition matrix in the form of a multi-line character string,
	with each line comma separated keywords. Output is a two dimensional list of
	keywords.
	All blanks are removed!
		
	Args:
		a transition matrix in the form of a dictionary of a multi-line character string

	Returns:
		two dimensional list of keywords.

	Raises:
		None.
	"""
	ptlLines = ptlLinesRaw.replace(" ","").splitlines() # remove blanks, then split at end of line
	ptl2DList = []
	for aLineStr in ptlLines:
		aLineListTemp = aLineStr.split(',') # break at commas
		aLineList = filter(None, aLineListTemp) # remove '' null strings when
			# encountering successive commas or a comma at the end of the line.
		ptl2DList.append(aLineList)
		
	return ptl2DList
	
def transitionListToMatrix(tListOfLists):
	"""Reformats a transition matrix in the form of a list of lists of the objects in
	sequence to a dictionary of "from, to" pairs.
		
	Args:
		a transition matrix in the form of a list of lists. Each list element is a list of objects in sequence.

	Returns:
		a dictionary object. "From" is the index, and To is the result.

	Raises:
		None.
	"""
	tMatrixPairs={}
	for aList in tListOfLists:
		aListIter = iter(aList)
		fromItem = next(aListIter)
		for toItem in aListIter:
			tMatrixPairs.update({fromItem : toItem})
			fromItem = toItem
	return tMatrixPairs

def transitionListofList_To_FromToList(tListOfLists):
	"""Reformats a transition matrix in the form of a list of lists of the objects in
	sequence to a list of "from, to" pairs.
	Note:  if only one element on a line, then duplicate the item in the "to" slot
	Args:
		a transition matrix in the form of a list of lists. Each list element is a list of objects in sequence.

	Returns:
		a list of lists object. Output is a list of from/to list pairs

	Raises:
		None.
	"""
	tMatrixPairs=[]
	for aList in tListOfLists:
		aListIter = iter(aList)
		fromItem = next(aListIter)
		if len(aList) == 1:  # length of 1. Repeat the item - no place to go to!
			tMatrixPairs.append([fromItem , fromItem])
		else:
			for toItem in aListIter:
				tMatrixPairs.append([fromItem , toItem])
				fromItem = toItem
	return tMatrixPairs

def transitionMatrixTo2DList(tMatrixPairs):
	"""Reformats a transition matrix in the form of a dictionary of "from, to" pairs into a
	set of lists with the objects in sequence.
		
	Args:
		tMatrixPairs: a transition matrix in the form of a dictionary of "from, to" pairs

	Returns:
		a two dimensional list object. Each list element is a list of objects in sequence.

	Raises:
		None.
	"""
	# investigate all the elements
	DebugOut('transitionMatrixTo2DList: enter')
	if not tMatrixPairs:
		elemToElemListOut = []
		DebugOut('transitionMatrixTo2DList: Exit - input null')
		return elemToElemListOut
	fromSet = set([])
	toSet = set([])
	for pFrom, pTo in tMatrixPairs.iteritems():
		fromSet.add(pFrom)
		toSet.add(pTo)	
	# find elements with no precedent.
	noPrecedent = fromSet - toSet # subtract to from from
# 	if noPrecedent:
# 		DebugOut('Elements with no precedent:  %s' %list(noPrecedent))
	allSet = fromSet | toSet # Union of two sets represent all elements
	numUnique = len(allSet)
	# create a character string representation
	elemToElemListLen = []
	for anItem in noPrecedent:
		currObj = anItem # start at the beginning
# 		DebugOut('currObj:  %s' %currObj)
		consecutiveFromTo = [currObj]
		elementsInThisLine = [] # accumulate elements in this line to avoid infinite loop
		while True:
			try:
				toObj = tMatrixPairs[currObj]
				if toObj in elementsInThisLine:
					break # end the while loop, repeating element.
				elementsInThisLine.append(toObj)
				consecutiveFromTo.append(toObj)
				currObj = toObj
			except KeyError:
				break # ok. Just came to the end of the string
		setEtoE = set(consecutiveFromTo)
		# calculate the number of elements unique to this string
		numUInconsecutive = numUnique - len(allSet-setEtoE) # number of unique consecutive items in a line
		elemToElemListLen.append([numUInconsecutive,consecutiveFromTo])
	# Sort sublist lengths so that the longest is first.
	elemToElemListLen.sort(reverse=True)
	# Restructure the list
	elemToElemListOut = []
	previousElementsRefd = [] # a list of previous elements, going top to bottom
	# Identify the first (and longest) list.
	firstList = elemToElemListLen[0][1]
	
	elemToElemListOut.append(firstList) # start the output list
	previousElementsRefd.extend(firstList) # accumulate the list of unique elements
	# iterate on the remaining lists, if any, in elemToElemListLen
	if len(elemToElemListLen) > 1:
		for [ll,aList] in elemToElemListLen[1:]:
			# go through each element discarding elements already seen
			# with firstList, except for the first appearance of an element already seen
			# this logic shows where this sublist connects with one of the above sublists
			subListElems = []
			for anElm in aList:
				if anElm in previousElementsRefd: # special logic
					subListElems.append(anElm) # reconnects with prior sublist
					break # discard remaining elements, they must duplicate prior sublist
				else:
					subListElems.append(anElm) # add to the list of elements "seen"
					previousElementsRefd.append(anElm) # add to list of previous elements
			elemToElemListOut.append(subListElems)
	#else: # done
	DebugOut('transitionMatrixTo2DList: exit')
	return elemToElemListOut

def transitionMatrixToMultiLineDisplay(tMatrixPairs):
	"""Reformats a transition matrix in the form of a dictionary of "from, to" pairs into a
	set of lists with the objects in sequence. Objects must have a string representation
		
	Args:
		tMatrixPairs: a transition matrix in the form of a dictionary of "from, to" pairs

	Returns:
		a multi-line string. Each page is separated by commas.

	Raises:
		None.
	"""
	PToPTrans2DList = transitionMatrixTo2DList(tMatrixPairs)
	defaultPTList = ''
	for aLine in PToPTrans2DList:
		DebugOut('transitionMatrixToMultiLineDisplay: aLine: %s' %aLine)
		lineStr = ', '.join(aLine)+os.linesep
		DebugOut('transitionMatrixToMultiLineDisplay: lineStr: %s' %lineStr)
		defaultPTList = defaultPTList + lineStr
	DebugOut('transitionMatrixToMultiLineDisplay: defaultPTList: %s' %defaultPTList)
	return defaultPTList
	
def dirListFiles(theStartPath):
	"""Lists files in the directory indicated by theStartPath, with wildcards.
	Default start directory is directory containing manage.py
		
	Args:
		path to a directory

	Returns:
		a list of file names - no path

	Raises:
		None.
	"""
	fileList = glob.glob(theStartPath)
	return fileList

def flattenList(xx):
	"""Flatten all levels in a list of lists to one level."""
	result = []
	for el in xx:
		if type(el) == list:
			result.extend(flattenList(el))
		else:
			result.append(el)
	return result

def removeDupsFromBeginning(aList):
	"""Starting from the beginning of the list, remove duplicates following the original.
		
	Args:
		a list

	Returns:
		a list with duplicates removed

	Raises:
		None.
	"""
	bList = list(aList) # copies the list
	for ii, elm in enumerate(bList):
		if ii > 0: # accept the first element
			if elm in bList[0:ii-1]:
				del bList[ii]
	return bList
	
def removeDupsFromEnd(aList):
	"""Starting from the end of the list, remove duplicates.
		
	Args:
		a list

	Returns:
		a list with duplicates removed

	Raises:
		None.
	"""
	bList = list(aList) # copies the list
	seenList = [] # put elements "seen" here
	for ii, elm in reversed(list(enumerate(bList))):
		if elm in seenList: # remove the duplicate
			del bList[ii]
		else:
			seenList.append(elm) # now we've seen and checked it
	return bList
	
def getModelFieldList( theModel ):
	"""gets all of the fields in a model & foreign keys"""
	fieldList = theModel._meta.get_all_field_names() # returns as a list.
	# We are not done. The problem with fieldList is that it contains the name of tables
	# with foreign keys which point to theModel. Remove these.
	outField = []
	for aField in fieldList:
		try:
			theName = theModel._meta.get_field(aField).name
			outField.append(theName)
		except: # name not in table
			continue
	# http://stackoverflow.com/questions/3106295/django-get-list-of-model-fields
	# https://django-model-internals-reference.readthedocs.org/en/latest/get_all_field_names.html
	return outField

def getModelFieldValueDict( theModel):
	"""Get fields and values from a model. Make a dictionary"""
	fieldList = getModelFieldList( theModel )
	qValueDict = {}
	for aFieldName in fieldList:
		try:
# 			qValueDict.update({aFieldName : unicode(getattr(theModel, aFieldName)).encode('utf-8')})
			qValueDict.update({aFieldName : getattr(theModel, aFieldName)}) # don't coerce!
		except AttributeError:
			pass # some fields (which ones?) will not be attributes of the model
	return qValueDict

def computertype(request): # identifies iPad or not!
	values = request.META.items()
	# tag needed is HTTP_USER_AGENT
	btype = dict(values)['HTTP_USER_AGENT']
	if 'Macintosh' in btype:
		currentComputer = 'Macintosh'
	elif 'iPad' in btype:
		currentComputer = 'iPad'
	elif 'Windows' in btype:
		currentComputer = 'Windows'
	else:
		currentComputer = 'computer'

	return currentComputer

def pagePerComputer( ct):
	DebugOut('pagePerComputer:  enter')
	DebugOut('ct:  %s' %ct)
	pageDetails = {}
	
	if ct == 'iPad':
		pageDetails['fontSize']='1.9em'
		pageDetails['fontSizeTextBox']='.9em'
	else:
		pageDetails['fontSize']='1.2em'
		pageDetails['fontSizeTextBox']='.8em'
	DebugOut('pagePerComputer:  enter')
	return pageDetails
	
def calculate_ptAge_now( bd):
	# convert all times to local timezone
	now = timezone.now()
	nowtz = make_aware(now, timezone.get_current_timezone())
	bdtz = make_aware(bd, timezone.get_current_timezone())
	age = 0
	return age
	
	# another algorithm
	# http://stackoverflow.com/questions/16613960/finding-out-age-in-months-and-years-given-dob-in-a-csv-using-python/16614616#16614616

def getage(now, dob):
	years = now.year - dob.year
	months = now.month - dob.month
	if now.day < dob.day:
		months -= 1
		while months < 0:
			months += 12
			years -= 1
	return '%sy%smo'% (years, months)

def makeUniqueTag( tagList, theTag, maxLength):
	"""Makes a unique tag with respect to "tagList".
	Args:
		tagList - list of character strings
		theTag - character string to test
		maxLength - output character string is not to exceed.
	"""
	# remove from the end of the tag anything like "_integer"
	theNewTag = str(theTag)
	splitTag = theTag.split('_')
	if len(splitTag) == 1:
		firstPart = theTag
	else: # > 1
		lastPart=splitTag[-1]
		try:
			# test for integer
			anInt=int(lastPart)
			# clip off the number
			firstPart=splitTag[0]
		except ValueError:
			# doesn't fit the profile
			firstPart = theTag
	for ii in range(1,100):
		if theNewTag in tagList:
			# conflict, so add the counter
			theNewTag = firstPart+'_'+str(ii)
		else:
			break
	return theNewTag
	
def makeUniqueList( listIn ):
	# output is a list of unique items in listIn with any duplicates following the first are deleted.
	# order is preserved
#	Reference: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
	copyList = []
	copyList.extend(listIn)	# make a local copy of the list
	seen = set()
	return [ x for x in copyList if x not in seen and not seen.add(x)]

def makeUniqueListReverse( listIn ):
	# output is a list of unique items in listIn with any duplicates preceding the last are deleted.
	# order is preserved
#	Reference: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
	copyList = []
	copyList.extend(listIn)	# make a local copy of the list
	copyList.reverse()
	seen = set()
	listOut = [ x for x in copyList if x not in seen and not seen.add(x)]
	listOut.reverse() # restore the original order
	return listOut

def appendToUniqueList( listIn, listAdd):
	# assume listIn consists of unique elements.
	# append listAdd to listIn removing previous duplicates, and appending unique listAdd to the end.
	# Remove duplicates in a list, then if the removed item is in listAdd it is added to the end of the list
	copyList = []
	copyList.extend(listIn)	# make a local copy of the list
	for item in listAdd: # check each element for a duplication # n^2 operation here
		copyList = [x for x in copyList if x != item] # remove all duplicates
	# we have removed all appearances of listAdd elements from copyList, now append listAdd
	copyList.extend(listAdd)
	return copyList

# debug tools ==================================
def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))

def DebugOut( debugMessage):
	#now = timezone.now()
	# open a debug file
	if settings.DEBUG_1:
		try:
			fpage = open('debugInfo.txt','a')
			#fpage.write('mQuest:  Time: %s \n' % now)
			fpage.write( debugMessage + '\n')
			fpage.close()
		except:
			settings.DEBUG_1 = False # persistent for this execution! No further
			pass
	return True

def transposeListMatrix(xx):
	"""Transpose matrix in two level list form"""
	tmat = map(list,zip(*xx)).copy()
	return tmat
	
def testU( debugMessage ):
	print( debugMessage )
	fpage = open('debugInfo.txt','a')
	#fpage.write('mQuest:  Time: %s \n' % now)
	fpage.write( debugMessage + '\n')
	fpage.close()
	
	return True
	
#!/usr/bin/env python

# Ununicode.toascii(): convert perfectly good unicode or utf-8
# strings to puny pathetic plain ascii.

# Copyright 2009 by Akkana Peck.
# Please reuse, modify and otherwise enjoy under the terms
# of the GNU Public License v2 or, at your option, a later version.

# This is ununicode v. 0.4

import unicodedata
import types

def toascii(line, errfilename = None, in_encoding = 'utf-8') :
    """
    Convert a line to plain ascii, making reasonable substitutions
    for accented characters, curly quotes, emdashes etc.
    Unknown characters will be backslash replaced, and
    can also be appended, with context, to an error file.
    Characters in the error file can then be added to the
    xlate table so they will be handled next time.

    Arguments:
    line:        a string or unicode string to be converted to ASCII.
    errfilename: a place to log unknown characters.
    in_encoding: the encoding used if line is a string
    (not used for unicode input).
    web location:  http://shallowsky.com/software/ununicode/ununicode-0.4.py
    """
    # Define the error file. In Python 2.6, the sub-function
    # log_error can see a list but not a scalar variable.
    # So the file pointer has to be errfile[0], not just errfile.
    errfile = [ None, errfilename ]

    # Log an error, giving some context around the problematic area:
    def log_error(uni, start, end, msg="error") :
        contextsize = 15
        if errfile[0] == None :
            if errfilename == None :
                return
            errfile[0] = open(errfile[1], "a")
        unilen = len(uni)
        strstart = start -contextsize
        if strstart < 0 : strstart = 0
        strend = end + contextsize
        if strend > unilen : strend = unilen
        print >>errfile[0], msg, ":", \
            uni[strstart:strend].encode('ascii', 'backslashreplace')
# [ u for u in uni[start:end]]

    output = ''

    # If it's a string, decode it to Unicode.
    # If it's already unicode, no need to do that.
    if type(line) == types.StringType :
        if in_encoding == '' :
            in_encoding = 'utf-8'
            # Slower but safer: try decoding with utf-8 then iso8859-15
        line = line.decode(in_encoding, 'replace')
    elif type(line) != types.UnicodeType :
        return "toascii needs either string or unicode, not" + str(type(line))

    normalized = unicodedata.normalize('NFKD', line)
    while normalized != None :
        try :
            output += normalized.encode('ascii', 'strict')
            # or ignore, replace, etc.
            normalized = None
            break

        except UnicodeEncodeError, e :
            # At this point, e has these useful attributes:
            # e.encoding: 'ascii'
            # e.args: (encoding, unicode, start, end?, message)
            # e.g.    ('ascii', u'\xff', 0, 1, 'ordinal not in range(128)')
            #print e
            #print "\nargs:", e.args
            #print "Error encoding to ascii:", e.args[2], e.args[3]

            # Now turn it into something we can view.

            # Some values unicodedata.normalize().encode doesn't grok:
            # Add to this table as you see characters showing up in
            # your error file.
            xlate = {
                # A few multi-char UTF-8 strings -- some sites, like
                # BBC, persist in throwing in UTF-8 quotes even though
                # they're using another charset like 8859-1.
                u'\x80\x93' : '-',  # UTF-8 endash
                u'\x80\x94' : '--', # UTF-8 emdash
                u'\x80\x98' : '`',  # UTF-8 left single quote
                u'\x80\x99' : '\'', # UTF-8 apostrophe
                # Previous line isn't catching the zillions of hits on BBC,
                # so let's try it without the u prefix.
                # If afterward we get \x80\x9d and \x80\x93
                # but no more \x80\x99, then probably none of these
                # should have the u prefix.
                #'\x80\x99'  : '\'', # UTF-8 apostrophe
                u'\x80\x9c' : '"',  # UTF-8 left double quote
                u'\x80\x9d' : '"',  # UTF-8 right double quote
                u'\x80\xa2' : '*',  # UTF-8 bullet

                # Combining forms.
                # If you don't want to see them (e.g. prefer to see
                # &ntilde; as n rather than n~), replace the matches
                # with '' instead of the characters here.
                u'\u0300' : '`',    # Combining grave accent
                u'\u0301' : '\'',   # Combining acute accent
                u'\u0302' : '^',    # Combining circumflex
                u'\u0303' : '~',    # Combining tilde
                u'\u0304' : '-',    # Combining overscore
                u'\u0306' : '^',    # Combining breve
                u'\u0308' : 'e',    # Combining diaresis
                u'\u030a' : '^',    # Combining ring above
                u'\u030c' : '^',    # Combining caron
                u'\u0327' : ',',    # Combining cedilla?

                # Unicode symbols
                u'\u0131' : 'i',   # unicode dotless i
                u'\u03bc' : '(u)', # mu
                u'\u200b' : '',    # zero-width space (zwsp)
                u'\u2010' : '-',   # hyphen
                u'\u2013' : '-',   # endash
                u'\u2014' : '--',  # emdash
                u'\u2015' : '--',  # horizontal bar
                u'\u2016' : '||',  # double vertical line
                u'\u2018' : '`',   # left single quote
                u'\u2019' : '\'',  # right single quote
                u'\u201a' : ',',   # single low-9 quot. mark (mistaken comma?)
                u'\u201c' : '"',   # left double quote
                u'\u201d' : '"',   # right double quote
                u'\u201e' : '"',   # double low-9 quotation mark
                u'\u2020' : '*',   # dagger
                u'\u2021' : '*',   # double dagger
                u'\u2022' : '*',   # bullet
                u'\u2028' : '_',   # "line separator" -- thereg uses as a space
                u'\u2032' : '\'',  # prime
                u'\u2039' : '&lt;', # left arrow
                u'\u203a' : '&gt;', # right arrow
                u'\u2044' : '/',   # "fraction slash"
                u'\u2190' : '<-',  # left arrow
                u'\u2191' : '^',   # up arrow
                u'\u2192' : '->',  # right arrow
                u'\u2193' : 'v',   # down arrow
                u'\u20ac' : '(EUR)',  # Euro symbol
                u'\u2192' : '-&gt;',  # right arrow
                u'\u25cf' : '*',   # black filled circle
                u'\ufeff' : '',    # Merc uses it, firefox displays nothing
                u'\ufffd' : '\'',  # Yet another apostrophe

                # Characters that oddly don't get translated to unicode:
                u'\x85' : '...',    # BBC uses this for ellipsis, though it's
                                    #   really a Unicode 3.0 newline [NEL]
                u'\x92' : '\'',     # yet another apostrophe
                u'\x93' : '"',      # yet another open quote
                u'\x94' : '"',      # yet another close quote
                u'\x96' : '-',      # yet another endash
                u'\xa1' : '!',      # upside down !
                u'\xa2' : '(c)',    # cents
                u'\xa3' : '(L)',    # UK pounds
                u'\xa5' : '(Y)',    # Yen
                u'\xa7' : '(sect)', # Section sign
                u'\xa8' : ':',      # umlaut
                u'\xa9' : '-',      # maybe an emdash?
                u'\xab' : '<<',     # left German quote
                u'\xad' : '-',      # emdash
                u'\xae' : '(R)',    # Registered trademark
                u'\xb0' : '^',      # degree
                u'\xb1' : '+/1',    # plus/minus
                u'\xb6' : 'PP',     # paragraph
                u'\xb7' : '*',      # mid dot
                u'\xbb' : '>>',     # left German quote
                u'\xbf' : '?',      # Spanish upside-down question mark
                u'\xc6' : 'ae',     # ae ligature
                u'\xd7' : 'x',      # math, times
                u'\xd8' : 'O/',     # O-slash
                u'\xdf' : 'ss',     # German ss ligature (like a beta)
                u'\xf8' : 'o/',     # o slash
                }

            # Encode the first part of the string, up to the error point.
            # Use backslashreplace even though there shouldn't be any errs.
            s = normalized[0:e.args[2]].encode('ascii', 'backslashreplace')

            # e.args[3] is supposedly the end point, but encode() isn't
            # smart enough to notice most multi-char sequences, so
            # in practice it's always e.args[2]+1.
            bad_u = normalized[e.args[2]:]
            if xlate.has_key(bad_u[0]) :
                s += xlate[bad_u[0:1]]
                normalized = normalized[e.args[2] + 1 : ]
            else :
                s += bad_u[0].encode('ascii', 'backslashreplace')
                log_error(e.args[1], e.args[2], e.args[3], e.args[4])
                normalized = normalized[e.args[3]:]

            # print with no newline OR space:
            output += s
            continue

    if errfile[0] != None :
        errfile[0].close()
    return output
