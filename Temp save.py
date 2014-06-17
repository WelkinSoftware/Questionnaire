tableName = 'Page'
fileName = 'test dump/%s.txt' %tableName
fileOut = codecs.open(fileName,'w', encoding='utf-8')
ap=Page.objects.get(id=598)
theText=ap.explanation
theText = repTChar(theText)
fileOut.write(theText+os.linesep)






.latest('lastUpdate')
xx = [
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

theCols = [ yCol for yCol in xx]
theRows = [ [ yCol[ii] for yCol in xx] for ii in range(9)]


import numpy
initStart = [
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
initStartArray = numpy.array(initStart)
initStartTrans = map(list,zip(*initStart))

tableDisplay=numpy.array(initStart).reshape(3,3,3,3).tolist()

d=[]
iNum=map(str,range(81))
ii = 0
for iRow in range(3):
	c=[]
	for iCol in range(3):
		b = []
		for iRow2 in range(3):
			a = []
			for iCol2 in range(3):
				a.append(str(iNum[ii]))
				ii+=1
			b.append(a)
		c.append(b)
	d.append(c)

for aItem in d:
	for bItem in aItem:
		for cItem in bItem:
			for dItem in cItem:
				print dItem

********************************************************** Save for a brief while
from base_page_incusion.html
	ul li {
		background-image:url(sqpurple.gif);
		background-repeat:no-repeat;
		background-position:0px 5px; 
		padding-left:14px;
	}


	# was function getNextPageFromGlobalFlags
	DebugOut('getNextPageFromGlobalFlags: enter')
	pageTransitionPresent = True # optimism
	DebugOut('Questionnaire: %s, page: %s, testCondition: %s' %(theQuestionnaire.shortTag,pageTag,testCondition))
	try: # try to find the records for the page which lists global flags
		pageAnalObjs = PageAnalysis.objects.filter(
			questionnaireID = theQuestionnaire,
			pageID__shortTag = pageTag,
			)
	except PageAnalysis.DoesNotExist:
		Debug("Retrieval from PageAnalysis failed, and that's ok")
		# no global flags apply to this page
		pageTransitionPresent = False
		next_page = ''
		return [next_page, pageTransitionPresent] # exit here. Nothing more to do
	# successful, so get the flags
	# make a list of flags to check.
	flagList = []
	for item in pageAnalObjs:
		flagList.append(item.testResultFlag)
	
	# bleed1 redo above. Use only QuestionnairePage, if global flag exists for this page, then next page.
	
	# for each flag, determine if there is a page transition defined for this page
	recordType = 'globalFlag'
	nextPageList = [] # last page set wins the game.
	pageTransitionPresent = False # reuse from above
	for aFlag in flagList:
		try:
			next_pageGlobal = QuestionnairePage.objects.get(
				questionnaireID = theQuestionnaire,
				pageID__shortTag=pageTag,
				testCondition=aFlag,
				recordType = recordType,
				).nextPage
			next_pageGlobal = qp.nextPage
			nextPageList.append(next_pageGlobal)
			if not pageTransitionPresent: # triggers once
				pageTransitionPresent = True
		except QuestionnairePage.DoesNotExist:
			next_page = ''
	if nextPageList != [] and pageTransitionPresent: # had at least one flag match
		next_page = nextPageList[-1]
	else:
		next_page = ''
********************************************************** Save for a brief while



recordType = 'calculated'
questionnaireObj = Questionnaire.objects.get(shortTag='BRCA')
pageObj = Page.objects.get(shortTag = 'P3')

qp = QuestionnairePage.objects.filter(
	pageID = pageObj
	).filter(
	questionnaireID = questionnaireObj
	).filter(
	recordType = recordType
	)
testConditionTransitionDict = {}
for item in qp:
	testConditionTransitionDict.update({qp.testCondition : qp.pageID.shortTag})
	
#

Here are other ways you can learn more:<br />
1. You may ask your physician for our handout.<br />
2. We suggest these websites:
<ul>
<li>National Institutes of Health: <a href="http://health.nih.gov">http://health.nih.gov</a></li>
<li>Susan Komen Foundation: <a href="http://ww5.komen.org/">http://ww5.komen.org</a></li>
<li>National Comprehensive Cancer Network: <a href="http://www.nccn.org">http://www.nccn.org</a></li>
<li>PAMF: <a href="http://www.pamf.org/">http://www.pamf.org/</a></li>
</ul>


<p>
1. Your chances of carrying a BRCA mutation are <b>very low</b>.
</p>
<p>
2. Your chances of developing breast or ovarian cancer are <b>average, not increased</b>. 
 "Average" risk means about 1 in 10 chance of getting breast cancer and about 1 in 100 chance of getting ovarian cancer.
</p>





	if ptlText: # not null
		ptlListOut = ptlText.split(os.linesep) # splits at the end of line
		# now split each csv line a the comma, eliminating blanks.
		ptlListInput = []
		for aLine in ptlListOut:
			ptlListInput.append(aLine.replace(" ","").split(',').strip()) # get rid of whitespace
		localInput['ptl'] = pickle.dumps(ptlListInput) # pickle the list of lists





ptlListOut = ptlText.split(os.linesep) # splits at the end of line
# now split each csv line
ptlListInput = []
for aLine in ptlListOut:
	ptlListInput.append(aLine.replace(" ","").split(','))

ptlListInput

ptlListInput == ptlList

ptlText = ''
ii = 1 # count lines. Must be a better way to do this ***
# don't want a '\n' at the end of the string
for aline in ptlList:
	ptlText = ptlText + ', '.join(aline)
	if ii != len(ptlList):
		ptlText = ptlText + '\n'
	ii += 1

print(ptlText)

ptlText = ',<br>'.join(ptlList)


Before determing multichoice
found a single choice for tag: ashkenaziJewish
Single choice appended to the list
at the top of the questions on the page loop

Tope of page loop
processing page: P3b
Number of questions found: 3
at the top of the questions on the page loop

at the top of the questions on the page loop
after aQuest
after qtag: pHxBrCABrainTumors
after atext
Before determing multichoice
found a single choice for tag: pHxBrCABrainTumors
Single choice appended to the list
at the top of the questions on the page loop



quaire = Questionnaire.objects.get(shortTag='BRCA')
now = timezone.now()
[pageList, fieldList, theList, tagToText ] = ListQuestionsForQuestionnaire(quaire)
allSubmit = Submission.objects.all()
theSubmit = allSubmit[0]
aPageTag = theList[2][0]
qQuestionTag = theList[2][1]
pageObj = Page.objects.get(shortTag=aPageTag)
theQuestionObj = Question.objects.get(questionTag = qQuestionTag)
aResp = Response.objects.create(
	questionID = theQuestionObj,
	pageID = pageObj,
	submissionID = theSubmit,
	lastUpdated = now,
	)
aValue = 'dire straits'
aRSObj = ResponseSelection.objects.create(  # This line will create duplicates!
	responseID = aResp,
	responseText = aValue,
	responseType = 'CharField',
	)


pageToPageMap=QuestionnairePage.objects.filter(questionnaireID__shortTag=workingQuestionnaireTag
	).filter(testCondition='next_page_default')

for aptlLine in ptlLines:
	addP2P(theQuesionnaireShortTag, aptlLine)

quit()
python manage.py shell
from multiquest.adminUtilities import *
#Execute
dumpQuestionnaire()

Questionnaire.objects.all().delete() # delete if found
theQuesionnaireShortTag= 'BRCA'
pageTopageDefault =[
	['splash','respondentIdent','H1','H2','H3','H3a','H3b','H4','H5','H5a','H6','H7','H7a','P1','P2','P3','P4','P5','questionnaireSummary','completion'],
	['P3a','P3b','P3c','P5'],
	['P4a','P4b','P5'],
	['avgRisk','completion'],
	['indetRisk','completion'],
	['riskAssess2','completion'],
	]
#pathsToChar=pickle.dumps(pageTopageDefault) # pickle the list
pathsToChar=pageTopageDefault # Don't pickle the list
q1=Questionnaire(
	shortTag=theQuesionnaireShortTag,
	barTitle='PAMF breast health screening questionnaire',
	pageTitle='Breast Health Screening',
	pageSubTitle='(This is a prototype questionnaire: please disregard the results.)',
	description='BRCA gene risk assessment.',
	explanation='BRCA gene risk assessment.',
	footerText='PAMF breast and ovarian cancer genetic counseling screening questionnaire',
	version='BRCA version 1.6',
	versionDate=tupd,
	splashScreenTextPrologue="This questionnaire helps determine if you might benefit from discussion regarding breast and ovarian cancer. Certain tests and treatments may lower your chances of getting these cancers or their recurrence.",
	splashScreenTextP1="This questionnaire is based on national guidelines to screen for certain gene mutations that may increase risk of cancer. It is meant for women who have <i>not</i> already had genetic testing for BRCA1 and BRCA2 mutations. If you have already had such testing, you are done! Please return this device to the person who gave it to you.",
	splashScreenTextP2="Your answers will suggest whether your chances of having these gene mutations are low or are high enough to merit further discussion. If you aren't able to answer some of the questions now, you may want to collect that information and talk further with your doctor.",
	splashScreenTextP3="To start the questionnaire, please click the 'Next' box. To learn more about any words highlighted in blue, simply tap that term. To return to the previous screen, tap the back arrow.",
	firstPageTag = "splash",
	ptl = pathsToChar,
	)
q1.save()



	questionResponseList = []
	# bleeding edge
	for aline in theList:
		try:
			aField = aline[1]
			fieldPage = aline[0]
			fieldName = aline[2]
			rawFieldValue = allResults[aField] # check for KeyError here, since not all Q's are answered
			fieldValue = str(rawFieldValue)
			if type(rawFieldValue) == list:
				listLevel = 'main'
				theLine = [listLevel, fieldName,""] # null value since value is a set of keyword, not user-friendly
				questionResponseList.append(theLine)
				DebugOut(fieldPage+" "+fieldName+": "+fieldValue)
				for aValue in rawFieldValue:
					tagName = aValue # only the field name appears
					listLevel = 'sub'
					fieldValue = ""  # assume a null value
					try:
						fieldName = tagToText[tagName]
						theLine = [listLevel, fieldName,fieldValue] # assume a null value
					except KeyError:
						DebugOut('No name found for sub key: %s' %tagName)
						theLine = [listLevel, tagName,fieldValue] # assume a null value
					questionResponseList.append(theLine)
			else:# not a list, therefore a the main level
				listLevel = 'main'
				theLine = [listLevel, fieldName,fieldValue]
				questionResponseList.append(theLine)
				DebugOut(fieldPage+" "+fieldName+": "+fieldValue)
		except KeyError:
			DebugOut('No value for field: %s' %aField)
			pass # continue to next field




import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Hello, world!')
msg['Subject'] = 'This is an email title'
msg['From'] = 'screener@screengenes.org'
msg['To'] = 'clewis222@me.com'

s = smtplib.SMTP('localhost:8000')
s.sendmail(me, [you], msg.as_string())
s.quit()


for respField in respFields:
	try:
		aRow.append(unicode(getattr(responderObj, respField)).encode('utf-8'))
	except:
		pass

therespondentID = Respondent.objects.get(
	lastName = "L",
	middleName = "k",
	firstName = "R",
	birthDate = "1991-01-05",
	)
# update
therespondentID.ptEmail = "clewis222@me.com"
therespondentID.ptUniqueID = uniquePTID("R", "k", "L", "1991-01-05"),
therespondentID.save()

pageToPageMap=QuestionnairePage.objects.filter(questionnaireID__shortTag=workingQuestionnaireTag
).filter(testCondition='next_page_default')


lastName = 'cccc'
middleName = 'bbbb'
firstName = 'aaa'
birthDate = '1914-01-05'
ptEmail = 'test@xx.com'

def uniquePTID(firstName, middleName, lastName, birthDate):
	# construct a unique patient id
	patientName = firstName+' '+middleName+' '+lastName
	patientName = patientName.title() # capitalize each word to reduce variation
	uid = "%s %s" % (birthDate, patientName)
	return uid

therespondentID = Respondent.objects.create(
	lastName = lastName,
	middleName = middleName,
	firstName = firstName,
	birthDate = birthDate,
	ptEmail = ptEmail,
	contactPhone = '',
	contactEmail = '',
	externalID = '',
	externalIDAuthority = '',
	ptUniqueID = uniquePTID(firstName, middleName, lastName, birthDate),
	)



		thePageQuestionsAll=PageQuestion.objects.order_by('questionSequence').filter( pageID__shortTag=this_page)


PageQuestion.objects.order_by('questionSequence').filter( questionID__questionTag=)

from django.db.models import Q

ll=[['P3a', 'P3b', 'P3c', 'P5'], ['P4a', 'P4b', 'P5']]



pageToPage = {}
for item in thePageToPageMap:
	pageToPage.update({item.pageID.shortTag : item.nextPage})


qasStr=Questionnaire.objects.get(shortTag='BRCA').ptl
pageToPage = {u'P3a': u'P3b', u'respondentIdent': u'H1', u'H7a': u'P1', u'P4b': u'P5', u'P4a': u'P4b', u'splash': u'respondentIdent', u'P2': u'P3', u'P3': u'P4', u'P1': u'P2', u'P4': u'P5', u'P5': u'completion', u'H3b': u'H4', u'H3a': u'H3b', u'H5a': u'H6', u'H2': u'H3', u'H3': u'H3a', u'H1': u'H2', u'H6': u'H7', u'H7': u'H7a', u'H4': u'H5', u'H5': u'H5a', u'P3b': u'P3c', u'P3c': u'P5'}

'<i>This questionnaire first asks about <a title="Tap here for more information about ovarian cancer"href="{{explainURLprefix}}ovca">ovarian cancer</a>, because women with this condition have a higher chance of BRCA gene mutations.</i>'

		{% for fieldName in fNames %}
		<td>{{ item.fieldName }}</td>
		{% endfor %}
	
			return HttpResponse("form is valid. To next page: %s" %next_page)
	return HttpResponse("got here2: %s" %pageIdent)
	
try:
	thePage=Page.objects.get(pageTag='P1')
except Page.DoesNotExist:
	print("exception")

		barTitle='PAMF breast health screening questionnaire',
		pageTitle='Breast Health Screening',
		pageSubTitle='(This is a prototype questionnaire: please disregard the results.)',
		description='BRCA gene risk assessment.',
		footerText='PAMF breast and ovarian cancer genetic counseling screening questionnaire',
		version='BRCA version 1.6',
		versionDate='2013-9-12',
		splashScreenTextPrelog="This questionnaire helps determine if you might benefit from discussion regarding breast and ovarian cancer. Certain tests and treatments may lower your chances of getting these cancers or their recurrence.",
		splashScreenTextP1="This questionnaire is based on national guidelines to screen for certain gene mutations that may increase risk of cancer. It is meant for women who have <i>not</i> already had genetic testing for BRCA1 and BRCA2 mutations. If you have already had such testing, you are done! Please return this device to the person who gave it to you.",
		splashScreenTextP2="Your answers will suggest whether your chances of having these gene mutations are low or are high enough to merit further discussion. If you aren't able to answer some of the questions now, you may want to collect that information and talk further with your doctor.",
		splashScreenTextP3="To start the questionnaire, please click the 'Next' box. To learn more about any words highlighted in blue, simply tap that term. To return to the previous screen, tap the back arrow.",


	if 'constantPageDataDict' in request.session:
		constantPageDataDict = request.session['constantPageDataDict']
	else:
		return render(request, 'system_error.html', {'syserrmsg': "Debug:  header and footer page data is missing in scrnrexpln."})
	pageBaseURL = constantPageDataDict['pageBaseURL']
	
	if "last_url" in request.session:
		back_to = pageBaseURL + request.session["last_url"][-1]
	else:
		return render(request, 'system_error.html', {'syserrmsg': "Debug:  last_url is missing in scrnrexpln."})



# delete later
	# Retrieve two pages
	pg=Page.objects.get(shortTag='H1')
	pgNext=Page.objects.get(shortTag='H2').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H2')
	pgNext=Page.objects.get(shortTag='H3').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H3')
	pgNext=Page.objects.get(shortTag='H4').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H4')
	pgNext=Page.objects.get(shortTag='H5').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H5')
	pgNext=Page.objects.get(shortTag='H6').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H6')
	pgNext=Page.objects.get(shortTag='H7').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	pg=Page.objects.get(shortTag='H7')
	pgNext=Page.objects.get(shortTag='P1').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	# Retrieve two pages
	pg=Page.objects.get(shortTag='P1')
	pgNext=Page.objects.get(shortTag='P2').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	# Retrieve two pages
	pg=Page.objects.get(shortTag='P2')
	pgNext=Page.objects.get(shortTag='P3').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	# Retrieve two pages
	pg=Page.objects.get(shortTag='P3')
	pgNext=Page.objects.get(shortTag='P4').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()

	# Retrieve two pages
	pg=Page.objects.get(shortTag='P4')
	pgNext=Page.objects.get(shortTag='P5').shortTag
	pq=QuestionnairePage(questionnaireID=q1,
		pageID = pg,
		nextPage = pgNext,
		)
	pq.save()
