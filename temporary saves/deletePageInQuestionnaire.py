def deletePageInQuestionnaire(theQuestionnaire, pageToDeleteObj):
	"""The page is deleted and QuestionnairePage is updated to repair the hole in the
	transition matrix
		
	Args:
		theQuestionnaire
		pageToDeleteObj - the page is inserted "after" this page in the transition matrix
	"""
	try:
		# search for the page to be deleted appearing in the "from" field in QuestionnairePage
		QPtoUpdate = QuestionnairePage.objects.get(
			questionnaireID = theQuestionnaire,
			pageID =pageToDeleteObj,
			recordType = 'next_page_default',
			) # should be only one record retrieval!!
		toPage = QPtoUpdate.nextPageID
		# check if pageToDeleteObj is the start page
		try:
			QPstartPage = QuestionnairePage.objects.get(
				questionnaireID = theQuestionnaire,
				pageID =pageToDeleteObj,
				recordType = 'start_page',
				) # should be only one record retrieval!!
			# pageToDeleteObj is a start page.
			# update to next page
			QPstartPage.pageID=toPage
			QPstartPage.nextPageID=toPage
		except:
			# not a start page. Do nothing for now
			pass
	except:
		# Could mean that pageToDeleteObj is at the end of the line.
		# Or could be that the transition matrix is screwed up
		# Makes it easy. Delete. The Cascade option will delete any QuestionnairePage
		# records which point to pageToDeleteObj in the "to" field.
		pageToDeleteObj.delete()
		return True
	# check for a page pointing "to" pageToDeleteObj
	# May be more than one.
	try:
		QPToPage = QuestionnairePage.objects.filter(
			questionnaireID = theQuestionnaire,
			nextPageID =pageToDeleteObj,
			recordType = 'next_page_default',
			) # May be more than one.
		# replace the "to" with "toPage" above which pageToDeleteObj points to
		for aQPrec in QPToPage:
			aQPrec.nextPageID = toPage,
			aQPrec.save()
		# pageToDeleteObj is now disassociated from the transition matrix
		pageToDeleteObj.delete()
	except:
		# This page has no precedent, therefore at the beginning of the line
		pageToDeleteObj.delete()
	return True
