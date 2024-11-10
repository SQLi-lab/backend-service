import hashlib
import random
import json
import uuid
import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotAllowed, \
    JsonResponse
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from django.db.models import Q
from sqli_api.models import Lab
from datetime import datetime

from sqli_lab.settings import DEPLOY_URL, DEPLOY_SECRET


@login_required
def labs(request):
    if request.method != 'GET':
        return render(request, 'pages/400.html')

    sort_by = request.GET.get('sort', 'date_created')

    active_labs = Lab.objects.filter(user_id=request.user,
                                     status__in=['В очереди',
                                                 'Создается',
                                                 'Выполняется']).values("uuid",
                                                                        "name",
                                                                        "date_created",
                                                                        "is_done",
                                                                        "status").order_by(
        '-id')

    removed_labs = Lab.objects.filter(user_id=request.user,
                                      status__in=['Ошибка создания',
                                                  'Ошибка удаления',
                                                  'Останавливается',
                                                  'Остановлена']).values("uuid",
                                                                         "name",
                                                                         "date_created",
                                                                         "is_done",
                                                                         "status").order_by(
        f'-{sort_by}')
    # Пагинация для архива
    paginator = Paginator(removed_labs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Пагинация для активных работ
    active_paginator = Paginator(active_labs, 8)
    active_page_num = request.GET.get('page_active')
    active_page_obj = active_paginator.get_page(active_page_num)

    show_pag_active = active_labs.count() > 8
    show_pag = removed_labs.count() > 8

    context = {'active_labs': active_labs, 'active_page_obj': active_page_obj,
               'removed_labs': removed_labs,
               'page_obj': page_obj,
               'user': request.user, 'sort_by': sort_by, 'paginator': paginator,
               'active_paginator': active_paginator,
               'show_pag_active': show_pag_active,
               'show_pag': show_pag}

    return render(request, 'labs/labs.html', context)


@login_required
def admin_labs(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    if not request.user.is_superuser:
        return render(request, 'pages/401.html')

    search = request.GET.get('search', '').strip()

    labs = Lab.objects.filter(user__group='student').order_by('-date_created')

    if search:
        labs = labs.filter(
            Q(name__icontains=search) | Q(uuid__icontains=search) | Q(
                status__icontains=search)
        )

    paginator = Paginator(labs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    show_pag = labs.count() > 10

    context = {
        'page_obj': page_obj,
        'show_pag': show_pag
    }

    return render(request, 'admin/admin_labs.html', context=context)


@login_required
def lab_add(request):
    if request.method != 'POST':
        return render(request, 'pages/400.html')

    user = request.user

    if Lab.objects.filter(user_id=user).filter(status__in=['В очереди',
                                                           'Создается',
                                                           'Выполняется']).exists() and not request.user.is_superuser:
        return render(request, 'pages/400.html')

    expired_seconds = 1800 if Lab.objects.filter(user=user,
                                                 is_done=True).exists() and not request.user.is_superuser else 10800

    lab = Lab.objects.create(
        uuid=uuid.uuid4(),
        user=user,
        status='В очереди',
        expired_seconds=expired_seconds
    )

    data = {
        'name': lab.name,
        'uuid': str(lab.uuid),
        'deploy_secret': DEPLOY_SECRET
    }

    try:
        response = requests.post(f'{DEPLOY_URL}/lab/add', json=data)
    except Exception as e:
        lab.status = 'Ошибка создания'
        lab.error_log = 'Ошибка создания лабораторной работы, сервер не доступен'
        lab.save()
        return JsonResponse(
            {'message': 'Ошибка создания лабораторной'},
            status=500)
    if response.status_code != 200:
        lab.status = 'Ошибка создания'
        lab.error_log = 'Ошибка создания лабораторной работы, сервер не доступен'
        lab.save()
        return JsonResponse(
            {'message': 'Ошибка создания лабораторной'},
            status=500)

    return JsonResponse(
        {'message': 'Лабораторная работа создана'},
        status=200)


@login_required
def lab_delete(request, uuid):
    if request.method != 'POST':
        return render(request, 'pages/400.html')

    lab = get_object_or_404(Lab, uuid=uuid)

    if lab.user != request.user:
        return render(request, 'pages/401.html')

    lab.status = 'Останавливается'
    lab.save()

    data = {
        'name': lab.name,
        'uuid': str(lab.uuid),
        'deploy_secret': DEPLOY_SECRET
    }

    try:
        response = requests.post(f'{DEPLOY_URL}/lab/delete', json=data)
    except Exception as e:
        lab.status = 'Ошибка удаления'
        lab.error_log = 'Ошибка удаления лабораторной работы, сервер не доступен'
        lab.save()
        return JsonResponse(
            {'message': 'Ошибка удаления лабораторной'},
            status=500)
    if response.status_code != 200:
        lab.status = 'Ошибка удаления'
        lab.error_log = 'Ошибка удаления лабораторной работы, сервер не доступен'
        lab.save()
        return JsonResponse(
            {'message': 'Ошибка создания лабораторной'},
            status=500)

    return JsonResponse(
        {'message': 'Лабораторная работа удалена'}, status=200)


@login_required
def lab_info(request, uuid):
    if request.method != 'GET':
        return render(request, 'pages/400.html')

    is_not_owner = False
    owner = None

    lab = get_object_or_404(Lab, uuid=uuid)
    if lab.user.id != request.user.id:
        if not request.user.is_superuser:
            return render(request, 'pages/401.html')
        is_not_owner = True
        owner = lab.user

    current_time = make_aware(datetime.now())
    duration_seconds = lab.expired_seconds
    if lab.date_started is not None:
        date_started = lab.date_started
        elapsed_time = (current_time - date_started).total_seconds()
        remaining_seconds = max(duration_seconds - elapsed_time, 0)
    else:
        remaining_seconds = 1

    context = {
        'lab': lab, "remaining_seconds": remaining_seconds, 'owner': owner,
        'is_not_owner': is_not_owner
    }
    return render(request, 'labs/lab_info.html', context)


def lab_check(request, uuid):
    if request.method != 'POST':
        return render(request, 'pages/400.html')

    data = json.loads(request.body)
    secret = data.get('secret', None)
    if not secret:
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется секрет'}, status=400)

    lab = get_object_or_404(Lab, uuid=uuid)

    if lab.user.id != request.user.id and not request.user.is_superuser:
        return render(request, 'pages/401.html')

    if lab.is_done:
        return JsonResponse(
            {'message': 'Данные верны', 'status': 'success'}, status=200)

    if hashlib.sha256(secret.encode('utf-8')) == lab.secret_hash:
        lab.date_done = make_aware(datetime.now())
        lab.is_done = True
        lab.save()
        return JsonResponse(
            {'message': 'Данные верны', 'status': 'success'}, status=200)

    return JsonResponse(
        {'message': 'Данные не верны', 'status': 'error'}, status=400)


@login_required
def labs_stats(request):
    created_count = Lab.objects.filter(user=request.user).count()
    completed_count = Lab.objects.filter(user=request.user,
                                         is_done=True).count()

    data = {
        'created': created_count,
        'completed': completed_count,
    }
    return JsonResponse(data)
