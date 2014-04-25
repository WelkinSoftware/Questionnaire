# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from scrsites.books.models import Book

def search_form(request):
    return render(request, 'search_form.html')
    
def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			books = Book.objects.filter(title__icontains=q)
			return render(request, 'search_results.html',
				{'books': books, 'query': q})
	return render(request, 'search_form.html',
		{'error': error})