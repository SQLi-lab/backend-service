from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render


@login_required
def help(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    return render(request, 'help.html')
