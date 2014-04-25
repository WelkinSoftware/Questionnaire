from multiquest.adminUtilities import *
from multiquest.forms import *
from multiquest.models import *
from multiquest.views import *
from multiquest.utilities import *
from multiquest.utilities_db import *
from django.contrib.auth.models import Group, User, Permission
theProjectTag = 'test_project'
theProject = getProjectObj( theProjectTag)
questionnaireShortTag = 'TestQuest'
theQuestionnaire= getQuestionnaireObjFromTags( theProjectTag, questionnaireShortTag)

# test creating
newShortTag='DupTest3'
newQuestionnaire = duplicateQuestionnaire(theProject, theQuestionnaire, newShortTag)
allPages = getAllPageObjsForQuestionnaire(newQuestionnaire)
oldQuestionnaire= getQuestionnaireObjFromTags( theProjectTag, questionnaireShortTag) # restore

# verify that the pages have been duplicated
oldQuestionnaire
allpOld = getAllPageObjsForQuestionnaire(oldQuestionnaire)
newQuestionnaire
allpNew = getAllPageObjsForQuestionnaire(newQuestionnaire)
allpOld
allpNew
len(allpOld)
len(allpNew


# test deleting
newShortTag='DupTest'
testQuestionnaire = getQuestionnaireObjFromTags( theProjectTag, newShortTag)
deleteQuestionnaire(testQuestionnaire)