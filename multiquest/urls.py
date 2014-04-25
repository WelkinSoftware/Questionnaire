from django.conf.urls import patterns, url
from multiquest import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^intro/$', views.intro, name='intro'),
	url(r'^registration/login/$',  views.login),
	url(r'^registration/logout/$', views.userLogout),	
	url(r'^registration/createNewAccount/$', views.createNewAccount),
	url(r'^registration/selectProjectDefault/$', views.selectProjectDefault),
	url(r'^registration/selectQuestionnaireDefault/$', views.selectQuestionnaireDefault),
	url(r'^registration/listRegistration/$', views.listRegistration),
	url(r'^registration/userLanding/$', views.userLanding),
	url(r'^registration/editProjectRecord/$', views.editProjectRecord),
	url(r'^working_pages/dumpSubmissionTable/$', views.dumpSubmissionTable),
	url(r'^working_pages/duplicateQuestionnaireView/$', views.duplicateQuestionnaireView),
	url(r'^working_pages/createProjectWithSamples/$', views.createProjectWithSamples),
	url(r'^working_pages/selectProjectsQuestionnairesToExecute/$', views.selectProjectsQuestionnairesToExecute),
	url(r'^working_pages/setSessionProjectQuestionnaireDefault/$', views.setSessionProjectQuestionnaireDefault),
	url(r'^working_pages/simplyExecuteTheQuestionnaire/$', views.simplyExecuteTheQuestionnaire),
	url(r'^working_pages/editQuestionnaire/$', views.editQuestionnaire),
	url(r'^working_pages/editDefaultPageTransitions/$', views.editDefaultPageTransitions),
	url(r'^working_pages/deleteQuestionnaireView/$', views.deleteQuestionnaireView),
	url(r'^working_pages/displayAndEditQuestion/$', views.displayAndEditQuestion),
	url(r'^working_pages/editSummaryAndAnalysisPage/$', views.editSummaryAndAnalysisPage),
	url(r'^working_pages/listQuestions/$', views.listQuestions),
	url(r'^working_pages/listPages/$', views.listPages),
	url(r'^working_pages/bulkPageEdit/$', views.bulkPageEdit),
	url(r'^working_pages/bulkQuestionEdit/$', views.bulkQuestionEdit),
#	url(r'^working_pages/completion/$', views.Completion),
	url(r'^working_pages/displayAndEditPage/$', views.displayAndEditPage),
	url(r'^working_pages/selectPages/$', views.selectPages),
	url(r'^working_pages/createPageQuestionLink/$', views.createPageQuestionLink),
	url(r'^working_pages/setPageToPageTransitionGlobalFlags/$', views.setPageToPageTransitionGlobalFlags),
	url(r'^working_pages/setPageToPageTransitionCalculated/$', views.setPageToPageTransitionCalculated),
	url(r'^working_pages/setGlobalFlags/$', views.setGlobalFlags),
	url(r'^working_pages/dumpSessionData/$', views.dumpSessionData),
	url(r'^working_pages/testing/$', views.testing),
	url(r'^working_pages/responseViewer/$', views.responseViewer),
	url(r'^working_pages/responseDelete/$', views.responseDelete),
	url(r'^working_pages/savecsv/$', views.savecsv),
	url(r'^working_pages/dumpSubmissionDataForProject/$', views.dumpSubmissionDataForProject),
	url(r'^working_pages/savepdf/$', views.savepdf),
	url(r'^working_pages/savecsvDecoder/$', views.savecsvDecoder),
	url(r'^working_pages/savePtResponse/$', views.savePtResponse),
	url(r'^explanations/(\w+)/$', views.scrnrexpln),
	url(r'^(\w+)/(\w+)/$', views.restartSession), # error exit when default not set
	url(r'^(\w+)/(\w+)/splash/$', views.splash, name='splash'), # first page of a questionnaire
		# first field is Project abbreviation, second is Questionnaire url
	url(r'^(\w+)/(\w+)/respondentIdent/$', views.respondentIdent, name='respondentIdent'),
	url(r'^(\w+)/(\w+)/completion/$', views.Completion, name='Completion'),
	url(r'^(\w+)/(\w+)/(\w+)/questionnaireSummary/$', views.questionnaireSummary, name='questionnaireSummary'),
	url(r'^(\w+)/(\w+)/(\w+)/$', views.QuestContinue, name='QuestContinue'),
)