from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from editions.models import *

import datetime

def show(request, year=None, month=None, day=None):
    
    # build a date
    if year and month and day:
        year = int(year)
        month = int(month)
        day = int(day)
        
        date = datetime.date(year, month, day)
    else:
        date = datetime.datetime.today()
    
    # get edition object, if not redirect to the latest
    try:
        edition = Edition.objects.get(date=date)
    except Edition.DoesNotExist:
        try:
            edition = Edition.objects.filter(date__lt=date)[0]
        except:
            edition = Edition.objects.all()[0]
        redirect(edition.date.strftime("/%Y-%m-%d"))
    
    # browser level 1 - full, desktop
    if request.browser_level == 1:
        return render_to_response('show_1.html', {
                'edition': edition,
            },
            context_instance=RequestContext(request)
        )
    
    # browser level 2 - advanced, e.g. iphone, android
    elif request.browser_level == 2:
        return render_to_response('show_2.html', {
                'edition': edition,
            },
            context_instance=RequestContext(request)
        )
    
    # browser level 3 - all other mobile devices
    else:
        return render_to_response('show_3.html', {
                'edition': edition,
            },
            context_instance=RequestContext(request)
        )

def search(request):
    q = request.GET.get('q')
    
    if q:
        list = Page.objects.filter(index__icontains=unicode(query))
        
        # browser level 1 - full, desktop
        if request.browser_level == 1:
            return render_to_response('search_1.html', {
                    'edition': Edition.objects.get(pk=1),
                    'list': list,
                    'query': query,
                },
                context_instance=RequestContext(request)
            )
        
        # browser level 2 - advanced, e.g. iphone, android
        elif request.browser_level == 2:
            return render_to_response('search_2.html', {
                    'edition': Edition.objects.get(pk=1),
                    'list': list,
                    'query': query,
                },
                context_instance=RequestContext(request)
            )
        
        # browser level 3 - all other mobile devices
        else:
            return render_to_response('search_3.html', {
                    'edition': Edition.objects.get(pk=1),
                    'list': list,
                    'query': query,
                },
                context_instance=RequestContext(request)
            )
    else:
        return redirect("/")

"""def if_ie6(request):
    user_agent = request.META['HTTP_USER_AGENT']"""