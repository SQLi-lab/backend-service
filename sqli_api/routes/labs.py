import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, \
    JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from sqli_api.models import Lab


@login_required
def labs(request):
    """
    Функция возвращает список лаб пользователя
    :param request:
    :return: страница 'labs'
    """
    sort_by = request.GET.get('sort', 'date_created')

    active_labs = Lab.objects.filter(user_id=request.user,
                                     status__in=['Создается',
                                                 'Создана']).values("uuid",
                                                                    "name",
                                                                    "date_created",
                                                                    "is_done",
                                                                    "status").order_by(
        '-id')

    removed_labs = Lab.objects.filter(user_id=request.user,
                                      status__in=['Ошибка создания',
                                                  'Останавливается',
                                                  'Остановлена',
                                                  'Решена']).values("uuid",
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

    context = {'active_labs': active_labs, 'active_page_obj': active_page_obj, 'removed_labs': removed_labs,
               'page_obj': page_obj,
               'user': request.user, 'sort_by': sort_by, 'paginator': paginator,
               'active_paginator': active_paginator,
               'page_obj': page_obj, }

    return render(request, 'labs/labs.html', context)


@login_required
def lab_add(request):
    if request.method == 'POST':
        user = request.user

        if Lab.objects.filter(user_id=user).filter(status__in=['Создается',
                                                               'Создана']).exists() and not request.user.is_superuser:
            return JsonResponse(
                {'message': 'Нельзя создать более 1 лабы'}, status=400)

        expired_seconds = 1800 if Lab.objects.filter(user=user,
                                                     is_done=True).exists() and not request.user.is_superuser else 10800

        lab = Lab.objects.create(
            uuid=uuid.uuid4(),
            unique_secret_hash=f'secret_{str(uuid.uuid4().hex)}',
            user=user,
            status='Создается',
            expired_seconds=expired_seconds
        )

        # TODO: shared_tash creating

        return JsonResponse(
            {'message': 'Лабораторная работа создана', 'lab_id': lab.id},
            status=200)

    return HttpResponseNotAllowed(['POST'], 'Метод не поддерживается')


@login_required
def lab_delete(request, uuid):
    if request.method == 'POST':
        lab = get_object_or_404(Lab, uuid=uuid)

        if lab.user != request.user:
            return JsonResponse(
                {'message': 'Нельзя удалить чужую лабу!'}, status=403)

        # TODO: shared_tash
        lab.status = 'Останавливается'
        lab.save()

        return JsonResponse(
            {'message': 'Лабораторная работа удалена', 'lab_id': lab.id},
            status=200)
    return HttpResponseNotAllowed(['POST'], 'Метод не поддерживается')


@login_required
def lab_info(request, uuid):
    lab = get_object_or_404(Lab, uuid=uuid)
    context = {
        'lab': lab
    }
    return render(request, 'labs/lab_info.html', context)


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
