def savecsv(request, forProject=None):
	"""Dumps a csv-type file of all submissions.

	This is a one line or more descriptive summary.
	Blah Blah Blah.

	Args:
		argument_one: This is of some type a and does x.
		arg....:...

	Returns:
		http response 	

	Raises:
		none.
	"""
	DebugOut('savecsv: Enter')
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	now = str(timezone.now())
	outcsvFileName = "Questionnaire Responses %s.csv" %now[:16] # cut off time zone & seconds fraction
	contentDispo = 'attachment; filename=' + '"' + outcsvFileName + '"'
	response['Content-Disposition'] = contentDispo
	
	# dump the header text for respondent ID
	writer = csv.writer(response)
	
	# get all Submissions
	allSubmissions = Submission.objects.all().order_by('-lastUpdate')
	#DebugOut('allSubmissions')
	#DebugOut(allSubmissions)
	if len(allSubmissions) == 0:
		errMsg = 'Zero submissions available. No export submissions file created.'
		DebugOut(errMsg)
		return render(request, 'system_error.html', { 'syserrmsg': [errMsg]})
	# get all global flags for all submissions
	allGFlagRecs = SubmissionAnalysis.objects.all()
	for aRec in allGFlagRecs:
		DebugOut('aRec %s' %str(aRec))
	# Make a list of unique flags. May be null
	globalFlagNames = list(set([aFlagRec.testResultFlag for aFlagRec in allGFlagRecs]))
	globalFlagNames.sort()
	DebugOut('globalFlagNames %s' %globalFlagNames)
	if forProject:
		theProject = forProject
		allQuestionnaires = getAllQuestionnareObjForProject(theProject)
		if len(allQuestionnaires) == 0:
			allerrMsg = ['No Questionnaires available for this project: %s.'%theProject.shortTag]
			allerrMsg.append('No export submissions file created.')
			DebugOut(allerrMsg)
			return render(request, 'system_error.html', { 'syserrmsg': allerrMsg})
		allQIDs = [aq.id for aq in allQuestionnaires]
	DebugOut('allQIDs: %s'%str(allQIDs))
	colm_headers = [] # save the new header here
	oldHeaderCopy = [] # save the old header here
	DebugOut('Submissions loop')
	icountExports = 0 # count the exported submissions
	for aSubmission in allSubmissions:
		#DebugOut('Top of submissions loop')
		if forProject:
			# Check if submission points to a questionnaire owned by the project
			qid = aSubmission.questionnaireID.id
			if qid not in allQIDs: # is Questionnaire in the Project?
				DebugOut('Skipped submissions for Submission uniqueID: %s'%aSubmission.respondentID.ptUniqueID)
				DebugOut('Skipped submissions for Questionnaire: %s, record %s'%(aSubmission.questionnaireID.shortTag,aSubmission.questionnaireID.id))
				continue # skip this loop, to to top of submission loop
		aRow = [] # add respondent ID, questionnaire ID, question responses
		icountExports+=1
		# Dump the Submission record
		aRow.append(aSubmission.lastUpdate)
		colm_headers.append('lastUpdate')
		aRow.append(aSubmission.reviewedBy)
		colm_headers.append('reviewedBy')
		aRow.append(aSubmission.reviewDate)
		colm_headers.append('reviewDate')
		aRow.append(aSubmission.okForExport)
		colm_headers.append('okForExport')
		# dump questionnaire data
		# dump Respondent data
		responderObj = aSubmission.respondentID
		# Respondent fields
		respFields = ['lastName', 'middleName', 'firstName', 'birthDate', 'contactPhone', 'contactEmail', 'externalID', 'externalIDAuthority']
		for respField in respFields: # process respondent identifiction
			try:
				theItem = unicode(getattr(responderObj, respField)).encode('utf-8')
				aRow.append(theItem)
				#DebugOut('respField field: %s value: %s' %(respField,theItem))
				colm_headers.append(respField)
			except AttributeError:
				DebugOut('syserrmsg: respField field: %s not found in database.' %(respField))
			except:
				DebugOut('syserrmsg: respField field: %s error in db retrieval' %(respField))
		# process questionnaire name and version
		aquaireObj = aSubmission.questionnaireID
		# Project shortTag
		projectShortTag = getProjectObjForQuestionnaire(aquaireObj).shortTag
		aRow.append(projectShortTag)
		colm_headers.append('Project')
		# Questionnaire fields ************************** BEGIN
		aRow.append(aquaireObj.shortTag)
		colm_headers.append('Questionnaire')
		aRow.append(aquaireObj.version)
		colm_headers.append('version')
		aRow.append(aquaireObj.versionDate)
		colm_headers.append('versionDate')
		aRow.append(aquaireObj.language)
		colm_headers.append('language')
		# Questionnaire fields ************************** END
		# retrieve any global flags for this submission *** BEGIN
		# display only the highest priority flag
		# sort the flags so that the order is the same for different submissions
		theFlagInfo = SubmissionAnalysis.objects.order_by('testResultFlagPriority').filter(
			submissionID = aSubmission,
			)
		allFlagsThisSubmit = [aGlobalFlag.testResultFlag for aGlobalFlag in theFlagInfo]
		DebugOut('allFlagsThisSubmit: %s' %allFlagsThisSubmit)
		for aFlag in globalFlagNames:
			colm_headers.append(aFlag)
			if aFlag in allFlagsThisSubmit:
				aRow.append("Yes")
			else:
				aRow.append("No")
		# retrieve any global flags for this submission *** END

		#DebugOut('retrieve all questions')
		DebugOut('retrieve all questions for questionnaire %s' %aquaireObj.shortTag)
		# list all possible question fields in uniqueTagList
		[pageList, uniqueTagList, theList, tagToText ] = ListQuestionsForQuestionnaire(aquaireObj)
		#DebugOut('after ListQuestionsForQuestionnaire')
		responseDict = {}	# translate from tag to value for that tag.
							# problem, this is for the old non-unique tags
		# retrieve all questions, first the response records
		allResponses = Response.objects.filter(submissionID = aSubmission)
		for aResponse in allResponses: # *** loop on Response records, one question each
			theQuestionObj = aResponse.questionID
			responseChoiceObjs = ResponseChoice.objects.order_by('choiceSequence').filter(questionID=theQuestionObj)
			theQRecNum = theQuestionObj.id
			questionTag = theQuestionObj.questionTag
			allRespForQuestionObj = ResponseSelection.objects.filter(responseID=aResponse)
			# possible multiple responses per question
			numSels = len(allRespForQuestionObj)
			DebugOut('Number of allRespForQuestionObj (always "1"?) %s' %(numSels)) # always? "1"
			if numSels == 1: # keyword and keyvalue
				currentVal = allRespForQuestionObj[0].responseText # ResponseSelection record
				DebugOut('responseRaw (single): %s' %currentVal)
				theQLabel = encodeQuestionResponseLabel(theQRecNum,'')
				responseDict.update({theQLabel : currentVal})
				DebugOut('tag & value: %s, %s' %(theQLabel,currentVal))
			elif numSels > 1: # is a list of tags
				for aRespToQuestion in allRespForQuestionObj:
					uniqueChoiceLabel = aRespToQuestion.responseText # the value IS the tag  # ResponseSelection record
					[questionRecNum,responseChoiceRecNum] = decodeQuestionResponseLabel(uniqueChoiceLabel)
					theChoice = responseChoiceObjs.get(id=responseChoiceRecNum)
#					currentVal = theChoice.choiceText
					theChoiceRecNum = aRespToQuestion.id
					DebugOut('responseRaw (multiple): %s' %uniqueChoiceLabel)
					# translate tag to text
					# if can't find then deliver a uniqueChoiceLabel value for display. Why not null?
					currentVal = tagToText.get(uniqueChoiceLabel, uniqueChoiceLabel)
					responseDict.update({uniqueChoiceLabel : currentVal})
					theQLabel = encodeQuestionResponseLabel(theQRecNum,theChoiceRecNum)
					DebugOut('tag & value: %s, %s' %(uniqueChoiceLabel,currentVal))
			else:
				DebugOut('No value for question tag %s, therefore "None"' %questionTag)
				colHdEntry=questionTag
				responseDict.update({questionTag : 'None'})
				DebugOut('tag & value: %s, %s' %(colHdEntry,currentVal))
		DebugOut('Response dictionary is complete')
		DebugOut('Number of entries: %s' %len(responseDict))
		# responseDict is complete. Now use it to replace tags with values
#		Create list of values in the same order as column headers
		# replace with values in default order - not in acquisition order
		# append a count to the tag to make it unique
		fieldCount = 1
		colmWCount = []
		responseList = []
		#DebugOut('uniqueTagList: %s' %uniqueTagList) # start with a list of all fields
		for aTag in uniqueTagList:
			#DebugOut('Start of appending fields to a list')
			#DebugOut('processing a response %s' %str(aTag))
			#DebugOut('response converted to string')
			#DebugOut('question tag found: %s' %aTag)
			try:
				theQresponse = responseDict[str(aTag)] # replace keyword with response value
			except KeyError:
				theQresponse = '' # replace keyword with response value
				#DebugOut('question tag not found in responseDict: %s' %aTag)
			#DebugOut('question tag after tagToText1: %s' %theQresponse)
			responseList.append(theQresponse)
			#DebugOut('End of appending responses to a list')
			[questionRecNum,responseChoiceRecNum] = decodeQuestionResponseLabel(aTag)
			aTagForDisplay = str(aTag)
			aTagForDisplay = Question.objects.get(id=questionRecNum).questionTag
			colmWCount.append(aTagForDisplay+'_'+str(fieldCount))
			fieldCount+=1
			colm_headers.extend(colmWCount) # Make the column headers unique
			#DebugOut('End of appending column titles to a list')
		DebugOut('End of responses')
		
		if oldHeaderCopy != colm_headers:
			writer.writerow(colm_headers)
			oldHeaderCopy = list(colm_headers) # Save the new header if different
		colm_headers = list([]) # annihilate the current list			
			
		#DebugOut('responseList %s' %responseList)
		#DebugOut('responseDict: %s' %list(responseDict))
		aRow.extend(responseList)
		#DebugOut('Before writing a row')
		writer.writerow(aRow) # append the submission to the csv file
		DebugOut('After writing a row')
	DebugOut('savecsv: Exit')
	if icountExports == 0:
		allerrMsg = ['No Submissions available for this project: %s.'%theProject.shortTag]
		allerrMsg.append('No export submissions file created.')
		DebugOut(allerrMsg)
		return render(request, 'system_error.html', { 'syserrmsg': allerrMsg})
	return response
