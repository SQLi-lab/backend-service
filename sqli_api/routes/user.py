from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from sqli_api.config import GROUP_MAP, YES_NO
from sqli_api.models import CustomUser, Lab
from django.shortcuts import render


@login_required
def my_account(request):
    """
    Функция рендерит страницу Профиль
    :param request:
    :return:
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'], 'Метод не поддерживается')

    user = CustomUser.objects.filter(id=request.user.id).first()

    user_labs = Lab.objects.filter(user_id=user.id)
    all_labs = user_labs.count()
    active_labs = user_labs.filter(
        status__in=["Создается", "Выполняется"]).count()
    done_labs = user_labs.filter(is_done=True).count()

    context = {"user": user, "role": GROUP_MAP[user.group],
               "verified": YES_NO[user.verified], "all_labs": all_labs,
               "active_labs": active_labs, "done_labs": done_labs}

    return render(request, 'user/user.html', context)

