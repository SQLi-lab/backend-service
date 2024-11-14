from django.shortcuts import render


def handler400(request, exception=None):
    return render(request, 'pages/400.html')


def handler403(request, exception=None):
    return render(request, 'pages/401.html')


def handler404(request, exception=None):
    return render(request, 'pages/404.html')


def handler500(request, exception=None):
    return render(request, 'pages/500.html')
