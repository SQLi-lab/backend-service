from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render

@login_required
def admin_help(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    return render(request, 'admin/help.html')
