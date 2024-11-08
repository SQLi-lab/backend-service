import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, \
    JsonResponse
from django.shortcuts import render, get_object_or_404

from sqli_api.models import Lab


@login_required
def labs(request):
    """
    Функция возвращает список лаб пользователя
    :param request:
    :return: страница 'labs'
    """
    active_labs = Lab.objects.filter(user_id=request.user,
                                     status__in=['Создается',
                                                 'Создана']).order_by('-id')

    removed_labs = Lab.objects.filter(user_id=request.user,
                                      status__in=['Ошибка создания',
                                                  'Останавливается',
                                                  'Остановлена',
                                                  'Решена']).order_by('-id')

    context = {'active_labs': active_labs, 'removed_labs': removed_labs}

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
def lab_delete(request, id):
    if request.method == 'POST':
        lab = get_object_or_404(Lab, id=id)

        if lab.user != request.user:
            return JsonResponse(
                {'message': 'Нельзя удалить чужую лабу!'}, status=403)

        # TODO: shared_tash
        lab.status = 'Останавливается'
        lab.save()

        return JsonResponse(
            {'message': 'Лабораторная работа удалена', 'lab_id': id},
            status=200)
    return HttpResponseNotAllowed(['POST'], 'Метод не поддерживается')


@login_required
def lab_info(request, id):
    lab = get_object_or_404(Lab, id=id)
    context = {
        'lab': lab
    }
    return render(request, 'labs/lab_info.html', context)
