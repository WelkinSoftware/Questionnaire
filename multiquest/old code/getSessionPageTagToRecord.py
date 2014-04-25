# def getSessionPageTagToRecord(request):
# 	"""Gets page to record translation from Session Data.
# 	
# 	This page to record mapping depends upon the page transition table defined by the input
# 	Questionnaire.
# 	
# 	Purpose:  help with translating a url and mapping the page tag to a page record
# 	
# 	Args:
# 		request query
# 
# 	Returns:
# 		None.
# 		
# 	Side effects:
# 		Session data:  pageTagToRecord and recordToPageTag
# 		which are dictionary objects page short tag : to page record id
# 
# 	Raises:
# 		None.
# 	"""
# 	if 'pageTagToRecord' in request.session:
# 		pageTagToRecord = request.session['pageTagToRecord']
# 	else:
# 		pageTagToRecord = {}
# 	
# 	if 'recordToPageTag' in request.session:
# 		recordToPageTag = request.session['recordToPageTag']
# 	else:
# 		recordToPageTag = {}
# 
# 	return [pageTagToRecord,recordToPageTag]
