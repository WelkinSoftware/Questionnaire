def selectProjectDefault(request):
	"""
	Allow the selection of a Project as a default to fill the UserProject table.
	Args
	http request
	
	Database
	Sets an association between User and Project in UserProject
	
	Session data
	Sets Project default.
	Uses temporary 'FselectProjectDefault'
	"""
	DebugOut('selectProjectDefault:  enter')
		
	# allProjectInfo record structure
	# [ Project short tag, name, email, projectAddress, contactPhone, internetLocation,
	# record number in the Project table ]
	theUser = request.user # user associated with this request.
	errMsg = []
	if request.method == 'POST':
		# Default project selected.
		# retrieve table from Session data
		if 'SelectProject' in request.POST:
			if 'FselectProjectDefault' in request.session:
				allProjectInfo = request.session['FselectProjectDefault']
				[dummyText, listRecNum] = request.POST['SelectProject'].split(" ") #decode the response
				# format is "Select" "record number in display list"
				recNum = int(listRecNum) - 1 # start with zero
				theProjectIDinDB = allProjectInfo[recNum][-1] # is the record number for the project
				try:
					theProject = Project.objects.get(id=theProjectIDinDB)
					setSessionProject(request, theProject) # set Session data default
					associateUserToProject(theProject, theUser)
					projectTag = theProject.shortTag
					errMsg.append('Project "%s" selected.' %projectTag)
					# delete the unneeded Session data
					del request.session['FselectProjectDefault']
					redirectURL = registrationURL_base + 'userLanding/'
					return HttpResponseRedirect(redirectURL)
				except Project.DoesNotExist:
					errMsg.append('System error (syserrmsg):  Project does not exist')
			else:
				allProjectInfo = displayProjectsWithinScope() # redo the data, since Session data missing
				request.session['FselectProjectDefault'] = allProjectInfo
				errMsg.append('Please select a Project.')			
		elif 'returnToHome' in request.POST:
			theUser = request.user # check for project registration
			theProject = getAssociatedProjectForUser(theUser)
			if theProject == None:
				errMsg.append('Please select a Project.')	
				allProjectInfo = displayProjectsWithinScope()
				request.session['FselectProjectDefault'] = allProjectInfo
			else:
				redirectURL = registrationURL_base + 'userLanding/'
				DebugOut('selectProjectDefault:  exit to %s'%redirectURL)
				return HttpResponseRedirect(redirectURL)
	else:
		allProjectInfo = displayProjectsWithinScope()
		request.session['FselectProjectDefault'] = allProjectInfo
		
	currentContext = {
		'theUser' : theUser,
		'allProjectInfo' : allProjectInfo,
		'errMsg' : errMsg,
		}
	DebugOut('selectProjectDefault:  exit')
	return render(request,'registration/selectProjectDefault.html',
		currentContext)
