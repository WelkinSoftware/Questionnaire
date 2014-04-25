	if submitSelected:
		DebugOut('submit Selected')
		# get the questionnaire object
		aquaireObj = theSubmission.questionnaireID
		# construct a table with field names and field values
		# Again add pt id and header information
		respObj = theSubmission.respondentID
		respName = respondentName( respObj )
		birthDay = str(respObj.birthDate)
		respondentDataCol = [
			theSubmission.lastUpdate,
			respName,
			birthDay,
			aquaireObj.barTitle,
			aquaireObj.version,
			aquaireObj.versionDate,
			theSubmission.reviewedBy,
			theSubmission.reviewDate,
			theSubmission.okForExport,
			]
		respondentQuestIDCol = [
			'Last updated',
			"Respondent's name",
			"Respondent's birthday",
			'Questionnaire name',
			'Questionnaire version',
			'Questionnaire version date',
			'Reviewed by',
			'Review date',
			'Ok for export?',
			 ]
