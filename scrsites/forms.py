# Forms for screener pages
from django import forms
from django.forms.widgets import RadioSelect

class p0Form(forms.Form):
    patientName = forms.CharField(max_length=50, label='My name is (last, first)')
    birthDate = forms.DateField(label='My birth date is (mm/dd/yyyy)')
    ptEmail = forms.EmailField( required=False, label='My e-mail address is')

class p1Form(forms.Form):
    pHxOvarianCA = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')], 
    	label='Have you ever had ovarian cancer?')

class aboveAverageRiskForm(forms.Form):
	patientCallbackNumber = forms.CharField(max_length=30, required=False, label='Patient phone')
	callbackReq = forms.BooleanField( required=False, label='Call back request')
	
class AverageRiskForm(forms.Form):
	placeF = forms.CharField(max_length=30, required=False, label='Place holder')

class IndetermRiskForm(forms.Form):
	placeF = forms.CharField(max_length=30, required=False, label='Place holder')

class p2Form(forms.Form):
    fHxOvarianCA = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')],
    	label='Have any of your close blood relatives ever had ovarian cancer?')

class p3Form(forms.Form):
    pHxBreastCA = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')], 
    label="""Have you ever had <a title="Tap here for more information about breast cancer"
            href="{{urlprefix}}scrn/explanations/moreonbreastca">
        breast cancer or DCIS?</a>.""")

class p3aForm(forms.Form):
	pHxBrCALE50Years = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCA3Neg = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCAGT1PrimarySame = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCAGT1PrimaryBoth = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCADermMan = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])

class p3bForm(forms.Form):
	ashkenaziJewish = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCAGE1RelBrCALE50Years = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	pHxBrCAGE2RelBrPancCA = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])

class p3c_Agg_queryForm(forms.Form): # aggregate "yes" or "no" query
	none_of_the_above = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')],
		label='If you have had any of these cancers, click "yes" to select.')

class p3cForm(forms.Form):
	error_css_class = 'error'
	required_css_class = 'required'
	pHxBrCAThyroidCA = forms.BooleanField(required=False,
		label="Thyroid cancer?")
	pHxBrCASarcoma = forms.BooleanField(required=False,
		label="Sarcoma?")
	pHxBrCAAdrenalCA = forms.BooleanField(required=False,
		label="Adrenal cancer?")
	pHxBrCAEndometrialCA = forms.BooleanField(required=False,
		label="Cancer of the uterus?")
	pHxBrCAPancreaticCA = forms.BooleanField(required=False,
		label="Pancreatic cancer?")
	pHxBrCABrainTumors = forms.BooleanField(required=False,
		label="Brain tumors?")
	pHxBrCAGastricCA = forms.BooleanField(required=False,
		label="Stomach cancer?")
	pHxBrCALeukLymphoma = forms.BooleanField(required=False,
		label="Leukemia or lymphoma?")

class p4Form(forms.Form):
	recognizedRiskGroup = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	fHxBrCASuscGene = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	fHxBreastCA = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])

class p4aForm(forms.Form):
	fHxBrCAMale = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	fHxBrCASameSideGE2 = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])
	
class p4b_Agg_queryForm(forms.Form): # aggregate "yes" or "no" query
	none_of_the_above = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')],
		label='If that relative had any of these cancers, click "yes"')

class p4bForm(forms.Form):
	error_css_class = 'error'
	required_css_class = 'required'
	fHxBrCADermMan = forms.BooleanField(required=False,
		label="Breast cancer involving the skin overlying the breast?")
	fHxBrCAThyroidCA = forms.BooleanField(required=False,
		label="Thyroid cancer?")
	fHxBrCASarcoma = forms.BooleanField(required=False,
		label="Sarcoma?")
	fHxBrCAAdrenalCA = forms.BooleanField(required=False,
		label="Adrenal cancer?")
	fHxBrCAEndometrialCA = forms.BooleanField(required=False,
		label="Cancer of the uterus?")
	fHxBrCAPancreaticCA = forms.BooleanField(required=False,
		label="Pancreatic cancer?")
	fHxBrCABrainTumors = forms.BooleanField(required=False,
		label="Brain tumors?")
	fHxBrCAGastricCA = forms.BooleanField(required=False,
		label="Stomach cancer?")
	#Diffuse gastric cancer
	fHxBrCALeukLymphoma = forms.BooleanField(required=False,
		label="Leukemia or lymphoma?")

class p5Form(forms.Form):
	fHxSufficient = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Yes', 'Yes'), ('No', 'No')])

class setDebugOptionsForm(forms.Form):
	specialDebugOutput = forms.BooleanField(required=False, label="Turn on special debug output.")
