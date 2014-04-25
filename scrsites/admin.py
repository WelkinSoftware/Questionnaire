from django.contrib import admin
from scrsites.models import PatientBRCADataEntry, nonPtInfo

class BRCAAdmin(admin.ModelAdmin):
    list_display = ('patientName', 'birthDate', 'ptEmail', 'entryDate', 'referralDecision', 'questionnaireMode')
    ordering = ('patientName',)

admin.site.register(PatientBRCADataEntry, BRCAAdmin)  #register models for admin