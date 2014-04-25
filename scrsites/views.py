from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, render, get_object_or_404
from django.conf import settings
from django import forms
from scrsites.forms import (p0Form, p1Form, p2Form, aboveAverageRiskForm, AverageRiskForm, 
	IndetermRiskForm, p3Form, p3aForm, p3bForm, p3cForm, p4Form, p4aForm, p4bForm, p5Form, 
	p4b_Agg_queryForm, p3c_Agg_queryForm, setDebugOptionsForm)
from scrsites.models import PatientBRCADataEntry, nonPtInfo, RiskNames
from datetime import datetime
#from dateutil.relativedelta import relativedelta

import csv
import unicodedata

def scrnrAdmin(request):	# for screener site administration
	return render_to_response('Site Welcome page/Welcome.html', {'current_date' : datetime.now(), 'thishost' : request.get_host(), 'imageloc' : settings.MEDIA_URL, 'urlprefix' : settings.WSGI_URL_PREFIX, "debug" : settings.DEBUG})

def scrnr(request, quickExit): # Splash screen. Check for cookie function. Start session. Optionally flush session data
	now = datetime.now()
	if 'specialDebugOutput' in request.session: # carry it through the impending flush
		specialDebugOutput = request.session["specialDebugOutput"]
	else:
		specialDebugOutput = False
	sessionFlush = True # default always for now ****************
	if sessionFlush:	# Delete all previous local data
		request.session.flush()
	request.session.set_test_cookie() # Set test cookie to test in next POST
	# restore special debug flag
	if specialDebugOutput: # If true, restore it
		request.session["specialDebugOutput"] = specialDebugOutput
	
	# Initialize session data
	request.session["quickExit"] = quickExit	# true or false for Quick Exit logic

	if request.method == 'POST':
		if not request.session.test_cookie_worked(): # check for cookie function
			return render(request, 'screener/spl.html', {'errmsg': "Please enable cookies in your browser."})
		request.session.set_expiry(settings.SESSION_EXPIRE_AT_AGE) # sessions data expires at fixed age
		if quickExit:
			request.session["last_url"] = ["quickExit"] # records this url visited. Initialize
			request.session["splash_url"] = "quickExit/" # record the questionnaire start page in Session data
		else:
			request.session["last_url"] = [""] # records this url visited. Initialize.
			request.session["splash_url"] = "" # record the questionnaire start page in Session data
		request.session["highRiskExit"] = False		# start out with no risk
		
		if specialDebugOutput: # If true, start a debug file
			# open a debug file
			fpage = open('debugInfo.txt','w')
			fpage.write("scrnr (POST):  Time: %s \n" % now)
			fpage.write("scrnr: fast mode is %s\n" % request.session["quickExit"])
			fpage.write("scrnr: last url: %s\n" %request.session["last_url"])
			fpage.write("scrnr: splash url: %s\n" %request.session["splash_url"])
			fpage.close()
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p0')
	return render(request, 'screener/spl.html', {'current_date' : now, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, "quickExit" : quickExit, "errmsg" : "", 
		'specialDebugOutput' : specialDebugOutput, 
		"debugMode" : settings.DEBUG})

def browsertype(request): # identifies iPad or not!
	values = request.META.items()
	# tag needed is HTTP_USER_AGENT
	btype = dict(values)['HTTP_USER_AGENT']
	if 'Safari' in btype:
		currentBrowser = 'Safari'	
	elif 'Windows' in btype:
		currentBrowser = 'Windows'	
	else:
		currentBrowser = 'Unknown'
		
	outstr = "browser type is %s" % currentBrowser
	return HttpResponse(outstr)
	
def url_host_user_agent(request): # returns entire string
	values = request.META.items()
	# tag needed is HTTP_USER_AGENT
	return dict(values)['HTTP_USER_AGENT']

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

def scrnrexpln(request, whichpage): #all explanations
	
	if "this_page" in request.session:
		back_to = settings.WSGI_URL_PREFIX + 'scrn/' + request.session["this_page"] # end of stack is previous page
	else:
		back_to = settings.WSGI_URL_PREFIX + 'scrn/'		

	if whichpage == "ashkenazijewishrelatives":
		return render(request, 'screener/Explanations/ashkenazijewishrelatives.html', { "back_to" : back_to})
	if whichpage == "brcatesting":
		return render(request, 'screener/Explanations/brcatesting.html', { "back_to" : back_to})
	if whichpage == "closebloodrelatives":
		return render(request, 'screener/Explanations/closebloodrelatives.html', { "back_to" : back_to})
	if whichpage == "moreonbreastca":
		return render(request, 'screener/Explanations/moreonbreastca.html', { "back_to" : back_to})
	if whichpage == "ovca":
		return render(request, 'screener/Explanations/ovca.html', { "back_to" : back_to})
	if whichpage == "skininbreastca":
		return render(request, 'screener/Explanations/skininbreastca.html', { "back_to" : back_to})
	# if none of the above, return to the general explanations page.
	return render_to_response('screener/explanations.html')

def setDebugOptions( request ):
	

	this_page = 'setDebugOptions'
	next_page = ''
	back_to = ''
	baseURL = 'scrn/' # base url for page locations
	urlprefix = settings.WSGI_URL_PREFIX
	templatebaseURL = 'screener/' # base url for template (html file) locations

	if request.method == 'POST':
		form = setDebugOptionsForm(request.POST)		
		if form.is_valid():
			for item in form: # move the form data to session data
				request.session[item.html_name] = form.cleaned_data[item.html_name]
			return HttpResponseRedirect(urlprefix + baseURL+next_page) # next screen url
	errmsg = ""
	form = setDebugOptionsForm()
	# fill fields with previously entered data from this session
	form_kwkv = []
	for item in form:
		if item.html_name in request.session:
			form_kwkv.append( [ item.html_name, request.session[item.html_name] ] )
	if form_kwkv != []: # check if any fields filled
		form_dict = dict(form_kwkv)
		form = setDebugOptionsForm(form_dict) # populate with values

	return render(request, templatebaseURL+this_page+'.html', {'this_page' : this_page,
	'errmsg' : errmsg,'urlprefix' : urlprefix, 'baseURL' : baseURL, 'back_to' : back_to,
	'form': form})	

def pageCalc( request ):
	# calculates the next page given the current state of the session data.

	if "last_url" in request.session:
		current_page = request.session["last_url"][-1] # end of the queue
	else:
		current_page = ""
		
	# first check for quickExit, if not quick, then slow
	if "quickExit" not in request.session:
		request.session["quickExit"] = False
	
	if request.session["quickExit"] and CheckPtReferral(request):
			nextPageUp = 'aboveAverageRisk'
	else:
		if current_page == '' or current_page == 'quickExit':	# at the splash screen
			nextPageUp = 'p0'
		elif current_page == 'p0':
			nextPageUp = 'p1'
		elif current_page == 'p1':
			nextPageUp = 'p2'
		elif current_page == 'p2':
			nextPageUp = 'p3'
		else:
			nextPageUp = current_page # return to the same page
	if 'specialDebugOutput' in request.session and request.session['specialDebugOutput']:
		fpage = open('debugInfo.txt','a')
		fout = "pageCalc: current page '%s', next page '%s' \n" %(current_page,nextPageUp)
		fpage.write(fout)
	return nextPageUp

def p0(request):

	allpms = {
		'this_page' : 'p0',
		'next_page' : 'p1',
		'field_style' : 'as_p' # as "table", "p" or "ul"
		}
	allLocs = {
		'baseURL' : 'scrn/', # base url for page locations
		'templatebaseURL' : 'screener/', # base url for template (html file) locations
		}		
	return page_now(request, p0Form, allpms, allLocs)

def page_now( request, theForm, allparams, allLocs ):
	baseURL = allLocs['baseURL']
	urlprefix = settings.WSGI_URL_PREFIX

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/') # start over

	if 'specialDebugOutput' in request.session:
		specialDebugOutput = request.session["specialDebugOutput"]
	else:
		specialDebugOutput = False

	if specialDebugOutput:
		fpage = open('debugInfo.txt','a')
		fpage.write("Page_now: STARTING\n")
		if "last_url" in request.session:
			fpage.write("Page_now: ****start of page list\n")
			for item in request.session["last_url"]:
				fout = "Page_now: Page list '%s'\n" % item
				fpage.write(fout)
			fpage.write("Page_now: ****end of page list\n")
		else:
			fpage.write("Page_now: last_url not in Session data\n")
			
	
	this_page = allparams['this_page'] #**** Must be present
	if "last_url" in request.session:
		if len(request.session["last_url"]) > 1: # detect immediate duplicates
			if request.session["last_url"][-1] == this_page:
				request.session["last_url"].pop()	# assume the previous page is different from this page
				request.session.modified = True	# save the session changes
	else:
		request.session["last_url"] = [this_page]
	
	back_to = request.session["last_url"][-1]

	if "session_errors" in request.session: # log the error
		errmsg = request.session["session_errors"]
	else:
		errmsg = False

	if "quickExit" in request.session: # quick exit option
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else: # if not set then assume False - "slow exit"
		quickExit = False
		
	if specialDebugOutput:
		fout = "Page_now: current page %s, back to %s , errmsg: %s\n" %(this_page,back_to, errmsg)
		fpage.write(fout)
		fout = "Page_now: quickExit mode value: %s\n" %quickExit
		fpage.write(fout)

	# fill fields with previously entered data from this session
	form = theForm()
	form_kwkv = []
	for item in form:
		if specialDebugOutput:
			fpage.write("page_now: checking previous value for: %s\n" % item.html_name)
		if item.html_name in request.session:
			form_kwkv.append( [ item.html_name, request.session[item.html_name] ] )
			if specialDebugOutput:
				fpage.write("page_now: filling previous value for: %s, %s\n" % (item.html_name, request.session[item.html_name]))
	if form_kwkv != []: # check if any fields filled
		form_dict = dict(form_kwkv)
		form = theForm(form_dict) # populate with values
		if specialDebugOutput:
			fpage.write("page_now: fill previously entered data\n")

	if request.method == 'POST':
		form = theForm(request.POST)	
		if specialDebugOutput:	
			fpage.write("page_now: POST Starting\n")
			fpage.write("page_now: form.errors %s\n" % form.errors)
		if form.is_valid():
			localRisk = False
			if specialDebugOutput:
				fpage.write("page_now: POST, form is valid\n")
			for item in form: # move the form data to session data
				cleanedItem = form.cleaned_data[item.html_name]
				if specialDebugOutput:
					fpage.write("page_now: item.html_name: %s, type: %s\n" % (item.html_name, type(cleanedItem)))
				if type(cleanedItem) == bool: # Convert to "Yes" or "No"
					if cleanedItem:
						cleanedItem = "Yes" # redefine to string
					else:
						cleanedItem = "No"
				request.session[item.html_name] = cleanedItem # Always a string
				if cleanedItem == 'Yes': # flag if a risk is found
					localRisk = True
			request.session["last_url"].append(this_page) # records this url visited.
			if localRisk:
				request.session["highRiskExit_"+this_page] = True # set Session data flag
			else:
				request.session["highRiskExit_"+this_page] = False # set Session data flag
			if "next_page" in allparams: # allow an override in parameter list
				next_page = allparams["next_page"]
			else:
				next_page = pageCalc( request )
			if specialDebugOutput:
				fpage.write("page_now: POST this page %s, next page: %s\n" % (this_page, next_page))
			if localRisk:
				if specialDebugOutput:
					fpage.write("Risk identified on page %s\n" % this_page)
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk') # quick exit screen url					
			return HttpResponseRedirect(urlprefix + baseURL+next_page) # next screen url
		else:
			if specialDebugOutput:
				fpage.write("page_now: POST, form is invalid\n")
	
	request.session["this_page"] = this_page # for return from explanation urls in template
	
	if specialDebugOutput:
		fpage.write("page_now: EXITING, errmsg: %s\n" % errmsg)

	if 'imageBaseURL' in allLocs: # check for an image
		imageBaseURL = allLocs['imageBaseURL']
	else:
		imageBaseURL = settings.MEDIA_URL
	computerT = computertype(request)
	inparams = {'form': form, 'imageloc' : settings.MEDIA_URL,
		'urlprefix' : urlprefix, 'back_to' : back_to, 'this_page' : this_page, 
		'errmsg' : errmsg,
		'baseURL' : allLocs['baseURL'],
		'computerT' : computerT,
		'field_style' : allparams['field_style'], 'imageBaseURL' : imageBaseURL}
	templatebaseURL = allLocs['templatebaseURL']
	return render(request, templatebaseURL+this_page+'.html', inparams)	

def p0_old(request): # collect pt name & bd

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
			
	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	# fill fields with previously entered data from this session
	# query Session data for previously entered pt name & bd
	if "patientName" in request.session: # if one is present, both will be present
		patientName = request.session['patientName']
		birthDate = request.session['birthDate']
		if "ptEmail" in request.session:
			ptEmail = request.session['ptEmail']
		else:
			ptEmail = ""
		form = p0Form({'patientName': patientName, 'birthDate': birthDate, 'ptEmail' : ptEmail}) # set initial data
	else:
		patientName = ""
		birthDate = ""
		ptEmail = ""
		form = p0Form()
		
	back_to = request.session["splash_url"] # force the back key to the splash screen with quickexit option
	now = datetime.now()
	errmsg = ""
	if request.method == 'POST':
		form = p0Form(request.POST)
		if form.is_valid():
			request.session["last_url"] = ["p0"] # records this url visited. Initialize the url stack
			request.session["patientName"] = form.cleaned_data['patientName'].title() # capitalize each word
			birthDate = request.session["birthDate"] = form.cleaned_data['birthDate']
			request.session["ptEmail"] = form.cleaned_data['ptEmailF']
			# check birthdate to be before today!
			ptAge = calculate_ptAge_now( birthDate)
			if ptAge < 0:
				errmsg = "Your birthdate must be before today!"
			else:
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p1') # next screen url
	return render(request, 'screener/p0.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to, "errmsg" : errmsg})
	
def uniquePTID(patientName, birthDate):
	# construct a unique patient id
	patientName = patientName.title() # capitalize each word to reduce variation
	uid = "%s %s" % (birthDate, patientName)
	return uid

	
def savePtResponse(request):

	# get the data
	field_list = ['patientName',
		'birthDate', 'ptEmail', 'entryDate', 'referralDecision', 'patientCallbackNumber',
		'pHxOvarianCA',
		'fHxOvarianCA', 'recognizedRiskGroup',
		'ashkenaziJewish', 'pHxBreastCA', 'fHxBreastCA', 'fHxBrCASuscGene',
		'fHxSufficient', 'pHxBrCARiskGroupA', 'pHxBrCALE50Years', 'pHxBrCA3Neg',
		'pHxBrCAGT1PrimarySame', 'pHxBrCAGT1PrimaryBoth', 'pHxBrCADermMan', 'pHxBrCARiskGroupB',
		'pHxBrCAGE1RelBrCALE50Years', 'pHxBrCAGE2RelBrPancCA', 'pHxBrCARiskGroupC', 'pHxBrCAThyroidCA',
		'pHxBrCASarcoma', 'pHxBrCAAdrenalCA', 'pHxBrCAEndometrialCA', 'pHxBrCAPancreaticCA',
		'pHxBrCABrainTumors', 'pHxBrCAGastricCA', 'pHxBrCALeukLymphoma', 'fHxBrCARiskGroupA',
		'fHxBrCAMale', 'fHxBrCASameSideGE2', 'fHxBrCARiskGroupB', 'fHxBrCADermMan',
		'fHxBrCAThyroidCA', 'fHxBrCASarcoma', 'fHxBrCAAdrenalCA', 'fHxBrCAEndometrialCA',
		'fHxBrCAPancreaticCA', 'fHxBrCABrainTumors', 'fHxBrCAGastricCA', 'fHxBrCALeukLymphoma'
		]
	#this is the "session name" for the database field data
	field_session_id = ['patientName',
		'birthDate', 'ptEmail', 'entryDate', 'referralDecision', 'patientCallbackNumber',
		'pHxOvarianCA',
		'fHxOvarianCA', 'recognizedRiskGroup',
		'ashkenaziJewish', 'pHxBreastCA', 'fHxBreastCA', 'fHxBrCASuscGene',
		'fHxSufficient', 'pHxBrCARiskGroupA', 'pHxBrCALE50Years', 'pHxBrCA3Neg',
		'pHxBrCAGT1PrimarySame', 'pHxBrCAGT1PrimaryBoth', 'pHxBrCADermMan', 'pHxBrCARiskGroupB',
		'pHxBrCAGE1RelBrCALE50Years', 'pHxBrCAGE2RelBrPancCA', 'pHxBrCARiskGroupC', 'pHxBrCAThyroidCA',
		'pHxBrCASarcoma', 'pHxBrCAAdrenalCA', 'pHxBrCAEndometrialCA', 'pHxBrCAPancreaticCA',
		'pHxBrCABrainTumors', 'pHxBrCAGastricCA', 'pHxBrCALeukLymphoma', 'fHxBrCARiskGroupA',
		'fHxBrCAMale', 'fHxBrCASameSideGE2', 'fHxBrCARiskGroupB', 'fHxBrCADermMan',
		'fHxBrCAThyroidCA', 'fHxBrCASarcoma', 'fHxBrCAAdrenalCA', 'fHxBrCAEndometrialCA',
		'fHxBrCAPancreaticCA', 'fHxBrCABrainTumors', 'fHxBrCAGastricCA', 'fHxBrCALeukLymphoma'
		]
	if "session_errors" not in request.session: # log the error
		request.session["session_errors"] = []	# create it

	request.session.modified = True	# save the session changes
	
	if "patientName" in request.session: # if one is present, both will be present
		patientName = request.session["patientName"]
		birthDate = request.session["birthDate"]
	else:
		request.session["session_errors"].append("Patient name not found in Session data.")
		request.session.modified = True	# save the session changes
		return False # Responses NOT saved to database

	# Create patient response record
	now = datetime.now()
	patientName = request.session["patientName"]
	birthDate = request.session["birthDate"]
	ptRecord=PatientBRCADataEntry(entryDate=now,
		patientName=patientName,
		birthDate=birthDate,
		patientUniqueID=uniquePTID(patientName, birthDate),
		)
		
	if "ptEmail" in request.session:	
		ptRecord.ptEmail=request.session["ptEmail"]
	if "referralDecision" in request.session:
		ptRecord.referralDecision = request.session["referralDecision"]
	if "patientCallbackNumber" in request.session:
		ptRecord.patientCallbackNumber = request.session["patientCallbackNumber"]
	if "pHxOvarianCA" in request.session:
		ptRecord.pHxOvarianCA = request.session["pHxOvarianCA"]
	if "fHxOvarianCA" in request.session:
		ptRecord.fHxOvarianCA = request.session["fHxOvarianCA"]
	if "recognizedRiskGroup" in request.session:
		ptRecord.recognizedRiskGroup = request.session["recognizedRiskGroup"]
	if "ashkenaziJewish" in request.session:
		ptRecord.ashkenaziJewish = request.session["ashkenaziJewish"]
	if "pHxBreastCA" in request.session:
		ptRecord.pHxBreastCA = request.session["pHxBreastCA"]
	if "fHxBreastCA" in request.session:
		ptRecord.fHxBreastCA = request.session["fHxBreastCA"]
	if "fHxBrCASuscGene" in request.session:
		ptRecord.fHxBrCASuscGene = request.session["fHxBrCASuscGene"]
	if "fHxSufficient" in request.session:
		ptRecord.fHxSufficient = request.session["fHxSufficient"]
	if "pHxBrCARiskGroupA" in request.session:
		ptRecord.pHxBrCARiskGroupA = request.session["pHxBrCARiskGroupA"]
	if "pHxBrCALE50Years" in request.session:
		ptRecord.pHxBrCALE50Years = request.session["pHxBrCALE50Years"]
	if "pHxBrCA3Neg" in request.session:
		ptRecord.pHxBrCA3Neg = request.session["pHxBrCA3Neg"]
	if "pHxBrCAGT1PrimarySame" in request.session:
		ptRecord.pHxBrCAGT1PrimarySame = request.session["pHxBrCAGT1PrimarySame"]
	if "pHxBrCAGT1PrimaryBoth" in request.session:
		ptRecord.pHxBrCAGT1PrimaryBoth = request.session["pHxBrCAGT1PrimaryBoth"]
	if "pHxBrCADermMan" in request.session:
		ptRecord.pHxBrCADermMan = request.session["pHxBrCADermMan"]
	if "pHxBrCARiskGroupB" in request.session:
		ptRecord.pHxBrCARiskGroupB = request.session["pHxBrCARiskGroupB"]
	if "pHxBrCARiskGroupB" in request.session:
		ptRecord.pHxBrCARiskGroupB = request.session["pHxBrCARiskGroupB"]
	if "pHxBrCAGE1RelBrCALE50Years" in request.session:
		ptRecord.pHxBrCAGE1RelBrCALE50Years = request.session["pHxBrCAGE1RelBrCALE50Years"]
	if "pHxBrCAGE2RelBrPancCA" in request.session:
		ptRecord.pHxBrCAGE2RelBrPancCA = request.session["pHxBrCAGE2RelBrPancCA"]
	if "pHxBrCARiskGroupC" in request.session:
		ptRecord.pHxBrCARiskGroupC = request.session["pHxBrCARiskGroupC"]
	if "pHxBrCAThyroidCA" in request.session:
		ptRecord.pHxBrCAThyroidCA = request.session["pHxBrCAThyroidCA"]
	if "pHxBrCASarcoma" in request.session:
		ptRecord.pHxBrCASarcoma = request.session["pHxBrCASarcoma"]
	if "pHxBrCAAdrenalCA" in request.session:
		ptRecord.pHxBrCAAdrenalCA = request.session["pHxBrCAAdrenalCA"]
	if "pHxBrCAEndometrialCA" in request.session:
		ptRecord.pHxBrCAEndometrialCA = request.session["pHxBrCAEndometrialCA"]
	if "pHxBrCAPancreaticCA" in request.session:
		ptRecord.pHxBrCAPancreaticCA = request.session["pHxBrCAPancreaticCA"]
	if "pHxBrCABrainTumors" in request.session:
		ptRecord.pHxBrCABrainTumors = request.session["pHxBrCABrainTumors"]
	if "pHxBrCAGastricCA" in request.session:
		ptRecord.pHxBrCAGastricCA = request.session["pHxBrCAGastricCA"]
	if "pHxBrCALeukLymphoma" in request.session:
		ptRecord.pHxBrCALeukLymphoma = request.session["pHxBrCALeukLymphoma"]
	if "fHxBrCARiskGroupA" in request.session:
		ptRecord.fHxBrCARiskGroupA = request.session["fHxBrCARiskGroupA"]
	if "fHxBrCAMale" in request.session:
		ptRecord.fHxBrCAMale = request.session["fHxBrCAMale"]
	if "fHxBrCASameSideGE2" in request.session:
		ptRecord.fHxBrCASameSideGE2 = request.session["fHxBrCASameSideGE2"]
	if "fHxBrCARiskGroupB" in request.session:
		ptRecord.fHxBrCARiskGroupB = request.session["fHxBrCARiskGroupB"]
	if "fHxBrCADermMan" in request.session:
		ptRecord.fHxBrCADermMan = request.session["fHxBrCADermMan"]
	if "fHxBrCAThyroidCA" in request.session:
		ptRecord.fHxBrCAThyroidCA = request.session["fHxBrCAThyroidCA"]
	if "fHxBrCASarcoma" in request.session:
		ptRecord.fHxBrCASarcoma = request.session["fHxBrCASarcoma"]
	if "fHxBrCAAdrenalCA" in request.session:
		ptRecord.fHxBrCAAdrenalCA = request.session["fHxBrCAAdrenalCA"]
	if "fHxBrCAEndometrialCA" in request.session:
		ptRecord.fHxBrCAEndometrialCA = request.session["fHxBrCAEndometrialCA"]
	if "fHxBrCAPancreaticCA" in request.session:
		ptRecord.fHxBrCAPancreaticCA = request.session["fHxBrCAPancreaticCA"]
	if "fHxBrCABrainTumors" in request.session:
		ptRecord.fHxBrCABrainTumors = request.session["fHxBrCABrainTumors"]
	if "fHxBrCAGastricCA" in request.session:
		ptRecord.fHxBrCAGastricCA = request.session["fHxBrCAGastricCA"]
	if "fHxBrCALeukLymphoma" in request.session:
		ptRecord.fHxBrCALeukLymphoma = request.session["fHxBrCALeukLymphoma"]

	if request.session["quickExit"]:
		ptRecord.questionnaireMode = "quickExit"
	else:
		ptRecord.questionnaireMode = "slowExit"
			
	try:
		qtitle = nonPtInfo.objects.get(id=1) # get the first and only record
		ptRecord.questionnaireTitle = qtitle.questionnaireTitle
	except:
		ptRecord.questionnaireTitle = ""
		
#	for ii in range(len(field_session_id)):
#		if field_session_id[ii] in request.session: #connect session data to db
#			sessNamforField = field_session_id[ii]
#			dbNam = field_list[ii]
#			ptRecord.dbNam = request.session[sessNamforField]

	# delete any matching patient data record. It will be replaced by the 
	# current session data
	uidSearch = uniquePTID(patientName, birthDate) # find the unique id for the patient
	PatientBRCADataEntry.objects.filter(patientUniqueID=uidSearch).delete() # delete if found.

	ptRecord.save()
	
	return True # Responses saved to database
	
def LR():

	riskText = [
		["pHxOvarianCA", "I have had ovarian cancer.", "I have never had ovarian cancer."],
		["fHxOvarianCA", "One or more of my close blood relatives has had ovarian cancer.", "None of my close blood relatives ever had ovarian cancer."],
		["recognizedRiskGroup", "I have at least one close blood relative who is Ashkenazi Jewish.", "I have no close blood relative who is Ashkenazi Jewish"],
		["ashkenaziJewish", "I have at least one close blood relative who is Ashkenazi Jewish.", "I do not have a close blood relative who is Ashkenazi Jewish."],
		["pHxBreastCA", "I have had breast cancer.", "I have never had breast cancer."],
		["fHxBreastCA", "One or more of my close blood relatives has had breast cancer.", "None of my close blood relatives had breast cancer"],
		["fHxBrCASuscGene", "One or more of my close blood relatives has been confirmed to have BRCA gene mutations.", "No close blood relatives have been confirmed to have BRCA gene mutations."],
		["pHxBrCALE50Years","I was under 51 years old when my breast cancer was first diagnosed.","I was not under 51 years old when my breast cancer was first diagnosed."],
		["pHxBrCA3Neg", """My cancer was described as "triple negative", not having receptors for estrogen, progesterone and HER2.""", """My cancer was not described as "triple negative", not having receptors for estrogen, progesterone and HER2."""],
		["pHxBrCAGT1PrimarySame", "My cancer was found in more than one location of the same breast.", "My cancer was not found in more than one location of the same breast."],
		["pHxBrCAGT1PrimaryBoth", "I had cancer in both breasts.", "I had cancer in only one breasts."],
		["pHxBrCADermMan", "My breast cancer involved the skin overlying the breast.", "My breast cancer did not involve the skin overlying the breast."],
		["pHxBrCAGE1RelBrCALE50Years", "I have close blood relatives with breast cancer who were diagnosed at age 50 years or younger.", "I do not have close blood relatives with breast cancer who were diagnosed at age 50 years or younger."],
		["pHxBrCAGE2RelBrPancCA", "I have two or more close blood relatives with breast or pancreatic cancer at any age.", "I do not have two or more close blood relatives with breast or pancreatic cancer at any age."],
		["pHxBrCAThyroidCA", "I have had thyroid cancer.", "I have not had thyroid cancer."],
		["pHxBrCASarcoma", "I have had a sarcoma.", "I have not had a sarcoma."],
		["pHxBrCAAdrenalCA", "I have had adrenal cancer.", "I have not had adrenal cancer."],
		["pHxBrCAEndometrialCA", "I have had cancer of the uterus.", "I have not had cancer of the uterus."],
		["pHxBrCAPancreaticCA", "I have had pancreatic cancer.", "I have not had pancreatic cancer."],
		["pHxBrCABrainTumors", "I have had brain tumors.", "I have not had brain tumors."],
		["pHxBrCAGastricCA", "I have had stomach cancer.", "I have not had stomach cancer."],
		["pHxBrCALeukLymphoma", "I have had leukemia or lymphoma.", "I have not had leukemia or lymphoma."],
		["fHxBrCAMale", "A male close blood relative has had breast cancer.", "No male blood relative has had breast cancer."],
		["fHxBrCASameSideGE2", "Two or more close blood relatives from the same side (mother's or father's) of my family had breast cancer.", "It is not true that two or more close blood relatives from the same side (mother's or father's) of my family had breast cancer."],
		["fHxBrCADermMan", "One or more of my close blood relatives has had breast cancer involving the skin overlying the breast.", "None of my close blood relatives has had breast cancer involving the skin overlying the breast."],
		["fHxBrCAThyroidCA", "One or more close blood relatives had thyroid cancer.", "None of my close blood relatives had thyroid cancer."],
		["fHxBrCASarcoma", "One or more close blood relatives had a sarcoma.", "None of my close blood relatives had a sarcoma."],
		["fHxBrCAAdrenalCA", "One or more close blood relatives had adrenal cancer.", "None of my close blood relatives had adrenal cancer."],
		["fHxBrCAEndometrialCA", "One or more close blood relatives had uterine cancer.", "None of my close blood relatives had uterine cancer."],
		["fHxBrCAPancreaticCA", "One or more close blood relatives had pancreatic cancer.", "None of my close blood relatives had pancreatic cancer."],
		["fHxBrCABrainTumors", "One or more close blood relatives had brain tumors.", "None of my close blood relatives had brain tumors."],
		["fHxBrCAGastricCA", "One or more close blood relatives had diffuse gastric cancer.", "None of my close blood relatives had diffuse gastric cancer."],
		["fHxBrCALeukLymphoma", "One or more close blood relatives had leukemia or lymphoma.", "None of my close blood relatives had leukemia or lymphoma."],
	]
	# Delete previous entries
	RiskNames.objects.all().delete() # delete all records if any found.

	looptx=0
	for ii in range(len(riskText)):
		row = riskText[ii]
		try:
			rText=RiskNames( riskID=row[0], riskDeclarYes=row[1], riskDeclarNo=row[2])
			rText.save()
			looptx += 1
		except:
			LoadFail = True
	
	LoadFail = False
	current_date = datetime.now()
	return current_date
	
def p1(request):
	
	allpms = {
		'this_page' : 'p1',
		'next_page' : 'p2',
		'field_style' : 'as_p' # as "table", "p" or "ul"
		}
	allLocs = {
		'baseURL' : 'scrn/', # base url for page locations
		'templatebaseURL' : 'screener/', # base url for template (html file) locations
		'imageBaseURL' : settings.MEDIA_URL # base for images
		}
	return page_now(request, p1Form, allpms, allLocs)
	
def p1_old(request):  # query for ovarian cancer

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	this_page = "p1"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False
		
	# fill fields with previously entered data from this session
	if "pHxOvarianCA" in request.session:
		form = p1Form({'pHxOvarianCA': request.session['pHxOvarianCA']}) # set previous value
	else:
		form = p1Form() # no initial data
		
	if request.method == 'POST':
		form = p1Form(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["pHxOvarianCA"] = form.cleaned_data['pHxOvarianCA']
			if request.session["pHxOvarianCA"] == 'Yes': # answered yes, so record in risk list
				request.session["highRiskExit_p1"] = True # Take the high risk exit screen, whenever executed
				if quickExit:	# quick exit at first risk
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk') # quick exit screen url
			else:
				request.session["highRiskExit_p1"] = False # No referral required
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p2') # next screen url
	if "session_errors" in request.session: # log the error
		diagMess = request.session["session_errors"]
	else:
		diagMess = "False"
		
	diagMess = "" # in production
	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p1.html', {'form': form, 'imageloc' : settings.MEDIA_URL,
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to, 'diagMess' : diagMess})

def SessionListAppend(request, listName, itemToAdd ): # Append an item to a list if not already there. Maintain in session data.
	if listName not in request.session:
		accumulated_list = request.session[listName] = []
	else:
		accumulated_list = request.session[listName]
	# check that itemToAdd doesn't already exist!
	if itemToAdd not in accumulated_list:
		accumulated_list.append( itemToAdd ) # so add it
	
	request.session[listName] = accumulated_list # replace the accumulated risk with new one added
	return accumulated_list # return the accumulated risk list

def SessionListNull(request, listName ):
	request.session[listName] = []
	return []
	
def SessionListRemoveItem(request, listName, itemToRemove ):
	if listName not in request.session:
		accumulated_list = request.session[listName] = [] # initialize to null list
	else:
		accumulated_list = request.session[listName]
	if itemToRemove in accumulated_list:
		accumulated_list.remove(itemToRemove) # remove first occurrence of the item
	request.session[listName] = accumulated_list # replace the accumulated risk with deletion
	return accumulated_list # return the accumulated risk list
	
def RiskListToText(request): # output list of text strings stating pt responses regarding risk.

	riskListdb = RiskNames.objects.all() # retrieve all possible risks from database

	riskList = [] # initialize the text list
	for ii in range(len(riskListdb)):
		if riskListdb[ii].riskID in request.session:
			if request.session[riskListdb[ii].riskID] == "Yes":
				riskList.append(riskListdb[ii].riskDeclarYes)
	return riskList
	
def AllPtResponseToText(request): # output list of text strings stating all of the pt responses on all pages.

	riskListdb = RiskNames.objects.all() # retrieve all possible risks from database

	ptResponseList = [] # initialize the text list
	for ii in range(len(riskListdb)):
		if riskListdb[ii].riskID in request.session:
			if request.session[riskListdb[ii].riskID] == "Yes":
				ptResponseList.append(riskListdb[ii].riskDeclarYes)
			elif request.session[riskListdb[ii].riskID] == "No":
				ptResponseList.append(riskListdb[ii].riskDeclarNo)
			else:
				ptResponseList.append("No response to %s" % riskListdb[ii].riskID)
			
	
	return ptResponseList

def p2(request):

	allpms = {
		'this_page' : 'p2',
		'field_style' : 'as_p' # as "table", "p" or "ul"
		}
	allLocs = {
		'baseURL' : 'scrn/', # base url for page locations
		'templatebaseURL' : 'screener/', # base url for template (html file) locations
		'imageBaseURL' : settings.MEDIA_URL # base for images
		}
	return page_now(request, p2Form, allpms, allLocs)

def p2_old(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	this_page = "p2"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "fHxOvarianCA" in request.session:
		form = p2Form({'fHxOvarianCA': request.session['fHxOvarianCA']}) # set previous value
	else:
		form = p2Form() # no initial data
	
	if 'refresh_count' not in request.session:
		request.session['refresh_count'] = 0
			
	if request.method == 'POST':
		form = p2Form(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["fHxOvarianCA"] = form.cleaned_data['fHxOvarianCA']
			if form.cleaned_data['fHxOvarianCA'] == 'Yes': # answered yes, so record risk
				request.session["highRiskExit_p2"] = True # Take the high risk exit screen, whenever executed
				if quickExit:	# quick exit at first risk
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk') # quick exit screen url
			else:
				request.session["highRiskExit_p2"] = False # No referral required

			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p3') # next screen url
	diagMess = ""
	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p2.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to, 'diagMess' : diagMess})

def calculate_ptAge_now( bd):
	now = datetime.now()
#	age = relativedelta(now, bd)
	age = 0
	return age

def termination_page(request, fmess, othermess):
	if request.method == 'POST':
		request.session.flush()
		return render(request, 'screener/Termination_page.html', {'fmess' : "Session data flushed"})
	return render(request, 'screener/Termination_page.html', {'fmess' : fmess, 'othermess' : othermess})

def p3(request): # Pt history of breast cancer

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/') # start over
	
	if 'specialDebugOutput' in request.session:
		specialDebugOutput = request.session["specialDebugOutput"]
	else:
		specialDebugOutput = False

	this_page = "p3"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "pHxBreastCA" in request.session:
		form = p3Form({'pHxBreastCA': request.session['pHxBreastCA']}) # set previous value
	else:
		form = p3Form() # no initial data
	
	if specialDebugOutput:
		fpage = open('debugInfo.txt','a')
		fpage.write("P3: starting \n")
		fout = "P3: current page %s, back to %s\n" %(this_page, back_to)
		fpage.write(fout)
		fout = "P3: quickExit mode value: %s\n" %quickExit
		fpage.write(fout)

	if request.method == 'POST':
		form = p3Form(request.POST)
		if specialDebugOutput:
			fpage.write("P3: POST, starting\n")
		if	form.is_valid():
			if specialDebugOutput:
				fpage.write("P3: POST, valid form\n")
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["pHxBreastCA"] = form.cleaned_data['pHxBreastCA']
			if specialDebugOutput:
				fpage.write("P3: item.html_name: %s, type: %s\n" % ("pHxBreastCA", type(request.session["pHxBreastCA"])))
			if	request.session["pHxBreastCA"] == 'Yes': # answered yes to breast cancer
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p3a') # next screen url
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4') # next screen url
		else:
			if specialDebugOutput:
				fpage.write("P3: POST, invalid form\n")

	if specialDebugOutput:
		fpage.write("P3: EXITING\n")
	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p3.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to, 'diagMess' : ''})

def p3a(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	this_page = "p3a"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "pHxBrCALE50Years" in request.session: # assume all items are available (or none) *** Check this
		form = p3aForm({'pHxBrCALE50Years': request.session['pHxBrCALE50Years'],
				'pHxBrCA3Neg': request.session['pHxBrCA3Neg'],
				'pHxBrCAGT1PrimarySame': request.session['pHxBrCAGT1PrimarySame'],
				'pHxBrCAGT1PrimaryBoth': request.session['pHxBrCAGT1PrimaryBoth'],
				'pHxBrCADermMan': request.session['pHxBrCADermMan'],
			}) # set previous values
	else:
		form = p3aForm() # no initial data

	if request.method == 'POST':
		form = p3aForm(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			highRiskExit = False # test for any "yes" to the following risk factors
			request.session["pHxBrCALE50Years"] = form.cleaned_data['pHxBrCALE50Years']
			if form.cleaned_data['pHxBrCALE50Years'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCA3Neg"] = form.cleaned_data['pHxBrCA3Neg']
			if form.cleaned_data['pHxBrCA3Neg'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCAGT1PrimarySame"] = form.cleaned_data['pHxBrCAGT1PrimarySame']
			if form.cleaned_data['pHxBrCAGT1PrimarySame'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCAGT1PrimaryBoth"] = form.cleaned_data['pHxBrCAGT1PrimaryBoth']
			if form.cleaned_data['pHxBrCAGT1PrimaryBoth'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCADermMan"] = form.cleaned_data['pHxBrCADermMan']
			if form.cleaned_data['pHxBrCADermMan'] == "Yes":
				highRiskExit = True

			if highRiskExit: # Take the high risk exit screen, whenever executed
				request.session["highRiskExit_p3a"] = True
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
			else:
				request.session["highRiskExit_p3a"] = False # No referral required
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p3b') # next screen url

	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p3a.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})

def p3b(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	this_page = "p3b"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "ashkenaziJewish" in request.session: # assume all items are available (or none) *** Check this
		form = p3bForm({'ashkenaziJewish': request.session['ashkenaziJewish'],
				'pHxBrCAGE1RelBrCALE50Years': request.session['pHxBrCAGE1RelBrCALE50Years'],
				'pHxBrCAGE2RelBrPancCA': request.session['pHxBrCAGE2RelBrPancCA'],
			}) # set previous values
	else:
		form = p3bForm() # no initial data
	
	if request.method == 'POST':
		form = p3bForm(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.

			# accumulate risks from this page
			highRiskExit = False # test for any "yes" to the following risk factors
			request.session["ashkenaziJewish"] = form.cleaned_data['ashkenaziJewish']
			if form.cleaned_data['ashkenaziJewish'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCAGE1RelBrCALE50Years"] = form.cleaned_data['pHxBrCAGE1RelBrCALE50Years']
			if form.cleaned_data['pHxBrCAGE1RelBrCALE50Years'] == "Yes":
				highRiskExit = True
			request.session["pHxBrCAGE2RelBrPancCA"] = form.cleaned_data['pHxBrCAGE2RelBrPancCA']
			if form.cleaned_data['pHxBrCAGE2RelBrPancCA'] == "Yes":
				highRiskExit = True

			if highRiskExit: # Take the high risk exit screen, whenever executed
				request.session["highRiskExit_p3b"] = True # referral required
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk') # quick exit screen url
			else:
				request.session["highRiskExit_p3b"] = False # No referral required
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p3c') # next screen url
	
	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p3b.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})

def p3c(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	this_page = "p3c"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page
	
	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# define tags
	highRisk_thispage = "highRiskExit_" + this_page # tag indicating high risk registered on this page
	notab_thispage = "none_of_the_above_"+this_page # tag indicating aggregate "yes" or "no"
	
	if notab_thispage in request.session: # user has selected "yes" or "no" to aggregate option, so not firstPass
		firstPass = False
	else:
		firstPass = True

	form = p3cForm() # define main form
	agForm = p3c_Agg_queryForm() # Define "some of the above"
	
	if 'specialDebugOutput' in request.session:
		specialDebugOutput = request.session["specialDebugOutput"]
	else:
		specialDebugOutput = False

	if specialDebugOutput:
		fpage = open('debugInfo.txt','a')
		fout = "P3c: current page %s, back to %s\n" %(this_page, back_to)
		fpage.write(fout)
		fout = "P3c: quickExit mode value: %s\n" %quickExit
		fpage.write(fout)

	if request.method == 'POST':
		if firstPass:
			agForm = p3c_Agg_queryForm(request.POST)
			if agForm.is_valid():
				# Special handling for "none of the above" option
				request.session[notab_thispage] = agForm.cleaned_data['none_of_the_above']			
				if request.session[notab_thispage] == "No": # no cancers, no referral required
					for item in form: # set each item "No" in session data and in form data
						request.session[item.html_name] = "No"
					# continue to next page after pt views selection
					request.session[highRisk_thispage] = False # No referral required
					# continue to collect history
					request.session["last_url"].append(this_page) # records this url visited.
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # next screen url, all "no"
				else:
					firstPass = False # continue to detailed selection of items
		else: # collect checkbox for the detailed list
			form = p3cForm(request.POST)		
			if form.is_valid():
				highRiskExit = False # test for any "yes" to the following risk factors
				for item in form: # move the form data to session data
					cleanedData = form.cleaned_data[item.html_name]
					if cleanedData:
						cleanedData = "Yes"
						if specialDebugOutput:
							fpage.write("P3c: item.html_name: %s, type: %s, value %s\n" % (item.html_name, type(cleanedData), cleanedData))
						highRiskExit = True
					else:
						cleanedData = "No"
					request.session[item.html_name] = cleanedData

				if highRiskExit: # Take the high risk exit screen, whenever executed
					request.session[highRisk_thispage] = True # referral required
					if quickExit: # exit questionnaire now
						request.session["last_url"].append(this_page) # records this url visited.
						return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					request.session[highRisk_thispage] = False # No referral required
					# otherwise continue to collect history
				request.session["last_url"].append(this_page) # records this url visited.
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # next screen url, all "no"


	# fill fields with previously entered data from this session
	if "pHxBrCAThyroidCA" in request.session: # assume all items are available
		# now, populate the form
		form_kwkv = []
		for item in form:
			if request.session[item.html_name] == "Yes":
				form_kwkv.append([item.html_name, True])
			else:
				form_kwkv.append([item.html_name, False])
		form_dict =dict(form_kwkv)
		form = p3cForm(form_dict) # populate with values
	request.session["this_page"] = this_page # for return from explanation urls in template
	return render(request, 'screener/p3c.html', {'form': form, 'agForm' : agForm, 'firstPass' : firstPass, 'imageloc' : settings.MEDIA_URL,
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})	

def p4(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	this_page = "p4"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "recognizedRiskGroup" in request.session: # assume all items are available (or none) *** Check this
		form = p4Form({'recognizedRiskGroup': request.session['recognizedRiskGroup'],
				'fHxBrCASuscGene': request.session['fHxBrCASuscGene'],
				'fHxBreastCA': request.session['fHxBreastCA'],
			}) # set previous values
	else:
		form = p4Form() # no start data
		
	# "Next page" logic using transition matrix
	next_page = {
		"YesYesYes" : "p4a",
		"YesYesNo" : "p5",
		"YesNoYes" : "p4a",
		"YesNoNo" : "p5",
		"NoYesYes" : "p4a",
		"NoYesNo" : "p5",
		"NoNoYes" : "p4a",
		"NoNoNo" : "p5"}
		
	next_page_quickExit = {
		"YesYesYes" : "aboveAverageRisk",
		"YesYesNo" : "aboveAverageRisk",
		"YesNoYes" : "aboveAverageRisk",
		"YesNoNo" : "p5",
		"NoYesYes" : "aboveAverageRisk",
		"NoYesNo" : "aboveAverageRisk",
		"NoNoYes" : "p4a",
		"NoNoNo" : "p5"}

	
	if request.method == 'POST':
		form = p4Form(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			a=request.session["recognizedRiskGroup"] = form.cleaned_data['recognizedRiskGroup']
			b=request.session["fHxBrCASuscGene"] = form.cleaned_data['fHxBrCASuscGene']
			c=request.session["fHxBreastCA"] = form.cleaned_data['fHxBreastCA']

			if ( any( [a=="Yes", b=="Yes", c=="Yes"])):
				request.session["highRiskExit_p4"] = True # referral required
			else:
				request.session["highRiskExit_p4"] = False # referral NOT required

			# Gather more information

			if ( a=="Yes" and b=="Yes" and c=="Yes"):
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4a') # Gather more info
			elif ( a=="Yes" and b=="Yes" and c=="No"):
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # females > 45
			elif ( a=="Yes" and b=="No" and c=="Yes"):
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4a') # Gather more info
			elif ( a=="Yes" and b=="No" and c=="No"):
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # females > 45
			elif ( a=="No" and b=="Yes" and c=="Yes"):
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4a') # Gather more info
			elif ( a=="No" and b=="Yes" and c=="No"):
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # females > 45
			elif ( a=="No" and b=="No" and c=="Yes"):
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4a') # Gather more info
			elif ( a=="No" and b=="No" and c=="No"):
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # All "no", females > 45

	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p4.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to, 'diagMess' : ''})	

def p4a(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	this_page = "p4a"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	# fill fields with previously entered data from this session
	if "fHxBrCAMale" in request.session: # assume all items are available
		form = p4aForm({'fHxBrCAMale': request.session['fHxBrCAMale'],
				'fHxBrCASameSideGE2': request.session['fHxBrCASameSideGE2'],
			}) # set previous values
	else:
		form = p4aForm() # no initial data

	if request.method == 'POST':
		form = p4aForm(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["fHxBrCAMale"] = form.cleaned_data['fHxBrCAMale']
			request.session["fHxBrCASameSideGE2"] = form.cleaned_data['fHxBrCASameSideGE2']
			highRiskExit = False # test for any "yes" to the following risk factors
			if form.cleaned_data['fHxBrCAMale'] == "Yes":
				highRiskExit = True
			if form.cleaned_data['fHxBrCASameSideGE2'] == "Yes":
				highRiskExit = True

			if highRiskExit: # Take the high risk exit screen, whenever executed
				request.session["highRiskExit_p4a"] = True # referral required
				if quickExit:
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
			else:
				request.session["highRiskExit_p4a"] = False # No referral required
			# otherwise continue to collect history
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p4b') # next screen url, all "no"

	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p4a.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})	

def p4b(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	this_page = "p4b"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	if "quickExit" in request.session: # if not set then assume False
		quickExit = request.session["quickExit"]	# true or false for Quick Exit logic
	else:
		quickExit = False

	highRisk_thispage = "highRiskExit_" + this_page # tag indicating high risk registered on this page
	notab_thispage = "none_of_the_above_"+this_page # tag indicating aggregate "yes" or "no"
	if notab_thispage in request.session: # user has selected "yes" or "no" to aggregate option, so not firstPass
		firstPass = False
	else:
		firstPass = True

	form = p4bForm() # define main form
	agForm = p4b_Agg_queryForm() # Define "some of the above"

	if request.method == 'POST':
		if firstPass:
			agForm = p4b_Agg_queryForm(request.POST)
			if agForm.is_valid():
				# Special handling for "none of the above" option
				request.session[notab_thispage] = agForm.cleaned_data['none_of_the_above']			
				if request.session[notab_thispage] == "No": # no cancers, no referral required
					for item in form: # set each item "No" in session data and in form data
						request.session[item.html_name] = "No"
					# continue to next page after pt views selection
					request.session[highRisk_thispage] = False # No referral required
					# continue to collect history
					request.session["last_url"].append(this_page) # records this url visited.
					return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # next screen url, all "no"
				else:
					firstPass = False # continue to detailed selection of items
		else: # collect checkbox for the detailed list
			form = p4bForm(request.POST)		
			if form.is_valid():
				highRiskExit = False # test for any "yes" to the following risk factors
				for item in form: # move the form data to session data
					if form.cleaned_data[item.html_name]:
						request.session[item.html_name] = "Yes"
						highRiskExit = True
					else:
						request.session[item.html_name] = "No"

				if highRiskExit: # Take the high risk exit screen, whenever executed
					request.session[highRisk_thispage] = True # referral required
					if quickExit: # exit questionnaire now
						request.session["last_url"].append(this_page) # records this url visited.
						return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
				else:
					request.session[highRisk_thispage] = False # No referral required
					# otherwise continue to collect history
				request.session["last_url"].append(this_page) # records this url visited.
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/p5') # next screen url, all "no"

	# fill fields with previously entered data from this session
	if "fHxBrCADermMan" in request.session: # assume all items are available
		# now, populate the form
		form_kwkv = []
		for item in form:
			if request.session[item.html_name] == "Yes":
				form_kwkv.append([item.html_name, True])
			else:
				form_kwkv.append([item.html_name, False])
		form_dict =dict(form_kwkv)
		form = p4bForm(form_dict) # populate with values
	request.session["this_page"] = this_page # for return from explanation urls in template
	return render(request, 'screener/p4b.html', {'form': form, 'agForm' : agForm, 'firstPass' : firstPass, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})	

def p5(request):

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	this_page = "p5"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	# fill fields with previously entered data from this session
	if "fHxSufficient" in request.session: # assume all items are available (or none) *** Check this
		form = p5Form({'fHxSufficient': request.session['fHxSufficient'],
			}) # set previous values
	else:
		form = p5Form() # no initial data

	if request.method == 'POST':
		form = p5Form(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["fHxSufficient"] = form.cleaned_data['fHxSufficient']
			if CheckPtReferral(request):
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/aboveAverageRisk')
			if request.session["fHxSufficient"] == "Yes":
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/AverageRisk') # Average risk
			else:
				return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/IndetermRisk') # Indeterminate risk

	request.session["this_page"] = this_page # for explanations urls
	return render(request, 'screener/p5.html', {'form': form, 'imageloc' : settings.MEDIA_URL, 
		'urlprefix' : settings.WSGI_URL_PREFIX, 'back_to' : back_to})	

def CheckPtReferral(request):
	# go through visited pages stack, then construct high risk flag ****
	refer = False
	# Session values may not exist
	if "highRiskExit_p1" in request.session:
		if request.session["highRiskExit_p1"]:
			refer = True
	if "highRiskExit_p2" in request.session:
		if request.session["highRiskExit_p2"]:
			refer = True
	if "highRiskExit_p3" in request.session:
		if request.session["highRiskExit_p3"]:
			refer = True
	if "highRiskExit_p3a" in request.session:
		if request.session["highRiskExit_p3a"]:
			refer = True
	if "highRiskExit_p3b" in request.session:
		if request.session["highRiskExit_p3b"]:
			refer = True
	if "highRiskExit_p3c" in request.session:
		if request.session["highRiskExit_p3c"]:
			refer = True
	if "highRiskExit_p4" in request.session:
		if request.session["highRiskExit_p4"]:
			refer = True
	if "highRiskExit_p4a" in request.session:
		if request.session["highRiskExit_p4a"]:
			refer = True
	if "highRiskExit_p4b" in request.session:
		if request.session["highRiskExit_p4b"]:
			refer = True
	return refer

def aboveAverageRisk(request): # Quick exit, high risk, get pt phone, query for callback

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/') # splash page

	# must have the following data
	if "patientName" in request.session:
		patientName = request.session['patientName'].title() # capitalize each word
		request.session['patientName'] = patientName # save capitalized form
	else: # if no patient name, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "birthDate" in request.session:
		birthDate = request.session['birthDate']
	else: # if no patient bd, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
	
	this_page = "aboveAverageRisk"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	# restore data to page, if any
	if "patientCallbackNumber" in request.session:
		form = aboveAverageRiskForm({'patientCallbackNumber': request.session['patientCallbackNumber'],
			'callbackReq': request.session['callbackReq']
			}) # set previous value
	else:
		form = aboveAverageRiskForm()

	if request.method == 'POST':
		form = aboveAverageRiskForm(request.POST)
		if form.is_valid():
			request.session["patientCallbackNumber"] = form.cleaned_data['patientCallbackNumber']
			request.session["callbackReq"] = form.cleaned_data['callbackReq']
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["referralDecision"] = "Refer" # This is the high risk page
			savePtResponse(request) # save data to database
			if 'ptEmail' in request.session:
				ptEmail = request.session['ptEmail']
			else:
				ptEmail = ""
			# create the summary page with additional pt filled out on the page.
			pt_currentAge = calculate_ptAge_now( birthDate)
			now = datetime.now()
			risk_list = RiskListToText(request) # convert risk list keywords to text
			siteInfo =  nonPtInfo.objects.get(id=1) # get the first and only record
			projectAbbrev = siteInfo.projectAbbrev
			projectContactPhone = siteInfo.projectContactPhone
			summaryPagehtml = render(request, 'screener/rAboveAvgRisk.html', {'form': form,'patientName' : patientName, 'birthDate' : birthDate,
				'pt_currentAge': pt_currentAge, 'current_date' : now, 'urlprefix' : settings.WSGI_URL_PREFIX, 
				'back_to' : back_to, 'projectAbbrev' : projectAbbrev, 'projectContactPhone' : projectContactPhone, 
				'risk_list': risk_list, 'diagMess' : '', 
				'patientCallbackNumber' : request.session["patientCallbackNumber"],
				'callbackReq' : request.session["callbackReq"],
				'patientCallbackNumber' : request.session["patientCallbackNumber"],
				'ptEmail' : ptEmail})
			request.session["summaryPagehtml"]=summaryPagehtml # save the html for possible email
			# Completion page is next
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/Completion')

	pt_currentAge = calculate_ptAge_now( birthDate)
	now = datetime.now()
	risk_list = RiskListToText(request) # convert risk list keywords to text
	siteInfo =  nonPtInfo.objects.get(id=1) # get the first and only record
	projectAbbrev = siteInfo.projectAbbrev
	projectContactPhone = siteInfo.projectContactPhone
	summaryPagehtml = render(request, 'screener/rAboveAvgRisk.html', {'form': form,'patientName' : patientName, 'birthDate' : birthDate,
		'pt_currentAge': pt_currentAge, 'current_date' : now, 'urlprefix' : settings.WSGI_URL_PREFIX, 
		'back_to' : back_to, 'projectAbbrev' : projectAbbrev, 'projectContactPhone' : projectContactPhone, 
		'risk_list': risk_list, 'diagMess' : ''})
	return summaryPagehtml


def AverageRisk(request): # Quick exit, high risk, get pt phone, query for callback

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/') # splash page

	# must have the following data
	if "patientName" in request.session:
		patientName = request.session['patientName'].title() # capitalize each word
		request.session['patientName'] = patientName # save capitalized form
	else: # if no patient name, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "birthDate" in request.session:
		birthDate = request.session['birthDate']
	else: # if no patient bd, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	this_page = "AverageRisk"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	# restore data to page, if any
	form = AverageRiskForm()

	if request.method == 'POST':
		form = AverageRiskForm(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["referralDecision"] = "NOReferral"
			savePtResponse(request) # save data to database
			# Completion page is next
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/Completion')
	now = datetime.now()
	pt_currentAge = calculate_ptAge_now( birthDate)
	
	risk_list = RiskListToText(request) # convert risk list keywords to text
	summaryPagehtml = render(request, 'screener/rAvgRisk.html', {'form': form,'patientName' : patientName, 'birthDate' : birthDate, 
		'pt_currentAge': pt_currentAge, 'current_date' : now, 'urlprefix' : settings.WSGI_URL_PREFIX, 
		'back_to' : back_to, "risk_list" : risk_list})
	request.session["summaryPagehtml"]=summaryPagehtml # save the html for possible email
	return summaryPagehtml

def IndetermRisk(request): # Quick exit, high risk, get pt phone, query for callback

	if not request.session.test_cookie_worked(): # check for cookie function and therefore session existence
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
		
	if "last_url" not in request.session: # if no previous url, then dropped in to page from outside
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/') # splash page

	# must have the following data
	if "patientName" in request.session:
		patientName = request.session['patientName'].title() # capitalize each word
		request.session['patientName'] = patientName # save capitalized form
	else: # if no patient name, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')

	if "birthDate" in request.session:
		birthDate = request.session['birthDate']
	else: # if no patient bd, return to splash screen
		return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/')
	
	this_page = "IndetermRisk"
	if request.session["last_url"][-1] == this_page:
		request.session["last_url"].pop()	# assume the previous page is different from this page
		request.session.modified = True	# save the session changes
	back_to = request.session["last_url"][-1]	# end of stack is previous page

	# restore data to page, if any
	form = IndetermRiskForm()

	if request.method == 'POST':
		form = IndetermRiskForm(request.POST)
		if form.is_valid():
			request.session["last_url"].append(this_page) # records this url visited.
			request.session["referralDecision"] = "Indeterminate"
			savePtResponse(request) # save data to database
			# Completion page is next
			return HttpResponseRedirect(settings.WSGI_URL_PREFIX + 'scrn/Completion')

	now = datetime.now()
	pt_currentAge = calculate_ptAge_now( birthDate)

	risk_list = RiskListToText(request) # convert risk list keywords to text
	
	if request.session["fHxSufficient"] == "No":
		indetermList = ["No risk history for female blood relatives over the age of 45."]
	else:
		indetermList = []
	
	siteInfo =  nonPtInfo.objects.get(id=1) # get the first and only record
	projectAbbrev = siteInfo.projectAbbrev
	projectContactPhone = siteInfo.projectContactPhone
	summaryPagehtml = render(request, 'screener/rIndetermRisk.html', {'form': form,'patientName' : patientName, 'birthDate' : birthDate, 
		'pt_currentAge': pt_currentAge, 'current_date' : now, 'urlprefix' : settings.WSGI_URL_PREFIX, 
		'back_to' : back_to, 'projectAbbrev' : projectAbbrev, 'projectContactPhone' : projectContactPhone, 
		"indetermList" : indetermList, "risk_list" : risk_list})
	request.session["summaryPagehtml"]=summaryPagehtml # save the html for possible email
	return summaryPagehtml

from django.core.mail import send_mail, EmailMessage

def Completion(request):
	
	current_date = str(datetime.now()) # to be printed only - no arithmetic
	if "splash_url" in request.session: # Define the starting page - preserve the quick exit option if it exists.
		startQURL = settings.WSGI_URL_PREFIX + 'scrn/' + request.session["splash_url"]
	else:
		startQURL = settings.WSGI_URL_PREFIX + 'scrn/' # Assume not quick exit
		
	if "ptEmail" in request.session:
		ptEmail = request.session["ptEmail"]
	else:
		ptEmail = ""
	
	sentMail = ""
	if request.method == 'POST':
		emailSubj = 'screener results for %s' % current_date[:16]
		siteInfo =  nonPtInfo.objects.get(id=1) # get the first and only record
		questionnaireEmail = siteInfo.questionnaireEmail # email "from" this address
		if 'summaryPagehtml' in request.session: # send risk page with html
			html_content = "%s" % request.session["summaryPagehtml"]
			msg = EmailMessage(emailSubj, html_content, questionnaireEmail, [ptEmail])
			msg.content_subtype = "html"  # Main content is now text/html
			sentMail = "Email has been sent to: " + ptEmail
		else:
			adminEmail = settings.DEFAULT_FROM_EMAIL # send error message back to screener
			emailBody = 'Error message to '+adminEmail +'\n Error, no summary data %s' % current_date
			msg = EmailMessage(emailSubj, emailBody, questionnaireEmail, [adminEmail])
			sentMail = 'Admin has been informed of an error: ' + adminEmail
		msg.send()
 		

	return render(request, 'screener/Completion.html', { 'urlprefix' : settings.WSGI_URL_PREFIX
		, 'startQURL' : startQURL, 'ptEmail' : ptEmail, 'current_date' : current_date
		, 'sentMail' : 	sentMail})


def back_to_Logic( request, this_page ): # not used #****
	if len(request.session["last_url"]) > 1: # detect immediate duplicates
		if request.session["last_url"][-1] == this_page:
			request.session["last_url"].pop()	# assume the previous page is different from this page
			request.session.modified = True	# save the session changes
		back_to = request.session["last_url"][-1]	# end of stack is previous page
	else:
		back_to = ""
		request.session["last_url"] = [back_to]
	return request.session["last_url"][-1]	# end of stack is previous page
	
def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))
