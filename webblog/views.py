from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse


def yandex_access(request):
    return render_to_response(
        'yandex_4176ffddb576e745.html', {},
        context_instance=RequestContext(request))


def robots(request):

    message = "User-agent: *\n"
    message += "Disallow: /static/\n"
    message += "Disallow: /admin/\n"
    message += "Disallow: /tag/\n"
    message += "Disallow: /category/\n"


    message += "Host: www.sdprog.ru\n\n"
    message += "Sitemap: http://www.sdprog.ru/sitemap.xml\n"

    resp = HttpResponse(message)
    resp['Content-Type'] = "text/plain"
    return resp

