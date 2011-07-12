from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from editions.models import *

import datetime

def show(request, year=None, month=None, day=None):
    if year and month and day:
        year = int(year)
        month = int(month)
        day = int(day)
        
        date = datetime.date(year, month, day)
    else:
        date = datetime.datetime.today()
    
    try:
        edition = Edition.objects.get(date=date)
    except Edition.DoesNotExist:
        try:
            edition = Edition.objects.filter(date__lt=date)[0]
        except:
            edition = Edition.objects.all()[0]
        redirect(edition.date.strftime("/%Y-%m-%d"))
    
    return render_to_response('show.html', {
            'edition': edition,
        },
        context_instance=RequestContext(request)
    )

def search(request):
    q = request.GET.get('q')
    
    if q:
        list = Page.objects.filter(index__icontains=unicode(query))
    
        return render_to_response('search.html', {
                'edition': Edition.objects.get(pk=1),
                'list': list,
                'query': query,
            },
            context_instance=RequestContext(request)
        )
    else:
        return redirect("/")

def search_redirect(request):
    q = request.GET.get('q')
    
    if q:
        return redirect("/search/%s" % q, permanent=True)
    else:
        return redirect("/", permanent=True)