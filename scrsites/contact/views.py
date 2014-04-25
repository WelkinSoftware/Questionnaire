from django.shortcuts import render
from django.http import HttpResponse
from scrsites.contact.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			request.session["subject"] = cd['subject']
			request.session["message"] = cd['message']
			request.session["email"] = cd['email']
#			send_mail(
#				cd['subject'],
#				cd['message'],
#				cd.get('email', 'noreply@example.com'),
#				['siteowner@example.com'],
#			)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm(
            initial={'subject': 'I love your site!'}
        )
        return render(request, 'contact/contact_form.html', {'form': form})
	
def contactThanks(request):
	return HttpResponse("Thank you")
