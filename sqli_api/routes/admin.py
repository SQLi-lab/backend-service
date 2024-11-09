import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse
from django.shortcuts import render

from sqli_api.models import CustomUser, Lab


@login_required
def admin_help(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    return render(request, 'admin/help.html')


@login_required
def admin_users(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    search = request.GET.get('search', '').strip()

    students = CustomUser.objects.filter(group='student').order_by('verified')

    if search:
        students = students.filter(
            Q(email__icontains=search) | Q(uuid__icontains=search) | Q(
                group__icontains=search) | Q(username__icontains=search)
        )

    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    show_pag = students.count() > 10

    context = {
        'page_obj': page_obj,
        'show_pag': show_pag
    }

    return render(request, 'admin/users.html', context=context)


@login_required
def admin_user_verify(request, uuid):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    try:
        user = CustomUser.objects.get(uuid=uuid)
        user.verified = True
        user.save()
    except Exception as e:
        return JsonResponse(
            {'message': f'Ошибка верификации: {e}', 'status': 'error'},
            status=400)

    return JsonResponse(
        {'message': 'Пользователь верифицирован', 'status': 'success'},
        status=200)


@login_required
def admin_user_delete(request, uuid):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    try:
        user = CustomUser.objects.get(uuid=uuid)
        user.delete()
    except Exception as e:
        return JsonResponse(
            {'message': f'Ошибка удаления: {e}', 'status': 'error'}, status=400)

    return JsonResponse(
        {'message': 'Пользователь удален', 'status': 'success'}, status=200)


@login_required
def admin_labs_dump(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = f'attachment; filename="labs_dump_{datetime.now()}.csv"'
    response.write('\ufeff'.encode('utf-8-sig'))

    writer = csv.writer(response)
    writer.writerow(
        ['id', 'name', 'uuid', 'url', 'secret_hash', 'expired_seconds',
         'date_created', 'date_started', 'is_done', 'date_done', 'status',
         'error_log', 'user_id'])

    for lab in Lab.objects.all():
        writer.writerow([lab.id, lab.name, lab.uuid, lab.url, lab.secret_hash,
                         lab.expired_seconds, lab.date_created,
                         lab.date_started, lab.is_done, lab.date_done,
                         lab.status, lab.error_log, lab.user_id])

    return response


@login_required
def admin_users_dump(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = f'attachment; filename="users_dump_{datetime.now()}.csv"'
    response.write('\ufeff'.encode('utf-8-sig'))

    writer = csv.writer(response)
    writer.writerow(
        ['id', 'password', 'last_login', 'username', 'uuid', 'study_group',
         'group', 'email', 'verified', 'is_active', 'is_staff', 'is_superuser',
         'date_joined', ])

    for user in CustomUser.objects.all():
        writer.writerow(
            [user.id, user.password, user.last_login, user.username, user.uuid,
             user.study_group, user.group, user.email, user.verified,
             user.is_active, user.is_staff, user.is_superuser,
             user.date_joined])

    return response
