from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class	nonPtInfo(models.Model):
	questionnaireTitle = models.CharField(max_length=100)
	questionnaireVersion = models.CharField(max_length=30, blank=True)
	questionnaireUpdate = models.CharField(max_length=30, blank=True)
	questionnaireEmail = models.CharField(max_length=30, blank=True)
	projectName = models.CharField(max_length=100)
	projectAbbrev = models.CharField(max_length=30, blank=True)
	projectContactPhone = models.CharField(max_length=30, blank=True)
	projectInternetResources = models.CharField(max_length=500, blank=True)
	projectInformedConsent = models.CharField(max_length=500, blank=True)
	genericInternetResources = models.CharField(max_length=500, blank=True)
	
class	PatientBRCADataEntry(models.Model):
	# p0
	patientName = models.CharField(max_length=30)
	birthDate = models.DateField()
	ptEmail = models.EmailField(max_length=75, blank=True)
	patientUniqueID = models.CharField(max_length=60, unique=True) # constructed
	entryDate = models.DateField()
	referralDecision = models.CharField(max_length=30)
	#questionnaire information
	questionnaireTitle = models.CharField(max_length=100, blank=True)
	questionnaireVersion = models.CharField(max_length=30, blank=True)
	questionnaireMode = models.CharField(max_length=30, blank=True) # e.g. "quickExit"
	questionnaireUpdate = models.CharField(max_length=30, blank=True) # version date
	
	# Callback number and associated checkbox
	callbackReq = models.BooleanField(max_length=30, blank=True)
	patientCallbackNumber = models.CharField(max_length=30, blank=True)
	# p1
	pHxOvCARiskGroupA = models.BooleanField( blank=True ) # *** not in any page
	pHxOvarianCA = models.CharField(max_length=30, blank=True) # page p1
	pHxFallopianCA = models.CharField(max_length=30, blank=True) # *** not in any page
	pHxPeritonealCA = models.CharField(max_length=30, blank=True) # *** not in any page
	fHxOvCARiskGroupA = models.CharField(max_length=30, blank=True) # *** not in any page
	fHxOvarianCA = models.CharField(max_length=30, blank=True) # page p2
	fHxFallopianCA = models.CharField(max_length=30, blank=True) # *** not in any page
	fHxPeritonealCA = models.CharField(max_length=30, blank=True) # *** not in any page
	# Recognized risk group variables
	recognizedRiskGroup = models.CharField(max_length=30, blank=True)	# page p4
	ashkenaziJewish = models.CharField(max_length=30, blank=True) # page p3b
	pHxBreastCA = models.CharField(max_length=30, blank=True) # page p3
	fHxBreastCA = models.CharField(max_length=30, blank=True)	# page p4
	fHxBrCASuscGene = models.CharField(max_length=30, blank=True)	# page p4
	fHxSufficient = models.CharField(max_length=30, blank=True)	# page p5
	pHxBrCARiskGroupA = models.CharField(max_length=30, blank=True) # *** not in any page
	pHxBrCALE50Years = models.CharField(max_length=30, blank=True)	# page p3a
	pHxBrCA3Neg = models.CharField(max_length=30, blank=True)	# page p3a
	pHxBrCAGT1PrimarySame = models.CharField(max_length=30, blank=True)	# page p3a
	pHxBrCAGT1PrimaryBoth = models.CharField(max_length=30, blank=True)	# page p3a
	pHxBrCADermMan = models.CharField(max_length=30, blank=True)	# page p3a
	pHxBrCARiskGroupB = models.CharField(max_length=30, blank=True) # *** not in any page
	pHxBrCAGE1RelBrCALE50Years = models.CharField(max_length=30, blank=True)	# page p3b
	pHxBrCAGE2RelBrPancCA = models.CharField(max_length=30, blank=True)	# page p3b
	pHxBrCARiskGroupC = models.CharField(max_length=30, blank=True) # *** not in any page
	pHxBrCAThyroidCA = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCASarcoma = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCAAdrenalCA = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCAEndometrialCA = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCAPancreaticCA = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCABrainTumors = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCAGastricCA = models.CharField(max_length=30, blank=True)	# page p3c
	pHxBrCALeukLymphoma = models.CharField(max_length=30, blank=True)	# page p3c
	fHxBrCARiskGroupA = models.CharField(max_length=30, blank=True) # *** not in any page
	fHxBrCAMale = models.CharField(max_length=30, blank=True)	# page p4a
	fHxBrCASameSideGE2 = models.CharField(max_length=30, blank=True)	# page p4a
	fHxBrCARiskGroupB = models.CharField(max_length=30, blank=True) # *** not in any page
	fHxBrCADermMan = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCAThyroidCA = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCASarcoma = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCAAdrenalCA = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCAEndometrialCA = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCAPancreaticCA = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCABrainTumors = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCAGastricCA = models.CharField(max_length=30, blank=True)	# page p4b
	fHxBrCALeukLymphoma = models.CharField(max_length=30, blank=True)	# page p4b
		
	def __unicode__(self):
		return self.patientName

class	RiskNames(models.Model): # Assocate risk ID with text for summary page
	riskID = models.CharField(max_length=30)
	riskDeclarYes = models.CharField(max_length=500)
	riskDeclarNo =  models.CharField(max_length=500)
	